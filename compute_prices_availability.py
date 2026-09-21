#!/usr/bin/env python3
"""Availability and retail prices for selected Azure VM instance types.

For every region in az_regions_annotated.json, report for each instance
type (default: Standard_B4ms, Standard_D4s_v3, Standard_E2s_v3,
Standard_F4s_v2):

  - Availability from the Azure Resource SKUs API, queried through the
    Python SDK (azure-mgmt-compute), i.e. the same data source as
    `az vm list-skus --location <region> --size <instance>` but without
    shelling out to the CLI. Requires Azure credentials
    (DefaultAzureCredential: environment variables, managed identity, or
    an existing `az login`) and a subscription id (AZURE_SUBSCRIPTION_ID
    or --subscription-id). Without credentials the availability columns
    are filled with "unknown" and the script still delivers prices.

  - Hourly retail prices (Linux pay-as-you-go and spot) from the public
    Azure Retail Prices API (https://prices.azure.com/api/retail/prices),
    which needs no authentication.

Usage
-----
    python3 compute_prices_availability.py
    python3 compute_prices_availability.py \\
        --regions-file az_regions_annotated.json \\
        --output compute_prices_availability.csv \\
        --instances Standard_B4ms Standard_D4s_v3

Setup
-----
    pip install requests pandas numpy azure-identity azure-mgmt-compute
    export AZURE_SUBSCRIPTION_ID=<subscription-id>   # for availability

Output
------
One row per (region, instance) with region metadata, availability
status/restriction details, and Linux on-demand and spot hourly prices.
"""

import argparse
import json
import logging
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

RETAIL_PRICES_URL = "https://prices.azure.com/api/retail/prices"

DEFAULT_INSTANCES = [
    "Standard_B4ms",
    "Standard_D4s_v3",
    "Standard_E2s_v3",
    "Standard_F4s_v2",
]

log = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Regions
# ----------------------------------------------------------------------
def load_regions(regions_file):
    """Return a DataFrame with one row per region from the annotated JSON."""
    with open(regions_file, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    rows = []
    for region in data:
        metadata = region.get("metadata", {}) or {}
        rows.append(
            {
                "region": region.get("name"),
                "displayName": region.get("displayName"),
                "regionalDisplayName": region.get("regionalDisplayName"),
                "regionCategory": metadata.get("regionCategory"),
                "isoCountryCode": metadata.get("isoCountryCode"),
                "latitude": metadata.get("latitude"),
                "longitude": metadata.get("longitude"),
            }
        )
    return pd.DataFrame(rows)



# ----------------------------------------------------------------------
# Availability (Resource SKUs API via the Python SDK)
# ----------------------------------------------------------------------
def _sku_availability(sku, instance):
    """Summarize one ResourceSku entry as a dict, az vm list-skus style."""
    restrictions = sku.restrictions or []
    blocking = [
        r
        for r in restrictions
        if r.type in ("NotAvailableInRegion", "NotAvailableForSubscription")
    ]
    if not blocking:
        status = "Available"
        restriction_type = restriction_reason = ""
    else:
        status = "Restricted"
        restriction_type = ",".join(sorted({r.type for r in blocking}))
        restriction_reason = "; ".join(
            reason for r in blocking if (reason := getattr(r, "reason_code", ""))
        )
    capacity = sku.capacity
    if capacity is None:
        capacity = np.nan
    return {
        "instance": instance,
        "available": status,
        "restriction_type": restriction_type,
        "restriction_reason": restriction_reason,
        "sku_capacity": capacity,
    }


def fetch_availability(regions, instances, subscription_id):
    """Query the Resource SKUs API for every region.

    Uses azure-identity + azure-mgmt-compute (the Python API behind
    `az vm list-skus --location <region>`).
    """
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from azure.core.exceptions import ClientAuthenticationError

    try:
        credential = DefaultAzureCredential()
        client = ComputeManagementClient(credential, subscription_id)
    except ClientAuthenticationError as exc:
        log.warning("Azure authentication failed, availability unknown: %s", exc)
        return None

    records = []
    for region in regions:
        try:
            skus = client.resource_skus.list(filter=f"location eq '{region}'")
            found = set()
            for sku in skus:
                if sku.name in instances and (
                    not sku.locations or region in (sku.locations or [])
                ):
                    record = {"region": region, **_sku_availability(sku, sku.name)}
                    records.append(record)
                    found.add(sku.name)
            for instance in instances - found:
                records.append(
                    {
                        "region": region,
                        "instance": instance,
                        "available": "NotOffered",
                        "restriction_type": "",
                        "restriction_reason": "",
                        "sku_capacity": np.nan,
                    }
                )
            log.info("availability: %s done (%d/%d instances found)",
                     region, len(found), len(instances))
        except Exception as exc:
            log.warning("availability: %s failed: %s", region, exc)
            for instance in instances:
                records.append(
                    {
                        "region": region,
                        "instance": instance,
                        "available": "unknown",
                        "restriction_type": "",
                        "restriction_reason": str(exc),
                        "sku_capacity": np.nan,
                    }
                )
    return pd.DataFrame(records)


# ----------------------------------------------------------------------
# Prices (public Azure Retail Prices API)
# ----------------------------------------------------------------------
def _get(url, params=None, retries=5):
    for attempt in range(retries):
        response = requests.get(url, params=params, timeout=60)
        if response.status_code in (429, 500, 502, 503, 504):
            wait = 2 ** attempt
            log.warning("retail API %s, retrying in %ds", response.status_code, wait)
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response.json()
    response.raise_for_status()
    raise RuntimeError("unreachable")


def fetch_prices(instances):
    """Return a DataFrame with on-demand and spot prices per (region, sku)."""
    items = []
    for instance in instances:
        flt = (
            f"armSkuName eq '{instance}' and serviceName eq 'Virtual Machines' "
            f"and priceType eq 'Consumption'"
        )
        url, params = RETAIL_PRICES_URL, {"$filter": flt}
        count = 0
        while url:
            page = _get(url, params=params)
            items.extend(page.get("Items", []))
            count += len(page.get("Items", []))
            url = page.get("NextPageLink")
            params = None
        log.info("retail prices: %s -> %d meters", instance, count)

    prices = pd.DataFrame(items)
    if prices.empty:
        return prices

    # Linux meters only; the API duplicates every sku with a Windows variant.
    prices = prices[~prices["productName"].str.contains("Windows", na=False)].copy()

    prices["meter_kind"] = np.where(
        prices["skuName"].str.contains("Spot|Low Priority", regex=True, na=False),
        "spot",
        "ondemand",
    )
    prices["isPrimaryMeterRegion"] = prices["isPrimaryMeterRegion"].astype(bool)

    # Keep the primary meter per (region, sku, kind); take the cheapest
    # among any leftovers (e.g. promo meters) so a region is never doubled.
    prices = prices.sort_values(
        ["isPrimaryMeterRegion", "retailPrice"], ascending=[False, True]
    )
    prices = prices.drop_duplicates(["armRegionName", "armSkuName", "meter_kind"])

    ondemand = prices[prices["meter_kind"] == "ondemand"].rename(
        columns={"retailPrice": "linux_price_hourly"}
    )
    spot = prices[prices["meter_kind"] == "spot"].rename(
        columns={"retailPrice": "spot_price_hourly"}
    )

    merged = ondemand.merge(
        spot[["armRegionName", "armSkuName", "spot_price_hourly"]],
        on=["armRegionName", "armSkuName"],
        how="outer",
    )
    merged = merged.rename(columns={"armRegionName": "region", "armSkuName": "instance"})
    return merged


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--regions-file",
        default="az_regions_annotated.json",
        help="Annotated Azure regions JSON (default: az_regions_annotated.json)",
    )
    parser.add_argument(
        "--output",
        default="compute_prices_availability.csv",
        help="Output CSV (default: compute_prices_availability.csv)",
    )
    parser.add_argument(
        "--instances",
        nargs="+",
        default=DEFAULT_INSTANCES,
        help="Instance types to look up (default: %(default)s)",
    )
    parser.add_argument(
        "--subscription-id",
        default=os.environ.get("AZURE_SUBSCRIPTION_ID"),
        help="Subscription id for availability lookups "
        "(default: AZURE_SUBSCRIPTION_ID)",
    )
    parser.add_argument(
        "--skip-availability",
        action="store_true",
        help="Do not query the Resource SKUs API (prices only)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose logging"
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    regions = load_regions(args.regions_file)
    log.info("loaded %d regions from %s", len(regions), args.regions_file)

    prices = fetch_prices(args.instances)
    if prices.empty:
        log.error("no price data returned by the retail prices API")
        return 1
    log.info("prices for %d (region, instance) combinations", len(prices))

    availability = None
    if not args.skip_availability:
        if args.subscription_id:
            availability = fetch_availability(
                regions["region"], set(args.instances), args.subscription_id
            )
        else:
            log.warning(
                "no subscription id (AZURE_SUBSCRIPTION_ID or --subscription-id), "
                "skipping availability lookup"
            )
    if availability is None:
        availability = pd.DataFrame(
            [
                {
                    "region": region,
                    "instance": instance,
                    "available": "unknown",
                    "restriction_type": "",
                    "restriction_reason": "",
                    "sku_capacity": np.nan,
                }
                for region in regions["region"]
                for instance in args.instances
            ]
        )

    frame = regions.merge(availability, on="region", how="left")
    frame = frame.merge(prices, on=["region", "instance"], how="left")

    frame["available"] = frame["available"].fillna("NoPriceData")
    frame["restriction_type"] = frame["restriction_type"].fillna("")
    frame["restriction_reason"] = frame["restriction_reason"].fillna("")
    frame["sku_capacity"] = pd.to_numeric(frame["sku_capacity"], errors="coerce")
    frame["linux_price_hourly"] = pd.to_numeric(
        frame["linux_price_hourly"], errors="coerce"
    )
    frame["spot_price_hourly"] = pd.to_numeric(
        frame["spot_price_hourly"], errors="coerce"
    )
    frame["spot_discount_pct"] = np.round(
        (1 - frame["spot_price_hourly"] / frame["linux_price_hourly"]) * 100, 1
    )

    columns = [
        "region",
        "displayName",
        "isoCountryCode",
        "regionCategory",
        "instance",
        "available",
        "restriction_type",
        "restriction_reason",
        "sku_capacity",
        "linux_price_hourly",
        "spot_price_hourly",
        "spot_discount_pct",
        "currencyCode",
        "unitOfMeasure",
        "effectiveStartDate",
        "latitude",
        "longitude",
    ]
    columns = [c for c in columns if c in frame.columns]
    frame = frame[columns].sort_values(["region", "instance"])
    frame.to_csv(args.output, index=False)
    log.info("wrote %d rows to %s", len(frame), args.output)

    pivot = frame.pivot_table(
        index="region", columns="instance", values="linux_price_hourly", dropna=False
    )
    with pd.option_context("display.width", 160):
        print(pivot.to_string())

    return 0


if __name__ == "__main__":
    sys.exit(main())
