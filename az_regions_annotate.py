#!/usr/bin/env python3
"""Annotate az_regions.json with two-letter ISO country codes.

Reads az_regions.json, adds an `isoCountryCode` field to each region's
metadata, and writes the result to az_regions_annotated.json.

Usage:
    python annotate_az_regions.py [input.json] [output.json]
"""

import json
import sys

# Explicit mapping of Azure region names to ISO 3166-1 alpha-2 codes.
# Regions without a single clear country (e.g. multi-country geographies
# like Europe/Asia Pacific) are mapped to the country of their physical
# datacenter location.
REGION_TO_ISO = {
    "australiacentral": "AU",
    "australiacentral2": "AU",
    "australiaeast": "AU",
    "australiasoutheast": "AU",
    "austriaeast": "AT",
    "belgiumcentral": "BE",
    "brazilsouth": "BR",
    "brazilsoutheast": "BR",
    "canadacentral": "CA",
    "canadaeast": "CA",
    "centralindia": "IN",
    "centralus": "US",
    "chilecentral": "CL",
    "denmarkeast": "DK",
    "eastasia": "HK",       # Hong Kong
    "eastus": "US",
    "eastus2": "US",
    "francecentral": "FR",
    "francesouth": "FR",
    "germanynorth": "DE",
    "germanywestcentral": "DE",
    "indiasouthcentral": "IN",
    "indonesiacentral": "ID",
    "israelcentral": "IL",
    "italynorth": "IT",
    "japaneast": "JP",
    "japanwest": "JP",
    "koreacentral": "KR",
    "koreasouth": "KR",
    "malaysiawest": "MY",
    "mexicocentral": "MX",
    "newzealandnorth": "NZ",
    "northcentralus": "US",
    "northeurope": "IE",    # Ireland
    "norwayeast": "NO",
    "norwaywest": "NO",
    "polandcentral": "PL",
    "qatarcentral": "QA",
    "southafricanorth": "ZA",
    "southafricawest": "ZA",
    "southcentralus": "US",
    "southindia": "IN",
    "southeastasia": "SG",  # Singapore
    "spaincentral": "ES",
    "swedencentral": "SE",
    "swedensouth": "SE",
    "switzerlandnorth": "CH",
    "switzerlandwest": "CH",
    "uaecentral": "AE",
    "uaenorth": "AE",
    "uksouth": "GB",
    "ukwest": "GB",
    "westcentralus": "US",
    "westeurope": "NL",     # Netherlands
    "westindia": "IN",
    "westus": "US",
    "westus2": "US",
    "westus3": "US",
}

# Fallback mapping by geographyGroup for regions not in the explicit map.
GEOGRAPHY_TO_ISO = {
    "Australia": "AU",
    "Austria": "AT",
    "Belgium": "BE",
    "Brazil": "BR",
    "Canada": "CA",
    "Chile": "CL",
    "Denmark": "DK",
    "France": "FR",
    "Germany": "DE",
    "India": "IN",
    "Indonesia": "ID",
    "Israel": "IL",
    "Italy": "IT",
    "Japan": "JP",
    "Korea": "KR",
    "Malaysia": "MY",
    "Mexico": "MX",
    "New Zealand": "NZ",
    "Norway": "NO",
    "Poland": "PL",
    "Qatar": "QA",
    "South Africa": "ZA",
    "Spain": "ES",
    "Sweden": "SE",
    "Switzerland": "CH",
    "UAE": "AE",
    "United Kingdom": "GB",
    "United States": "US",
    # Multi-country geographies: mapped by physical datacenter location
    # (Ireland / Netherlands / Hong Kong / Singapore) via the explicit map.
    "Europe": None,
    "Asia Pacific": None,
}


def annotate(regions):
    """Return a new list of regions with isoCountryCode added to metadata."""
    annotated = []
    missing = []
    for region in regions:
        name = region["name"]
        metadata = dict(region.get("metadata", {}))
        code = REGION_TO_ISO.get(name)
        if code is None:
            code = GEOGRAPHY_TO_ISO.get(metadata.get("geographyGroup"))
        if code is None:
            missing.append(name)
        else:
            metadata["isoCountryCode"] = code
        annotated.append({**region, "metadata": metadata})
    if missing:
        print(f"WARNING: no ISO code found for: {', '.join(missing)}")
    return annotated


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "az_regions.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "az_regions_annotated.json"

    with open(input_path, "r", encoding="utf-8") as f:
        regions = json.load(f)

    annotated = annotate(regions)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(annotated, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = len(annotated)
    tagged = sum(
        1 for r in annotated if "isoCountryCode" in r.get("metadata", {})
    )
    print(f"Annotated {tagged}/{total} regions -> {output_path}")


if __name__ == "__main__":
    main()