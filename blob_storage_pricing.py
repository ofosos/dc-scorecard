#!/usr/bin/env python3
"""Fetch Azure blob storage prices per GB for each region.

Reads ``az_regions_annotated.json`` (Azure region list) and queries the
Azure Retail Prices API (https://prices.azure.com/api/retail/prices) for
block blob storage "Data Stored" meters, then writes a long-format CSV
with one row per (region, access frequency, performance, redundancy):

    Region,AccessFrequency,Performance,Redundancy,PricePerGB

Dimension mapping (Azure does not sell every combination):

- Access frequency:
    Hot Tier     -> "Hot" SKUs
    Cold Tier    -> "Cold" SKUs, falling back to "Cool" where Cold is
                    not offered in a region
    Archive Tier -> "Archive" SKUs
- Performance:
    Standard SSD -> General Block Blob v2 (standard performance,
                    priced per access tier)
    Premium SSD  -> Premium Block Blob (SSD-backed premium storage)
- Redundancy:
    LRS / GRS / ZRS (read-access RA-GRS/RA-GZRS and geo-zone GZRS
                    SKUs are not requested and are skipped)

Cells Azure does not sell are written with an empty price:
- Premium Block Blob is only offered with LRS and ZRS (no GRS).
- Premium Block Blob has no access tiers; its price is listed under
  "Hot Tier" only.
- Archive ZRS is not offered in most regions.

Usage:
    python blob_storage_pricing.py                    # all regions -> blob_storage_pricing.csv
    python blob_storage_pricing.py --regions westeurope,uaenorth
    python blob_storage_pricing.py --output out.csv --currency EUR

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
DEFAULT_OUTPUT = Path("blob_storage_pricing.csv")

REGION_COLUMN = "Region"
ACCESS_COLUMN = "AccessFrequency"
PERFORMANCE_COLUMN = "Performance"
REDUNDANCY_COLUMN = "Redundancy"
PRICE_COLUMN = "PricePerGB"

ACCESS_TIERS = ("Hot Tier", "Cold Tier", "Archive Tier")
PERFORMANCE_TIERS = ("Premium SSD", "Standard SSD")
REDUNDANCIES = ("LRS", "GRS", "ZRS")

# Access tier -> SKU tier names in preference order (fallback last).
TIER_SKUS = {
    "Hot Tier": ("Hot",),
    "Cold Tier": ("Cold", "Cool"),
    "Archive Tier": ("Archive",),
}

# Products in preference order (plain variants before Hierarchical
# Namespace ones, which carry the same data-stored price).
STANDARD_PRODUCTS = (
    "General Block Blob v2",
    "General Block Blob v2 Hierarchical Namespace",
)
PREMIUM_PRODUCTS = (
    "Premium Block Blob",
    "Premium Block Blob v2",
    "Premium Block Blob v2 Hierarchical Namespace",
    "Premium Block Blob Hierarchical Namespace",
)

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
    products = [f"productName eq '{p}'" for p in STANDARD_PRODUCTS + PREMIUM_PRODUCTS]
    return (
        f"serviceName eq 'Storage' and armRegionName eq '{region}' "
        f"and ({' or '.join(products)})"
    )


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
    """Return {(sku tier, redundancy): price per GB} for one region."""
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
            if not item.get("meterName", "").endswith("Data Stored"):
                continue
            if item.get("unitOfMeasure") != "1 GB/Month":
                continue
            if item.get("tierMinimumUnits", 0.0) != 0.0:
                continue
            sku = item.get("skuName", "")
            parts = sku.split()
            if len(parts) != 2:
                continue
            tier, redundancy = parts
            if redundancy not in REDUNDANCIES:
                continue
            product = item.get("productName", "")
            pool = STANDARD_PRODUCTS if product in STANDARD_PRODUCTS else PREMIUM_PRODUCTS
            rank = pool.index(product)
            key = (tier, redundancy)
            current = prices.get(key)
            if current is None or rank < current[0]:
                prices[key] = (rank, float(item["retailPrice"]))
        url = page.get("NextPageLink")
    return {k: v[1] for k, v in prices.items()}


def region_matrix(region: str, prices: dict[tuple[str, str], float]) -> list[dict]:
    """Build the (access, performance, redundancy) cross product for a region."""
    rows = []

    def lookup(tiers: tuple[str, ...], redundancy: str) -> float:
        for tier in tiers:
            if (tier, redundancy) in prices:
                return prices[(tier, redundancy)]
        return np.nan

    for access in ACCESS_TIERS:
        sku_tiers = TIER_SKUS[access]
        for performance in PERFORMANCE_TIERS:
            for redundancy in REDUNDANCIES:
                if performance == "Premium SSD":
                    # Premium Block Blob has no access tiers: price under
                    # Hot Tier only, and no GRS offering.
                    price = (lookup(("Premium",), redundancy)
                             if access == "Hot Tier" else np.nan)
                else:
                    price = lookup(sku_tiers, redundancy)
                rows.append({
                    REGION_COLUMN: region,
                    ACCESS_COLUMN: access,
                    PERFORMANCE_COLUMN: performance,
                    REDUNDANCY_COLUMN: redundancy,
                    PRICE_COLUMN: price,
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
        columns=[REGION_COLUMN, ACCESS_COLUMN, PERFORMANCE_COLUMN,
                 REDUNDANCY_COLUMN, PRICE_COLUMN],
    )
    df[ACCESS_COLUMN] = pd.Categorical(df[ACCESS_COLUMN], categories=ACCESS_TIERS)
    df[PERFORMANCE_COLUMN] = pd.Categorical(df[PERFORMANCE_COLUMN], categories=PERFORMANCE_TIERS)
    df[REDUNDANCY_COLUMN] = pd.Categorical(df[REDUNDANCY_COLUMN], categories=REDUNDANCIES)
    df[PRICE_COLUMN] = df[PRICE_COLUMN].astype(float)
    return df.sort_values(
        [REGION_COLUMN, ACCESS_COLUMN, PERFORMANCE_COLUMN, REDUNDANCY_COLUMN]
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
    df.to_csv(args.output, index=False)

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
