#!/usr/bin/env python3
"""Compute a datacenter "sweat score" for each Azure region.

Reads ``region_temperatures.json`` (a JSON dictionary mapping each Azure
region's programmatic name to a list of ``["YYYY-MM-DD", tmax]`` daily maximum
temperature pairs, as produced by ``max_temperatures_region.py``) and scores
every day:

    tmax < 35 C            -> 0 points
    35 C <= tmax < 38 C     -> 1 point
    38 C <= tmax < 40 C     -> 2 points
    tmax >= 40 C            -> 4 points

The region's sweat score is the sum of the daily points across all days. The
result is written as a two-column CSV: the region's programmatic name and its
sweat score.

Usage:
    python sweat_score.py                          # region_temperatures.json -> region_temperatures_sweatscore.csv
    python sweat_score.py --input temps.json --output scores.csv

Requires: pandas, numpy
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_INPUT = Path("region_temperatures.json")
DEFAULT_OUTPUT = Path("region_temperatures_sweatscore.csv")

REGION_COLUMN = "Region"
SCORE_COLUMN = "SweatScore"


def daily_sweat_points(temps: np.ndarray) -> np.ndarray:
    """Vectorized daily scoring: <35 -> 0, 35..<38 -> 1, 38..<40 -> 2, >=40 -> 4."""
    points = np.zeros(len(temps), dtype=int)
    points[(temps >= 35) & (temps < 38)] = 1
    points[(temps >= 38) & (temps < 40)] = 2
    points[temps >= 40] = 4
    return points


def sweat_scores(temperatures: dict[str, list]) -> pd.DataFrame:
    """Compute the per-region sweat score from {region: [[date, tmax], ...]} data."""
    records = []
    for region, series in temperatures.items():
        temps = np.asarray([t for _, t in series], dtype=float)
        if np.isnan(temps).any():
            print(f"WARNING: {region}: {int(np.isnan(temps).sum())} missing temperature(s) treated as 0 points",
                  file=sys.stderr)
        points = daily_sweat_points(temps)
        records.append({REGION_COLUMN: region, SCORE_COLUMN: int(points.sum())})
    df = pd.DataFrame.from_records(records, columns=[REGION_COLUMN, SCORE_COLUMN])
    return df.sort_values(REGION_COLUMN).reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help=f"Region temperatures JSON (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"Output CSV file (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")

    with open(args.input, encoding="utf-8") as fh:
        temperatures = json.load(fh)

    if not isinstance(temperatures, dict) or not temperatures:
        parser.error(f"{args.input} does not contain a non-empty region dictionary")

    scores = sweat_scores(temperatures)
    scores.to_csv(args.output, index=False)

    hot = scores[scores[SCORE_COLUMN] > 0]
    print(f"Wrote {len(scores)} regions to {args.output}")
    print(f"Regions with a non-zero sweat score: {len(hot)}")
    if not hot.empty:
        print(hot.sort_values(SCORE_COLUMN, ascending=False).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
