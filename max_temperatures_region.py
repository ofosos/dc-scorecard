#!/usr/bin/env python3
"""Fetch two years of daily maximum temperatures for each Azure region.

Reads ``az_regions_annotated.json`` (Azure region list with lat/long metadata),
queries Open-Meteo's Historical Weather Archive API for the daily maximum
temperature of the last two years for every region, and writes a JSON
dictionary:

    {
        "<azure region programmatic name>": [
            ["YYYY-MM-DD", 12.3],
            ...
        ],
        ...
    }

Usage:
    python fetch_region_temperatures.py                 # all regions, write region_temperatures.json
    python fetch_region_temperatures.py --test          # live API smoke test (3 regions, 7 days)
    python fetch_region_temperatures.py --regions westeurope,uaenorth
    python fetch_region_temperatures.py --output out.json --workers 8

Requires: pandas, numpy, requests
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DEFAULT_INPUT = Path("az_regions_annotated.json")
DEFAULT_OUTPUT = Path("region_temperatures.json")

# Open-Meteo free tier: non-commercial use without a key, up to 10k calls/day.
# Be polite: retry on 429/5xx with exponential backoff.
MAX_RETRIES = 5
TIMEOUT = 60  # seconds


def date_range(years: int = 2) -> tuple[str, str]:
    """Return (start_date, end_date) ISO strings covering the last `years` years."""
    end = date.today() - timedelta(days=5)  # archive lags a few days behind
    start = end - timedelta(days=365 * years)
    return start.isoformat(), end.isoformat()


def load_regions(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        regions = json.load(fh)
    keep = []
    for region in regions:
        meta = region.get("metadata", {})
        lat, lon = meta.get("latitude"), meta.get("longitude")
        if lat is None or lon is None:
            print(f"  skipping {region.get('name')}: no coordinates", file=sys.stderr)
            continue
        keep.append(
            {
                "name": region["name"],
                "displayName": region.get("displayName", region["name"]),
                "latitude": float(lat),
                "longitude": float(lon),
            }
        )
    return keep


def fetch_region_daily_max(
    session: requests.Session,
    region: dict,
    start_date: str,
    end_date: str,
) -> dict[str, list]:
    """Query Open-Meteo archive for one region; return {region_name: [(date, tmax), ...]}."""
    params = {
        "latitude": region["latitude"],
        "longitude": region["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max",
        "timezone": "UTC",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(ARCHIVE_URL, params=params, timeout=TIMEOUT)
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = 2 ** attempt
                print(
                    f"  {region['name']}: HTTP {resp.status_code}, retrying in {wait}s "
                    f"({attempt}/{MAX_RETRIES})",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            resp.raise_for_status()
            payload = resp.json()
        except (requests.RequestException, ValueError) as exc:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"{region['name']}: request failed: {exc}") from exc
            time.sleep(2 ** attempt)
            continue

        daily = payload.get("daily", {})
        dates = daily.get("time", [])
        temps = daily.get("temperature_2m_max", [])
        if not dates:
            raise RuntimeError(f"{region['name']}: API returned no daily data: {payload}")

        # pandas Series with numpy float64 values; NaN = missing data
        series = pd.Series(
            np.asarray(temps, dtype=float), index=pd.to_datetime(dates), name=region["name"]
        )
        pairs = [
            [ts.strftime("%Y-%m-%d"), round(float(t), 1)]
            for ts, t in series.items()
            if pd.notna(t)
        ]
        return {region["name"]: pairs}

    raise RuntimeError(f"{region['name']}: exhausted retries")


def fetch_all(regions: list[dict], start_date: str, end_date: str, workers: int) -> dict:
    results: dict[str, list] = {}
    session = requests.Session()
    session.headers.update({"User-Agent": "azure-region-temperature-fetch/1.0"})

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_region_daily_max, session, region, start_date, end_date): region
            for region in regions
        }
        done = 0
        for future in as_completed(futures):
            region = futures[future]
            done += 1
            try:
                results.update(future.result())
                n = len(next(iter(future.result().values())))
                print(f"[{done}/{len(regions)}] {region['displayName']}: {n} days")
            except RuntimeError as exc:
                print(f"[{done}/{len(regions)}] FAILED {region['displayName']}: {exc}", file=sys.stderr)
    return results


def run_test() -> int:
    """Smoke test against the live API: 3 regions, 7 days of data."""
    regions = [
        {"name": "germanywestcentral", "displayName": "Germany West Central",
         "latitude": 50.11, "longitude": 8.68},
        {"name": "qatarcentral", "displayName": "Qatar Central",
         "latitude": 25.29, "longitude": 51.53},
        {"name": "westus3", "displayName": "West US 3",
         "latitude": 33.45, "longitude": -112.07},
    ]
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=7)
    print(f"Live API test: {start} .. {end}")
    results = fetch_all(regions, start.isoformat(), end.isoformat(), workers=3)
    ok = True
    for r in regions:
        data = results.get(r["name"])
        if not data:
            print(f"  FAIL: no data for {r['name']}")
            ok = False
        else:
            temps = [t for _, t in data]
            print(
                f"  OK {r['name']}: {len(data)} days, "
                f"min {min(temps):.1f} C, max {max(temps):.1f} C "
                f"(sample: {data[0]}, {data[-1]})"
            )
    print("TEST " + ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help=f"Azure regions JSON (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"Output JSON file (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--regions", type=str, default=None,
                        help="Comma-separated subset of programmatic region names")
    parser.add_argument("--years", type=int, default=2,
                        help="How many years back to query (default: 2)")
    parser.add_argument("--workers", type=int, default=5,
                        help="Parallel requests (default: 5; be gentle with the free tier)")
    parser.add_argument("--test", action="store_true",
                        help="Run a live API smoke test instead of the full fetch")
    args = parser.parse_args()

    if args.test:
        return run_test()

    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")

    regions = load_regions(args.input)
    if args.regions:
        wanted = {r.strip() for r in args.regions.split(",")}
        missing = wanted - {r["name"] for r in regions}
        if missing:
            parser.error(f"unknown region(s): {', '.join(sorted(missing))}")
        regions = [r for r in regions if r["name"] in wanted]

    print(f"Querying {len(regions)} regions for {args.years} year(s) of daily max temperature")

    start_date, end_date = date_range(args.years)
    print(f"Date range: {start_date} .. {end_date}")

    results = fetch_all(regions, start_date, end_date, args.workers)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print(f"Wrote {args.output}: {len(results)} regions, "
          f"{sum(len(v) for v in results.values())} date/temperature pairs")

    if len(results) < len(regions):
        print("WARNING: some regions failed; re-run with --regions <names> to retry them",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())