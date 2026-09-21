#!/usr/bin/env python3
"""Summarize the Azure pricing matrices into a markdown report.

Loads the four pricing CSVs produced by the sibling scripts:

- ``compute_prices_availability.csv``  (VM hourly prices per instance)
- ``blob_storage_pricing.csv``         (blob price per GB)
- ``block_storage_pricing.csv``        (managed disk price per GB)
- ``files_pricing.csv``                (Azure Files price per GB)

Each file has one row per region per service offering, where an offering
is identified by a tuple of dimensions (instance type, or access
frequency/performance/redundancy combinations).  Cells Azure does not
sell are ``na`` (the compute file leaves them empty).

For every offering the report shows top, bottom, median and average
price, the top and bottom decile prices, the number of regions
(including ``na`` rows), the number of regions with a price (excluding
``na``), the percentage of regions the offering is available in, and the
regions carrying the top and bottom prices.

Usage:
    python pricing_summary.py                    # writes pricing-summary.md
    python pricing_summary.py --output out.md

Requires: pandas, numpy
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_OUTPUT = Path("pricing-summary.md")
NA = "na"
MAX_REGIONS_LISTED = 12

SERVICES = (
    {
        "title": "Compute (virtual machines)",
        "file": "compute_prices_availability.csv",
        "region": "region",
        "dims": ("instance",),
        "prices": (
            ("linux_price_hourly", "Linux on-demand", "USD/hour"),
            ("spot_price_hourly", "Spot", "USD/hour"),
        ),
    },
    {
        "title": "Blob storage",
        "file": "blob_storage_pricing.csv",
        "region": "Region",
        "dims": ("AccessFrequency", "Performance", "Redundancy"),
        "prices": (("PricePerGB", "", "USD/GB/month"),),
    },
    {
        "title": "Block storage (managed disks)",
        "file": "block_storage_pricing.csv",
        "region": "Region",
        "dims": ("Performance", "Redundancy"),
        "prices": (("PricePerGB", "", "USD/GB/month"),),
    },
    {
        "title": "Azure Files",
        "file": "files_pricing.csv",
        "region": "Region",
        "dims": ("AccessFrequency", "Performance", "Redundancy"),
        "prices": (("PricePerGB", "", "USD/GB/month"),),
    },
)


def load_offering_frames(service: dict) -> list[pd.DataFrame]:
    """Return one long-format frame per price column of a service.

    Columns: offering (label string), region, price (float, NaN for na).
    """
    df = pd.read_csv(service["file"], dtype=str, keep_default_na=False)
    frames = []
    for column, label, _unit in service["prices"]:
        parts = [df[dim] for dim in service["dims"]]
        if label:
            parts.append(pd.Series([label] * len(df), index=df.index))
        offering = parts[0].str.cat(parts[1:], sep=" / ")
        price = pd.to_numeric(
            df[column].where(df[column].str.lower() != NA).replace("", NA),
            errors="coerce",
        )
        frames.append(
            pd.DataFrame(
                {
                    "offering": offering,
                    "region": df[service["region"]],
                    "price": price,
                }
            )
        )
    return frames


def fmt_regions(regions: list[str]) -> str:
    listed = ", ".join(sorted(regions[:MAX_REGIONS_LISTED]))
    if len(regions) > MAX_REGIONS_LISTED:
        listed += f" (+{len(regions) - MAX_REGIONS_LISTED} more)"
    return listed or "—"


def offering_table(frame: pd.DataFrame, unit: str) -> str:
    prices = frame["price"]
    offered = prices.dropna()
    n_regions = len(frame)

    def price_row(stat: str, value: float | None) -> str:
        shown = "n/a" if value is None or np.isnan(value) else f"{value:.6g}"
        return f"| {stat} | {shown} | |"

    def price_row_regions(stat: str, value: float | None, regions: list[str]) -> str:
        shown = "n/a" if value is None or np.isnan(value) else f"{value:.6g}"
        return f"| {stat} | {shown} | {fmt_regions(regions)} |"

    lines = [
        "| Statistic | Price/Count | Regions |",
        "| --- | --- | --- |",
    ]
    if offered.empty:
        lines.append("| Not offered in any region | | |")
        lines.append(f"| Number of regions (incl. na) | {n_regions} | |")
        lines.append("| Number of regions with a price | 0 | |")
        lines.append("| Offered in | 0.0% of regions | |")
        return "\n".join(lines)

    top = offered.max()
    bottom = offered.min()
    top_regions = frame.loc[prices == top, "region"].tolist()
    bottom_regions = frame.loc[prices == bottom, "region"].tolist()
    p90 = np.percentile(offered, 90)
    p10 = np.percentile(offered, 10)
    top_decile_regions = frame.loc[prices >= p90, "region"].tolist()
    bottom_decile_regions = frame.loc[prices <= p10, "region"].tolist()

    lines.append(price_row_regions("Top price", top, top_regions))
    lines.append(price_row_regions("Bottom price", bottom, bottom_regions))
    lines.append(price_row("Median price", float(np.median(offered))))
    lines.append(price_row("Average price", float(offered.mean())))
    lines.append(price_row_regions("Top decile price (P90)", p90, top_decile_regions))
    lines.append(price_row_regions("Bottom decile price (P10)", p10, bottom_decile_regions))
    lines.append(f"| Number of regions (incl. na) | {n_regions} | |")
    lines.append(f"| Number of regions with a price | {len(offered)} | |")
    lines.append(
        f"| Offered in | {100.0 * len(offered) / n_regions:.1f}% of regions | |"
    )
    lines.append(f"| Unit | {unit} | |")
    return "\n".join(lines)


def build_report() -> str:
    out: list[str] = [
        "# Azure pricing summary",
        "",
        "Per-offering price statistics across all Azure regions, computed",
        "from `compute_prices_availability.csv`, `blob_storage_pricing.csv`,",
        "`block_storage_pricing.csv` and `files_pricing.csv`. Rows Azure does",
        "not sell are `na`; the number of regions includes them, the number",
        "of offerings excludes them.",
        "",
    ]
    for service in SERVICES:
        unit = service["prices"][0][2]
        out.append(f"## {service['title']}")
        out.append("")
        for frame in load_offering_frames(service):
            for offering, group in frame.groupby("offering", sort=True):
                out.append(f"### {offering}")
                out.append("")
                out.append(offering_table(group, unit))
                out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize the Azure pricing CSVs into a markdown report."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output markdown file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    report = build_report()
    args.output.write_text(report)
    n_offering_sections = report.count("\n### ")
    print(f"Wrote {args.output} with {n_offering_sections} offering summaries.")


if __name__ == "__main__":
    main()
