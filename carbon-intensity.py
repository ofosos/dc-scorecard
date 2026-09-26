#!/usr/bin/env python3
"""
Fetch grid carbon intensity (gCO2eq/kWh) for Azure datacenter locations
using the Electricity Maps API (v3).

Setup:
  1. Get a free API token: https://www.electricitymaps.com/  (dashboard -> API token)
  2. pip install requests pandas
  3. export EMAPS_TOKEN="your-token"

Notes:
  - Electricity Maps zones are ISO country codes (e.g. "DE") or subnational
    grid zones (e.g. "US-MIDA-PJM", "AU-NSW"). The mapping below pairs each
    Azure region with its most representative grid zone. For countries where
    EM only has country-level data, the country code is used.
  - The token supports the free tier (limited zones/requests); a paid plan
    unlocks all zones and history. If a zone is not in your plan, the script
    reports it as "no access" and continues.
  - Endpoints used (v3):
      GET /v3/carbon-intensity/latest?zone=<zone>
      GET /v3/carbon-intensity/history?zone=<zone>&datetime=...  (optional)
"""

import os
import sys
import time

import pandas as pd
import requests

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

API_BASE = "https://api.electricitymap.org/v3"
TOKEN = os.environ.get("EMAPS_TOKEN")
if not TOKEN:
    sys.exit("Set EMAPS_TOKEN env var to your Electricity Maps API token.")

HEADERS = {"auth-token": TOKEN}
TIMEOUT = 15
RETRY_BACKOFF = [2, 5, 10]          # seconds, on 429/5xx

# Azure region -> Electricity Maps zone.
# Programmatic region name -> (display name, EM zone)
# Adjust zones as needed; see https://www.electricitymaps.com/data-portal
AZURE_TO_EMAPS = {
    # Europe
    "westeurope":         ("West Europe",         "NL"),
    "northeurope":        ("North Europe",        "IE"),
    "germanywestcentral": ("Germany West Central", "DE"),   # Frankfurt
    "germanynorth":       ("Germany North",       "DE"),    # Berlin
    "francecentral":      ("France Central",      "FR"),
    "francesouth":        ("France South",        "FR"),
    "uksouth":            ("UK South",            "GB"),    # GB is whole-grid; England has no separate EM zone
    "ukwest":             ("UK West",             "GB"),
    "swedencentral":      ("Sweden Central",      "SE"),
    "norwayeast":         ("Norway East",         "NO-NO1"),
    "norwaywest":         ("Norway West",         "NO-NO3"),
    "switzerlandnorth":   ("Switzerland North",   "CH"),
    "austriaeast":        ("Austria East",        "AT"),
    "belgiumcentral":     ("Belgium Central",     "BE"),
    "denmarkeast":        ("Denmark East",        "DK-DK1"),
    "polandcentral":      ("Poland Central",      "PL"),
    "italynorth":         ("Italy North",         "IT-NO"),
    "spaincentral":       ("Spain Central",       "ES"),
    "finlandcentral":     ("Finland",             "FI"),
    # Americas
    "eastus":             ("East US",             "US-PJM"),
    "eastus2":            ("East US 2",           "US-MIDA-PJM"),
    "centralus":          ("Central US",          "US-MISO"),
    "northcentralus":     ("North Central US",    "US-MISO"),
    "southcentralus":     ("South Central US",    "US-TEX-ERCO"),
    "westus":             ("West US",             "US-CAL-CISO"),
    "westus2":            ("West US 2",           "US-NW-NWMT"),
    "westus3":            ("West US 3",           "US-SW-AZPS"),
    "canadacentral":      ("Canada Central",      "CA-ON"),
    "canadaeast":         ("Canada East",         "CA-QC"),
    "brazilsouth":        ("Brazil South",        "BR-CS"),
    "mexicocentral":      ("Mexico Central",      "MX-BC"),
    "chilecentral":       ("Chile Central",       "CL-SEN"),
    # Middle East & Africa
    "israelcentral":      ("Israel Central",      "IL"),
    "uaenorth":           ("UAE North",           "AE"),
    "qatarcentral":       ("Qatar Central",       "QA"),
    "southafricanorth":   ("South Africa North",  "ZA"),
    # Asia Pacific
    "southeastasia":      ("Southeast Asia",     "SG"),
    "eastasia":           ("East Asia",          "HK"),
    "japaneast":          ("Japan East",         "JP-TK"),
    "japanwest":          ("Japan West",         "JP-KN"),
    "koreacentral":       ("Korea Central",      "KR"),
    "centralindia":       ("Central India",      "IN-SO"),
    "southindia":         ("South India",        "IN-SO"),
    "westindia":          ("West India",         "IN-WE"),
    "indiasouthcentral":  ("India South Central","IN-SO"),
    "australiaeast":      ("Australia East",     "AU-NSW"),
    "australiasoutheast": ("Australia Southeast","AU-VIC"),
    "newzealandnorth":    ("New Zealand North",  "NZ"),
    "indonesiacentral":   ("Indonesia Central",  "ID"),
    "malaysiawest":       ("Malaysia West",      "MY"),
}

# ----------------------------------------------------------------------
# API helpers
# ----------------------------------------------------------------------

def _get(url, params=None):
    """GET with simple retry/backoff on 429 and 5xx."""
    for attempt, backoff in enumerate([0] + RETRY_BACKOFF):
        if backoff:
            time.sleep(backoff)
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503):
                continue
            return {"error": f"HTTP {r.status_code}", "detail": r.text[:200]}
        except requests.RequestException as e:
            if attempt == len(RETRY_BACKOFF):
                return {"error": str(e)}
    return {"error": "retries exhausted"}

def latest_intensity(zone: str):
    """Latest carbon intensity for a zone. Returns dict with value or error."""
    data = _get(f"{API_BASE}/carbon-intensity/latest", {"zone": zone})
    if "error" in data:
        return {"zone": zone, "error": data["error"]}
    ci = data.get("carbonIntensity")
    return {
        "zone": zone,
        "carbon_intensity": ci,
        "datetime": data.get("datetime"),
        "updated_at": data.get("updatedAt"),
        "emission_factor_type": data.get("emissionFactorType"),
    }

def history_intensity(zone: str, hours: int = 24):
    """Past N hours of carbon intensity (for averaging)."""
    data = _get(f"{API_BASE}/carbon-intensity/history", {"zone": zone})
    if "error" in data or "history" not in data:
        return []
    hist = data["history"][-hours:] if hours else data["history"]
    return [(h.get("datetime"), h.get("carbonIntensity")) for h in hist]

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def fetch_24h_average(zone: str):
    """Simple mean of the last 24 hourly values (smoother than a snapshot)."""
    hist = history_intensity(zone, hours=24)
    vals = [v for _, v in hist if v is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)

def main():
    rows = []
    for prog_name, (display, zone) in AZURE_TO_EMAPS.items():
        print(f"Fetching {display:25s} -> zone {zone} ...", end=" ")
        latest = latest_intensity(zone)
        avg24 = fetch_24h_average(zone) if "error" not in latest else None
        rows.append({
            "region": prog_name,
            "display_name": display,
            "emaps_zone": zone,
            "carbon_intensity_now": latest.get("carbon_intensity"),
            "carbon_intensity_avg24h": round(avg24, 1) if avg24 else None,
            "datetime": latest.get("datetime"),
            "error": latest.get("error"),
        })
        print("ok" if "error" not in latest else f"FAILED ({latest['error']})")
        time.sleep(1)   # be nice to the API / free-tier rate limits

    df = pd.DataFrame(rows)
    ok = df[df["carbon_intensity_now"].notna()].sort_values("carbon_intensity_now")
    fail = df[df["carbon_intensity_now"].isna()]

    print("\n=== Azure regions by current grid carbon intensity (gCO2eq/kWh) ===")
    if not ok.empty:
        print(ok[["region", "display_name", "emaps_zone",
                  "carbon_intensity_now", "carbon_intensity_avg24h"]].to_string(index=False))
    if not fail.empty:
        print("\nNo data (check zone mapping or API plan access):")
        print(fail[["region", "emaps_zone", "error"]].to_string(index=False))

    df.to_csv("azure_carbon_intensity.csv", index=False)
    print("\nWrote: azure_carbon_intensity.csv")

if __name__ == "__main__":
    main()