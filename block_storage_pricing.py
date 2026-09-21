#!/usr/bin/env python3
"""Fetch Azure block storage (managed disk) prices per GB for each region.

Reads ``az_regions_annotated.json`` (Azure region list) and queries the
Azure Retail Prices API (https://prices.azure.com/api/retail/prices) for
managed disk meters, then writes a long-format CSV with one row per
(region, performance, redundancy):

    Region,Performance,Redundancy,PricePerGB

Dimension mapping (Azure does not sell every combination):

- Performance:
    Standard HDD -> "Standard HDD Managed Disks"
    Standard SSD -> "Standard SSD Managed Disks"
    Premium SSD  -> "Premium SSD Managed Disks"
    Ultra Disk   -> "Ultra Disks"
- Redundancy:
    LRS / ZRS

Azure does not publish a single per-GB meter for managed disks other
than Ultra Disk.  The per-GB price is therefore derived from the
cheapest per-GB available disk tier, the 1 TiB disks (S30/E30/P30),
which carry the same per-GB rate as all tiers of their family:

- Standard HDD / Standard SSD / Premium SSD: S30/E30/P30 "Disk" meter
  (unit ``1/Month``) divided by 1024 GiB.
- Ultra Disk: "Ultra LRS Provisioned Capacity" meter (unit
  ``1 GiB/Hour``) multiplied by 730 hours per month.

Cells Azure does not sell are written with the string "na":
- Standard HDD is not offered with ZRS.
- Ultra Disk is only offered with LRS.
- ZRS managed disks require availability zones; regions without them
  (e.g. australiacentral) have no ZRS prices at all.

Usage:
    python block_storage_pricing.py                    # all regions -> block_storage_pricing.csv
    python block_storage_pricing.py --regions westeurope,uaenorth
    python block_storage_pricing.py --output out.csv --currency EUR

Requires: pandas, numpy, requests
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests

API_URL = "https://prices.azure.com/api/retail/prices"
DEFAULT_INPUT = Path("az_regions_annotated.json")
DEFAULT_OUTPUT = Path("block_storage_pricing.csv")

REGION_COLUMN = "Region"
PERFORMANCE_COLUMN = "Performance"
REDUNDANCY_COLUMN = "Redundancy"
PRICE_COLUMN = "PricePerGB"

PERFORMANCE_TIERS = ("Standard HDD", "Standard SSD", "Premium SSD", "Ultra Disk")
REDUNDANCIES = ("LRS", "ZRS")

GIB_PER_TIB_DISK = 1024
HOURS_PER_MONTH = 730

# (performance, redundancy) -> (product, sku, meter, unit, price -> GB/month)
TIERS = {
    ("Standard HDD", "LRS"): (
        "Standard HDD Managed Disks", "S30 LRS", "S30 LRS Disk",
        "1/Month", lambda p: p / GIB_PER_TIB_DISK,
    ),
    ("Standard SSD", "LRS"): (
        "Standard SSD Managed Disks", "E30 LRS", "E30 LRS Disk",
        "1/Month", lambda p: p / GIB_PER_TIB_DISK,
    ),
    ("Standard SSD", "ZRS"): (
        "Standard SSD Managed Disks", "E30 ZRS", "E30 ZRS Disk",
        "1/Month", lambda p: p / GIB_PER_TIB_DISK,
    ),
    ("Premium SSD", "LRS"): (
        "Premium SSD Managed Disks", "P30 LRS", "P30 LRS Disk",
        "1/Month", lambda p: p / GIB_PER_TIB_DISK,
    ),
    ("Premium SSD", "ZRS"): (
        "Premium SSD Managed Disks", "P30 ZRS", "P30 ZRS Disk",
        "1/Month", lambda p: p / GIB_PER_TIB_DISK,
    ),
    ("Ultra Disk", "LRS"): (
        "Ultra Disks", "Ultra LRS", "Ultra LRS Provisioned Capacity",
        "1 GiB/Hour", lambda p: p * HOURS_PER_MONTH,
    ),
}

PRODUCTS = ("Standard HDD Managed Disks", "Standard SSD Managed Disks",
            "Premium SSD Managed Disks", "Ultra Disks")

MAX_RETRIES = 5
TIMEOUT = 60  # seconds
WORKERS = 4

# Be polite: retry on 429/5xx with exponential backoff.
RETRY_STATUS = {429, 500, 502, 503, 504}


def load_regions(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as fh:
        regions = json.load(fh)
    return [r["name"] for r in regions if r.get("type") == "Region"]


def build_filter(region: str) -> str:
    products = " or ".join(f"productName eq '{p}'" for p in PRODUCTS)
    return (f"serviceName eq 'Storage' and armRegionName eq '{region}' "
            f"and ({products})")


def fetch_page(session: requests.Session, url: str) -> dict:
    for attempt in range(MAX_RETRIES):
        try:
            resp = session.get(url, timeout=TIMEOUT)
            if resp.status_code in RETRY_STATUS:
                raise requests.HTTPError(f"HTTP {resp.status_code}")
            resp.raise_for_status()
            return resp.json()
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout):
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("unreachable")


def fetch_region_prices(session: requests.Session, region: str,
                        currency: str) -> dict[tuple[str, str], float]:
    """Return {(performance, redundancy): price per GB per month}."""
    params = f"$filter={requests.utils.quote(build_filter(region))}"
    if currency != "USD":
        params += f"&currencyCode={currency}"
    url = f"{API_URL}?{params}"

    prices: dict[tuple[str, str], float] = {}
    while url:
        page = fetch_page(session, url)
        for item in page.get("Items", []):
            if item.get("type") != "Consumption":
                continue
            for key, (product, sku, meter, unit, convert) in TIERS.items():
                if (item.get("productName") == product
                        and item.get("skuName") == sku
                        and item.get("meterName") == meter
                        and item.get("unitOfMeasure") == unit):
                    prices[key] = convert(float(item["retailPrice"]))
        url = page.get("NextPageLink")
    return prices


def region_matrix(region: str, prices: dict[tuple[str, str], float]) -> list[dict]:
    """Build the (performance, redundancy) cross product for a region."""
    rows = []
    for performance in PERFORMANCE_TIERS:
        for redundancy in REDUNDANCIES:
            rows.append({
                REGION_COLUMN: region,
                PERFORMANCE_COLUMN: performance,
                REDUNDANCY_COLUMN: redundancy,
                PRICE_COLUMN: prices.get((performance, redundancy), np.nan),
            })
    return rows


def fetch_all(regions: list[str], currency: str) -> pd.DataFrame:
    records: list[dict] = []
    failures: list[str] = []
    session = requests.Session()

    def work(region: str) -> list[dict]:
        return region_matrix(region, fetch_region_prices(session, region, currency))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, r): r for r in regions}
        for future in as_completed(futures):
            region = futures[future]
            try:
                records.extend(future.result())
                print(f"fetched {region}")
            except Exception as exc:  # noqa: BLE001 - report and continue
                failures.append(region)
                print(f"WARNING: {region}: {exc}", file=sys.stderr)

    if failures:
        print(f"WARNING: no data for {len(failures)} region(s): "
              f"{', '.join(sorted(failures))}", file=sys.stderr)

    df = pd.DataFrame.from_records(
        records,
        columns=[REGION_COLUMN, PERFORMANCE_COLUMN, REDUNDANCY_COLUMN,
                 PRICE_COLUMN],
    )
    df[PERFORMANCE_COLUMN] = pd.Categorical(df[PERFORMANCE_COLUMN],
                                            categories=PERFORMANCE_TIERS)
    df[REDUNDANCY_COLUMN] = pd.Categorical(df[REDUNDANCY_COLUMN],
                                           categories=REDUNDANCIES)
    df[PRICE_COLUMN] = df[PRICE_COLUMN].astype(float)
    return df.sort_values(
        [REGION_COLUMN, PERFORMANCE_COLUMN, REDUNDANCY_COLUMN]
    ).reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help=f"Azure regions JSON (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"Output CSV file (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--regions", type=str, default=None,
                        help="Comma-separated region names (default: all)")
    parser.add_argument("--currency", type=str, default="USD",
                        help="Price currency code (default: USD)")
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")

    regions = load_regions(args.input)
    if args.regions:
        wanted = [r.strip() for r in args.regions.split(",") if r.strip()]
        unknown = [r for r in wanted if r not in regions]
        if unknown:
            parser.error(f"unknown region(s): {', '.join(unknown)}")
        regions = wanted
    if not regions:
        parser.error("no regions selected")

    df = fetch_all(regions, args.currency.upper())
    df.to_csv(args.output, index=False, na_rep="na")

    total = len(df)
    missing = int(df[PRICE_COLUMN].isna().sum())
    print(f"Wrote {total} rows for {df[REGION_COLUMN].nunique()} region(s) "
          f"to {args.output}")
    print(f"Rows with a price: {total - missing}, rows not offered by Azure: {missing}")
    offered = df[~df[PRICE_COLUMN].isna()]
    if not offered.empty:
        print(f"Price per GB range: {offered[PRICE_COLUMN].min():.5f} - "
              f"{offered[PRICE_COLUMN].max():.5f} {args.currency}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
