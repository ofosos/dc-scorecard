PYTHON ?= python3

.DELETE_ON_ERROR:

.PHONY: all clean

all: az_regions_annotated.json \
     ilo_azure_regions.csv \
     global_rights_azure_regions.csv \
     ged-azure.csv ged-azure-agg.csv \
     gdacs_events_by_region.json \
     region_temperatures.json \
     region_temperatures_sweatscore.csv \
     compute_prices_availability.csv \
     blob_storage_pricing.csv \
     block_storage_pricing.csv \
     files_pricing.csv \
     pricing-summary.md

az_regions_annotated.json: az_regions_annotate.py az_regions.json
	$(PYTHON) az_regions_annotate.py

ilo_azure_regions.csv: ilo_analysis.py az_regions_annotated.json ilo-core-conventions.csv
	$(PYTHON) ilo_analysis.py

global_rights_azure_regions.csv: global-rights-index-merge-azure.py az_regions_annotated.json global-rights-index.csv
	$(PYTHON) global-rights-index-merge-azure.py

GEDEvent_v26_1.csv: ged261-csv.zip
	$(PYTHON) -m zipfile -e ged261-csv.zip .

ged-azure.csv ged-azure-agg.csv &: ged-analysis.py GEDEvent_v26_1.csv az_regions.json
	$(PYTHON) ged-analysis.py

gdacs_events_by_region.json: gdacs_az_regions.py az_regions_annotated.json
	$(PYTHON) gdacs_az_regions.py

region_temperatures.json: max_temperatures_region.py az_regions_annotated.json
	$(PYTHON) max_temperatures_region.py

region_temperatures_sweatscore.csv: sweat_score.py region_temperatures.json
	$(PYTHON) sweat_score.py

compute_prices_availability.csv: compute_prices_availability.py az_regions_annotated.json
	$(PYTHON) compute_prices_availability.py

blob_storage_pricing.csv: blob_storage_pricing.py az_regions_annotated.json
	$(PYTHON) blob_storage_pricing.py

block_storage_pricing.csv: block_storage_pricing.py az_regions_annotated.json
	$(PYTHON) block_storage_pricing.py

files_pricing.csv: files_pricing.py az_regions_annotated.json
	$(PYTHON) files_pricing.py

pricing-summary.md: pricing_summary.py compute_prices_availability.csv blob_storage_pricing.csv block_storage_pricing.csv files_pricing.csv
	$(PYTHON) pricing_summary.py

azure_carbon_intensity.csv: carbon-intensity.py
	$(PYTHON) carbon-intensity.py

clean:
	rm -f az_regions_annotated.json \
	      ilo_azure_regions.csv \
	      global_rights_azure_regions.csv \
	      GEDEvent_v26_1.csv \
	      ged-azure.csv \
	      ged-azure-agg.csv \
	      gdacs_events_by_region.json \
	      gdacs_events_by_region.json.error.log \
	      region_temperatures.json \
	      region_temperatures_sweatscore.csv \
	      compute_prices_availability.csv \
	      blob_storage_pricing.csv \
	      block_storage_pricing.csv \
	      files_pricing.csv \
	      pricing-summary.md \
	      azure_carbon_intensity.csv
