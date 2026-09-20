import json

import numpy as np
import pandas as pd

# Input files
AZ_REGIONS_FILE = "az_regions_annotated.json"
RIGHTS_INDEX_FILE = "global-rights-index.csv"
OUTPUT_FILE = "global_rights_azure_regions.csv"


def main() -> None:
    # Load the annotated Azure regions JSON
    with open(AZ_REGIONS_FILE, "r", encoding="utf-8") as f:
        regions_raw = json.load(f)

    # Flatten the nested region metadata into a flat DataFrame
    regions = pd.json_normalize(regions_raw)

    # Keep the region name and pull the ISO country code out of metadata
    regions = regions[["name", "metadata.isoCountryCode"]]
    regions = regions.rename(
        columns={"name": "Region", "metadata.isoCountryCode": "Country_Code"}
    )

    # Load the Global Rights Index CSV
    rights = pd.read_csv(RIGHTS_INDEX_FILE)

    # Merge on the two-letter ISO country code (left join keeps every Azure region)
    merged = regions.merge(rights, on="Country_Code", how="left")

    # Report any regions whose country had no rights-index entry
    missing = merged[merged["Country"].isna()]
    if not missing.empty:
        print("Regions without a rights-index match:")
        print(missing[["Region", "Country_Code"]].to_string(index=False))

    # Convert Rating to numeric for convenience where possible (5+ stays as-is otherwise)
    merged["Rating"] = merged["Rating"].astype(str)

    # Write the result
    merged.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(merged)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()