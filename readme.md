# Readme

## Contents

Scripts included:

 - UCDP GED conflict database
 - Electricity Maps carbon intensity
 - GDACS/USGS natural disasters
 - 

## Azure regions

Table: https://learn.microsoft.com/th-th/azure/reliability/regions-list?tabs=all

Extraction prompt:

```
Extract the azure regions from the following table. Make sure the output is compatible with the json formatted "az account list-locations" output. Include information not given by AZ CLI. Include latitude and longitude for each region.
```

Output: `az_regions.json`

## Azure ISO map

Add ISO two-letter country code to azure regions.

Script: `az_regions_annotate.py`

Output: `az_regions_annotated.json`


## ILO conventions

https://normlex.ilo.org/dyn/nrmlx_en/f?p=NORMLEXPUB:10011:0::NO::P10011_DISPLAY_BY%2CP10011_CONVENTION_TYPE_CODE:1%2CF

Extracted into `ilo-core-conventions.csv`.

## ILO - Azure match

Script: `ilo_analysis.py`



Output: `azure_regions_ilo.csv`

## ITUC Global Rights Index

https://www.ituc-csi.org/the-global-rights-index-explained

Get the global report here: https://www.ituc-csi.org/global-rights-index-reports

Extract with `pdftext`.

Extraction prompt:

```
The txt file contains the full text extract from the 2026 ITUC Global Right Index report. Extract all country ratings. The output format should be a CSV with the Country name, two letter country code, and the rating. Finally explain the meaning and range of the rating column.
```

| Rating | Meaning |
| --- | --- |
| 1 | Sporadic violations of rights |
| 2 | Repeated violations of rights |
| 3 | Regular violations of rights |
| 4 | Systematic violations of rights |
| 5 | No guarantee of rights |
| 5+ | No guarantee of rights due to the breakdown of the rule of law |

## GDACS data

Natural disasters.

API:
https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH

Script: `gdacs_az_regions.py`

The geodata processing uses GeoPandas: event geometries are parsed with
Shapely, each Azure region is buffered into a true WGS84 geodesic circle
(geodesic densification via `pyproj.Geod`, boundary within 100 m of the
exact circle) and events are assigned with a single `geopandas.sjoin`
spatial join (`predicate="intersects"`).

## GED data

Armed conflict.

Script: `ged-analysis.py`

The point/circle intersection and the per-region matching use GeoPandas
spatial joins against WGS84 geodesic circles (geodesic densification via
`pyproj.Geod`); distances are WGS84 geodesic distances (`pyproj.Geod.inv`),
replacing the haversine approximation.

## Azure VM availability and prices

Availability (Resource SKUs API, like `az vm list-skus --location <region> --size <instance>`)
and Linux/spot retail prices (Retail Prices API) for selected instance
types across all regions in `az_regions_annotated.json`. Default
instances: Standard_B4ms, the D series across generations (D4s_v3/v4/
v5/v6, D4_v2, DS4_v2, D4), the E series (E2s_v3/v4/v5/v6, E2_v3; the E
series starts at v3) and the F series (F4s_v2, F4s, F4, plus its
successor FX4mds; the F series ends at v2).

    pip install requests pandas numpy azure-identity azure-mgmt-compute
    export AZURE_SUBSCRIPTION_ID=<subscription-id>
    python3 compute_prices_availability.py

Without Azure credentials the script still returns prices and marks
availability as `unknown`.
## Azure blob storage pricing

Per GB blob storage prices from the Azure Retail Prices API, for the full
(access frequency, performance, redundancy) matrix per region, with
LRS, GRS, ZRS, GZRS, RA-GRS and RA-GZRS redundancy options.

Script: `blob_storage_pricing.py`

Output: `blob_storage_pricing.csv`

## Azure block storage pricing

Per GB managed disk (block storage) prices from the Azure Retail Prices
API, for the full (performance, redundancy) matrix per region:
Standard HDD, Standard SSD, Premium SSD and Ultra Disk, each with LRS
and ZRS. Azure does not publish a per-GB meter for managed disks other
than Ultra Disk, so the per-GB price is derived from the 1 TiB disk
tiers (S30/E30/P30, 1024 GiB) and the Ultra per-GiB/hour capacity
meter (730 h/month). Combinations Azure does not sell (e.g. Standard
HDD ZRS, Ultra Disk ZRS, ZRS in regions without availability zones) are
written as `na`.

Script: `block_storage_pricing.py`

Output: `block_storage_pricing.csv`

## Azure Files pricing

Per GB Azure Files (file share) prices from the Azure Retail Prices
API, for the full (access frequency, performance, redundancy) matrix
per region: Hot, Cool and Transaction Optimized tiers (the SKU tier
the Retail Prices API names "Standard"), Standard HDD and Premium SSD
performance, each with LRS, GRS, ZRS and GZRS. Standard HDD prices
from the "Files v2" share "Data Stored" meters (classic "Files"
product as fallback for LRS/GRS), Premium SSD from the "Premium Files"
provisioned share meters (listed under Hot Tier only, no GRS/GZRS).
Combinations Azure does not sell are written as `na`.

Script: `files_pricing.py`

Output: `files_pricing.csv`

## Pricing summary

Per-offering statistics (top, bottom, median, average, top/bottom decile
price, number of regions including `na`, number of regions with a price,
percentage of regions offered in, and the regions carrying the top and
bottom prices) for the compute, blob, block and Files pricing matrices,
written as one markdown table per offering.

Script: `pricing_summary.py`

Output: `pricing-summary.md`

## Makefile

`make` regenerates all generated CSV/JSON outputs in dependency
order: annotating the Azure regions first, then the per-topic data
files that read it, and finally `pricing-summary.md` from the four
pricing matrices. Each data file has its own make target, so `make
files_pricing.csv` or `make pricing-summary.md` rebuilds just that
file plus its dependencies. `make clean` removes the generated data
files (the 274 MB GED event extract is unzipped to
`GEDEvent_v26_1.csv`, which is git-ignored).

## Requirements

 - Azure CLI
 - Python w/ Pipenv

## Outputs

 - `az_regions_annotated.json` AZ regions with ISO country code and coords
 - `region_temperatures_sweatscore.csv` sweat score (high temps)
 - `ilo_azure_regions.csv` signed ILO core conventions
 - `global_rights_azure_regions.csv` ITUC global rights index
 - `ged-azure.csv` armed conflict data (UU GED)
 - `gdacs_events_by_regions.json` natural disasters
 - `azure_carbon_intensity.csv` carbon intensity
 - `compute_prices_availability.csv` VM availability and prices per region
 - `blob_storage_pricing.csv` blob storage price per GB (tier/performance/redundancy)
 - `block_storage_pricing.csv` block storage (managed disk) price per GB (performance/redundancy)
 - `files_pricing.csv` Azure Files price per GB (performance/redundancy)
 - `pricing-summary.md` per-offering pricing statistics across regions
