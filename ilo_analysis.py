"""
Merge Azure region metadata with ILO core conventions data.

Reads:
  - az_regions_annotated.json : Azure regions with metadata (incl. isoCountryCode)
  - ilo-core-conventions.csv  : ILO core convention ratification years by country

Writes:
  - ilo_azure_regions.csv : one row per Azure region, with the region's
    ISO country code and all corresponding ILO columns (left join).
"""

import json

import numpy as np
import pandas as pd

AZ_JSON = "az_regions_annotated.json"
ILO_CSV = "ilo-core-conventions.csv"
OUTPUT_CSV = "ilo_azure_regions.csv"

# --- Load Azure regions -------------------------------------------------
with open(AZ_JSON, "r", encoding="utf-8") as f:
    az_raw = pd.json_normalize(json.load(f))

# Flatten the nested metadata columns into simple names
az = az_raw.rename(columns=lambda c: c.replace("metadata.", ""))

# Keep the useful region fields
az_regions = az[
    [
        "name",
        "displayName",
        "regionalDisplayName",
        "regionType",
        "regionCategory",
        "geographyGroup",
        "geography",
        "physicalLocation",
        "latitude",
        "longitude",
        "availabilityZoneSupport",
        "accessRestriction",
        "isoCountryCode",
    ]
].copy()

az_regions["isoCountryCode"] = az_regions["isoCountryCode"].replace("", np.nan)

# --- Load ILO conventions ------------------------------------------------
ilo = pd.read_csv(ILO_CSV, dtype={"country_iso": str})

# --- Merge on two-letter ISO country code --------------------------------
merged = az_regions.merge(
    ilo,
    how="left",
    left_on="isoCountryCode",
    right_on="country_iso",
    validate="many_to_one",
)

# country_iso is redundant with isoCountryCode after the merge
merged = merged.drop(columns=["country_iso"])

# --- Write output ---------------------------------------------------------
merged.to_csv(OUTPUT_CSV, index=False)

print(f"Wrote {len(merged)} rows to {OUTPUT_CSV}")