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

Script: `gdacs_region_events.py`


## GED data

Armed conflict.

Script: `ged-analysis.py`

## Requirements

 - Azure CLI
 - Python w/ Pipenv

