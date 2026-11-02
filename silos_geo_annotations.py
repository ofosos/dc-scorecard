#!/usr/bin/env python3
"""Generate one map annotation file per silo.

Reads silos.json (silo name -> list of Azure region names) and the
annotated Azure regions list, and writes one JSON file per silo
(<silo>.json) in the format of afri.json: a compact array of
{"title", "lat", "lng", "description"} objects with the region's
display name, coordinates and physical location.

Usage:
    python silos_geo_annotations.py [silos.json] [az_regions_annotated.json] [output_dir]
"""

import json
import sys
from pathlib import Path


def build_markers(region_names, regions_by_name):
    """Return the marker list for one silo, in silo region order."""
    markers = []
    missing = []
    for name in region_names:
        region = regions_by_name.get(name)
        if region is None:
            missing.append(name)
            continue
        metadata = region.get("metadata", {})
        markers.append(
            {
                "title": region.get("displayName", name),
                "lat": metadata["latitude"],
                "lng": metadata["longitude"],
                "description": metadata.get("physicalLocation", ""),
            }
        )
    if missing:
        print(f"WARNING: no region info for: {', '.join(missing)}")
    return markers


def main():
    silos_path = sys.argv[1] if len(sys.argv) > 1 else "silos.json"
    regions_path = (
        sys.argv[2] if len(sys.argv) > 2 else "az_regions_annotated.json"
    )
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(".")

    with open(silos_path, "r", encoding="utf-8") as f:
        silos = json.load(f)

    with open(regions_path, "r", encoding="utf-8") as f:
        regions = json.load(f)

    regions_by_name = {region["name"]: region for region in regions}

    output_dir.mkdir(parents=True, exist_ok=True)
    for silo, region_names in silos.items():
        markers = build_markers(region_names, regions_by_name)
        output_path = output_dir / f"{silo}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(markers, f, separators=(",", ":"), ensure_ascii=False)
            f.write("\n")
        print(f"{silo}: {len(markers)} regions -> {output_path}")


if __name__ == "__main__":
    main()
