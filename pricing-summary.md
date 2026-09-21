# Azure pricing summary

Per-offering price statistics across all Azure regions, computed
from `compute_prices_availability.csv`, `blob_storage_pricing.csv`,
`block_storage_pricing.csv` and `files_pricing.csv`. Rows Azure does
not sell are `na`; the number of regions includes them, the number
of offerings excludes them.

## Contents

Table of contents entries marked with a degree symbol (°) are
offerings available in 100% of regions.

- [Compute (virtual machines)](#compute-virtual-machines)
  - [Standard_B4ms / Linux on-demand](#standard_b4ms--linux-on-demand)
  - [Standard_D4 / Linux on-demand](#standard_d4--linux-on-demand)
  - [Standard_D4_v2 / Linux on-demand](#standard_d4_v2--linux-on-demand)
  - [Standard_D4s_v3 / Linux on-demand](#standard_d4s_v3--linux-on-demand)
  - [Standard_D4s_v4 / Linux on-demand](#standard_d4s_v4--linux-on-demand) °
  - [Standard_D4s_v5 / Linux on-demand](#standard_d4s_v5--linux-on-demand) °
  - [Standard_D4s_v6 / Linux on-demand](#standard_d4s_v6--linux-on-demand)
  - [Standard_DS4_v2 / Linux on-demand](#standard_ds4_v2--linux-on-demand)
  - [Standard_E2_v3 / Linux on-demand](#standard_e2_v3--linux-on-demand)
  - [Standard_E2s_v3 / Linux on-demand](#standard_e2s_v3--linux-on-demand)
  - [Standard_E2s_v4 / Linux on-demand](#standard_e2s_v4--linux-on-demand) °
  - [Standard_E2s_v5 / Linux on-demand](#standard_e2s_v5--linux-on-demand) °
  - [Standard_E2s_v6 / Linux on-demand](#standard_e2s_v6--linux-on-demand) °
  - [Standard_F4 / Linux on-demand](#standard_f4--linux-on-demand)
  - [Standard_F4s / Linux on-demand](#standard_f4s--linux-on-demand)
  - [Standard_F4s_v2 / Linux on-demand](#standard_f4s_v2--linux-on-demand)
  - [Standard_FX4mds / Linux on-demand](#standard_fx4mds--linux-on-demand)
  - [Standard_B4ms / Spot](#standard_b4ms--spot)
  - [Standard_D4 / Spot](#standard_d4--spot)
  - [Standard_D4_v2 / Spot](#standard_d4_v2--spot)
  - [Standard_D4s_v3 / Spot](#standard_d4s_v3--spot)
  - [Standard_D4s_v4 / Spot](#standard_d4s_v4--spot) °
  - [Standard_D4s_v5 / Spot](#standard_d4s_v5--spot) °
  - [Standard_D4s_v6 / Spot](#standard_d4s_v6--spot)
  - [Standard_DS4_v2 / Spot](#standard_ds4_v2--spot)
  - [Standard_E2_v3 / Spot](#standard_e2_v3--spot)
  - [Standard_E2s_v3 / Spot](#standard_e2s_v3--spot)
  - [Standard_E2s_v4 / Spot](#standard_e2s_v4--spot) °
  - [Standard_E2s_v5 / Spot](#standard_e2s_v5--spot) °
  - [Standard_E2s_v6 / Spot](#standard_e2s_v6--spot) °
  - [Standard_F4 / Spot](#standard_f4--spot)
  - [Standard_F4s / Spot](#standard_f4s--spot)
  - [Standard_F4s_v2 / Spot](#standard_f4s_v2--spot)
  - [Standard_FX4mds / Spot](#standard_fx4mds--spot)
- [Blob storage](#blob-storage)
  - [Archive Tier / Premium SSD / GRS](#archive-tier--premium-ssd--grs)
  - [Archive Tier / Premium SSD / GZRS](#archive-tier--premium-ssd--gzrs)
  - [Archive Tier / Premium SSD / LRS](#archive-tier--premium-ssd--lrs)
  - [Archive Tier / Premium SSD / RA-GRS](#archive-tier--premium-ssd--ra-grs)
  - [Archive Tier / Premium SSD / RA-GZRS](#archive-tier--premium-ssd--ra-gzrs)
  - [Archive Tier / Premium SSD / ZRS](#archive-tier--premium-ssd--zrs)
  - [Archive Tier / Standard SSD / GRS](#archive-tier--standard-ssd--grs)
  - [Archive Tier / Standard SSD / GZRS](#archive-tier--standard-ssd--gzrs)
  - [Archive Tier / Standard SSD / LRS](#archive-tier--standard-ssd--lrs)
  - [Archive Tier / Standard SSD / RA-GRS](#archive-tier--standard-ssd--ra-grs)
  - [Archive Tier / Standard SSD / RA-GZRS](#archive-tier--standard-ssd--ra-gzrs)
  - [Archive Tier / Standard SSD / ZRS](#archive-tier--standard-ssd--zrs)
  - [Cold Tier / Premium SSD / GRS](#cold-tier--premium-ssd--grs)
  - [Cold Tier / Premium SSD / GZRS](#cold-tier--premium-ssd--gzrs)
  - [Cold Tier / Premium SSD / LRS](#cold-tier--premium-ssd--lrs)
  - [Cold Tier / Premium SSD / RA-GRS](#cold-tier--premium-ssd--ra-grs)
  - [Cold Tier / Premium SSD / RA-GZRS](#cold-tier--premium-ssd--ra-gzrs)
  - [Cold Tier / Premium SSD / ZRS](#cold-tier--premium-ssd--zrs)
  - [Cold Tier / Standard SSD / GRS](#cold-tier--standard-ssd--grs)
  - [Cold Tier / Standard SSD / GZRS](#cold-tier--standard-ssd--gzrs)
  - [Cold Tier / Standard SSD / LRS](#cold-tier--standard-ssd--lrs) °
  - [Cold Tier / Standard SSD / RA-GRS](#cold-tier--standard-ssd--ra-grs)
  - [Cold Tier / Standard SSD / RA-GZRS](#cold-tier--standard-ssd--ra-gzrs)
  - [Cold Tier / Standard SSD / ZRS](#cold-tier--standard-ssd--zrs)
  - [Hot Tier / Premium SSD / GRS](#hot-tier--premium-ssd--grs)
  - [Hot Tier / Premium SSD / GZRS](#hot-tier--premium-ssd--gzrs)
  - [Hot Tier / Premium SSD / LRS](#hot-tier--premium-ssd--lrs) °
  - [Hot Tier / Premium SSD / RA-GRS](#hot-tier--premium-ssd--ra-grs)
  - [Hot Tier / Premium SSD / RA-GZRS](#hot-tier--premium-ssd--ra-gzrs)
  - [Hot Tier / Premium SSD / ZRS](#hot-tier--premium-ssd--zrs)
  - [Hot Tier / Standard SSD / GRS](#hot-tier--standard-ssd--grs)
  - [Hot Tier / Standard SSD / GZRS](#hot-tier--standard-ssd--gzrs)
  - [Hot Tier / Standard SSD / LRS](#hot-tier--standard-ssd--lrs) °
  - [Hot Tier / Standard SSD / RA-GRS](#hot-tier--standard-ssd--ra-grs)
  - [Hot Tier / Standard SSD / RA-GZRS](#hot-tier--standard-ssd--ra-gzrs)
  - [Hot Tier / Standard SSD / ZRS](#hot-tier--standard-ssd--zrs)
- [Block storage (managed disks)](#block-storage-managed-disks)
  - [Premium SSD / LRS](#premium-ssd--lrs) °
  - [Premium SSD / ZRS](#premium-ssd--zrs)
  - [Standard HDD / LRS](#standard-hdd--lrs) °
  - [Standard HDD / ZRS](#standard-hdd--zrs)
  - [Standard SSD / LRS](#standard-ssd--lrs) °
  - [Standard SSD / ZRS](#standard-ssd--zrs)
  - [Ultra Disk / LRS](#ultra-disk--lrs)
  - [Ultra Disk / ZRS](#ultra-disk--zrs)
- [Azure Files](#azure-files)
  - [Cool Tier / Premium SSD / GRS](#cool-tier--premium-ssd--grs)
  - [Cool Tier / Premium SSD / GZRS](#cool-tier--premium-ssd--gzrs)
  - [Cool Tier / Premium SSD / LRS](#cool-tier--premium-ssd--lrs)
  - [Cool Tier / Premium SSD / ZRS](#cool-tier--premium-ssd--zrs)
  - [Cool Tier / Standard HDD / GRS](#cool-tier--standard-hdd--grs)
  - [Cool Tier / Standard HDD / GZRS](#cool-tier--standard-hdd--gzrs)
  - [Cool Tier / Standard HDD / LRS](#cool-tier--standard-hdd--lrs) °
  - [Cool Tier / Standard HDD / ZRS](#cool-tier--standard-hdd--zrs)
  - [Hot Tier / Premium SSD / GRS](#hot-tier--premium-ssd--grs-1)
  - [Hot Tier / Premium SSD / GZRS](#hot-tier--premium-ssd--gzrs-1)
  - [Hot Tier / Premium SSD / LRS](#hot-tier--premium-ssd--lrs-1) °
  - [Hot Tier / Premium SSD / ZRS](#hot-tier--premium-ssd--zrs-1)
  - [Hot Tier / Standard HDD / GRS](#hot-tier--standard-hdd--grs)
  - [Hot Tier / Standard HDD / GZRS](#hot-tier--standard-hdd--gzrs)
  - [Hot Tier / Standard HDD / LRS](#hot-tier--standard-hdd--lrs) °
  - [Hot Tier / Standard HDD / ZRS](#hot-tier--standard-hdd--zrs)
  - [Standard Tier / Premium SSD / GRS](#standard-tier--premium-ssd--grs)
  - [Standard Tier / Premium SSD / GZRS](#standard-tier--premium-ssd--gzrs)
  - [Standard Tier / Premium SSD / LRS](#standard-tier--premium-ssd--lrs)
  - [Standard Tier / Premium SSD / ZRS](#standard-tier--premium-ssd--zrs)
  - [Standard Tier / Standard HDD / GRS](#standard-tier--standard-hdd--grs)
  - [Standard Tier / Standard HDD / GZRS](#standard-tier--standard-hdd--gzrs)
  - [Standard Tier / Standard HDD / LRS](#standard-tier--standard-hdd--lrs) °
  - [Standard Tier / Standard HDD / ZRS](#standard-tier--standard-hdd--zrs)

## Compute (virtual machines)

### Standard_B4ms / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.349 | brazilsoutheast |
| Bottom price | 0.166 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.2 | |
| Average price | 0.209635 | |
| Top decile price (P90) | 0.2614 | brazilsouth, brazilsoutheast, francesouth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.1754 | eastus, eastus2, northcentralus, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_D4 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.988 | brazilsoutheast |
| Bottom price | 0.536 | eastus2, southcentralus |
| Median price | 0.678 | |
| Average price | 0.70429 | |
| Top decile price (P90) | 0.883 | brazilsoutheast, eastasia, japaneast, southafricawest |
| Bottom decile price (P10) | 0.564 | centralindia, eastus2, southcentralus, westindia |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 31 | |
| Offered in | 54.4% of regions | |
| Unit | USD/hour | |

### Standard_D4_v2 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.912 | francesouth |
| Bottom price | 0.458 | eastus2, westus2, westus3 |
| Median price | 0.5982 | |
| Average price | 0.630758 | |
| Top decile price (P90) | 0.778009 | brazilsoutheast, eastasia, francesouth, japaneast, newzealandnorth, switzerlandwest |
| Bottom decile price (P10) | 0.5108 | eastus2, mexicocentral, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 52 | |
| Offered in | 91.2% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v3 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.413 | brazilsoutheast |
| Bottom price | 0.192 | eastus, eastus2, westus2, westus3 |
| Median price | 0.235 | |
| Average price | 0.246931 | |
| Top decile price (P90) | 0.3094 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.2052 | eastus, eastus2, northcentralus, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v4 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.398 | brazilsoutheast |
| Bottom price | 0.192 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.23 | |
| Average price | 0.241817 | |
| Top decile price (P90) | 0.3018 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.202 | centralindia, eastus, eastus2, indiasouthcentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v5 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.398 | brazilsoutheast |
| Bottom price | 0.192 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.23 | |
| Average price | 0.241351 | |
| Top decile price (P90) | 0.3018 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.202 | centralindia, eastus, eastus2, indiasouthcentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v6 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.418 | brazilsoutheast |
| Bottom price | 0.202 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.242 | |
| Average price | 0.255472 | |
| Top decile price (P90) | 0.3196 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.212 | centralindia, eastus, eastus2, indiasouthcentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_DS4_v2 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.912 | francesouth |
| Bottom price | 0.458 | eastus2, westus2, westus3 |
| Median price | 0.5982 | |
| Average price | 0.630758 | |
| Top decile price (P90) | 0.778009 | brazilsoutheast, eastasia, francesouth, japaneast, newzealandnorth, switzerlandwest |
| Bottom decile price (P10) | 0.5108 | eastus2, mexicocentral, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 52 | |
| Offered in | 91.2% of regions | |
| Unit | USD/hour | |

### Standard_E2_v3 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.306 | brazilsoutheast |
| Bottom price | 0.126 | eastus, northcentralus, westus2, westus3 |
| Median price | 0.156 | |
| Average price | 0.162377 | |
| Top decile price (P90) | 0.20184 | brazilsouth, brazilsoutheast, francesouth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.1346 | eastus, eastus2, northcentralus, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v3 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.306 | brazilsoutheast |
| Bottom price | 0.126 | eastus, northcentralus, westus2, westus3 |
| Median price | 0.156 | |
| Average price | 0.162377 | |
| Top decile price (P90) | 0.20184 | brazilsouth, brazilsoutheast, francesouth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.1346 | eastus, eastus2, northcentralus, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v4 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.261 | brazilsoutheast |
| Bottom price | 0.126 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.152 | |
| Average price | 0.157041 | |
| Top decile price (P90) | 0.1974 | brazilsouth, brazilsoutheast, germanynorth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.13 | centralindia, eastus, eastus2, indiasouthcentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v5 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.261 | brazilsoutheast |
| Bottom price | 0.126 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.152 | |
| Average price | 0.157211 | |
| Top decile price (P90) | 0.1992 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.13 | centralindia, eastus, eastus2, indiasouthcentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v6 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.274 | brazilsoutheast |
| Bottom price | 0.132 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.16 | |
| Average price | 0.165228 | |
| Top decile price (P90) | 0.2086 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.136 | eastus, eastus2, indonesiacentral, malaysiawest, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_F4 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.373 | brazilsoutheast |
| Bottom price | 0.198 | centralindia |
| Median price | 0.228 | |
| Average price | 0.242439 | |
| Top decile price (P90) | 0.2926 | brazilsoutheast, germanynorth, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.2002 | centralindia, eastus, eastus2, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_F4s / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.373 | brazilsoutheast |
| Bottom price | 0.198 | centralindia |
| Median price | 0.228 | |
| Average price | 0.242439 | |
| Top decile price (P90) | 0.2926 | brazilsoutheast, germanynorth, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.2002 | centralindia, eastus, eastus2, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_F4s_v2 / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.341 | brazilsoutheast |
| Bottom price | 0.169 | eastus, eastus2, westus2, westus3 |
| Median price | 0.202 | |
| Average price | 0.208526 | |
| Top decile price (P90) | 0.252 | brazilsouth, brazilsoutheast, francesouth, germanynorth, norwaywest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.17 | centralindia, eastus, eastus2, northcentralus, southafricawest, westindia, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_FX4mds / Linux on-demand

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.723 | brazilsoutheast |
| Bottom price | 0.372 | eastus, eastus2, westus2 |
| Median price | 0.443 | |
| Average price | 0.443722 | |
| Top decile price (P90) | 0.4846 | brazilsouth, brazilsoutheast |
| Bottom decile price (P10) | 0.372 | eastus, eastus2, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 18 | |
| Offered in | 31.6% of regions | |
| Unit | USD/hour | |

### Standard_B4ms / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0384 | italynorth |
| Bottom price | 0.0333 | westus3 |
| Median price | 0.03585 | |
| Average price | 0.03585 | |
| Top decile price (P90) | 0.03789 | italynorth |
| Bottom decile price (P10) | 0.03381 | westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 2 | |
| Offered in | 3.5% of regions | |
| Unit | USD/hour | |

### Standard_D4 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.198 | brazilsoutheast |
| Bottom price | 0.107 | eastus2, southcentralus |
| Median price | 0.136 | |
| Average price | 0.14095 | |
| Top decile price (P90) | 0.177 | brazilsoutheast, eastasia, japaneast, southafricawest |
| Bottom decile price (P10) | 0.113 | centralindia, eastus2, southcentralus, westindia |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 31 | |
| Offered in | 54.4% of regions | |
| Unit | USD/hour | |

### Standard_D4_v2 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.182 | francesouth |
| Bottom price | 0.0673 | australiacentral2 |
| Median price | 0.11934 | |
| Average price | 0.124919 | |
| Top decile price (P90) | 0.155931 | brazilsoutheast, eastasia, francesouth, japaneast, newzealandnorth, norwaywest |
| Bottom decile price (P10) | 0.102 | australiacentral2, eastus2, mexicocentral, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 52 | |
| Offered in | 91.2% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v3 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.09193 | eastus2 |
| Bottom price | 0.025 | australiacentral2 |
| Median price | 0.044352 | |
| Average price | 0.0467355 | |
| Top decile price (P90) | 0.058598 | brazilsoutheast, canadacentral, eastus2, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.0370944 | australiacentral2, centralus, northcentralus, uksouth, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v4 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.07355 | brazilsoutheast |
| Bottom price | 0.024 | australiacentral2 |
| Median price | 0.042504 | |
| Average price | 0.0445197 | |
| Top decile price (P90) | 0.0557726 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0375514 | australiacentral2, centralindia, indiasouthcentral, northcentralus, uksouth, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v5 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.07355 | brazilsoutheast |
| Bottom price | 0.024 | australiacentral2 |
| Median price | 0.042504 | |
| Average price | 0.0444315 | |
| Top decile price (P90) | 0.0557726 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0375514 | australiacentral2, centralindia, indiasouthcentral, northcentralus, uksouth, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_D4s_v6 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.077246 | brazilsoutheast |
| Bottom price | 0.0252 | australiacentral2 |
| Median price | 0.044722 | |
| Average price | 0.0467331 | |
| Top decile price (P90) | 0.0590622 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0376996 | australiacentral2, eastus2, northcentralus, uksouth, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_DS4_v2 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.281762 | eastus2 |
| Bottom price | 0.0673 | australiacentral2 |
| Median price | 0.125685 | |
| Average price | 0.133816 | |
| Top decile price (P90) | 0.16582 | brazilsoutheast, canadacentral, eastasia, eastus2, francesouth, japaneast |
| Bottom decile price (P10) | 0.104004 | australiacentral2, mexicocentral, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 52 | |
| Offered in | 91.2% of regions | |
| Unit | USD/hour | |

### Standard_E2_v3 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.056549 | brazilsoutheast |
| Bottom price | 0.016 | australiacentral2 |
| Median price | 0.028644 | |
| Average price | 0.0296025 | |
| Top decile price (P90) | 0.0372996 | brazilsouth, brazilsoutheast, francesouth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.0244568 | australiacentral2, centralus, northcentralus, uksouth, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v3 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.06368 | eastus2 |
| Bottom price | 0.016 | australiacentral2 |
| Median price | 0.028829 | |
| Average price | 0.0307684 | |
| Top decile price (P90) | 0.0403634 | brazilsouth, brazilsoutheast, canadacentral, eastus2, norwaywest, switzerlandwest |
| Bottom decile price (P10) | 0.0244568 | australiacentral2, centralus, northcentralus, uksouth, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 53 | |
| Offered in | 93.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v4 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.048233 | brazilsoutheast |
| Bottom price | 0.0151 | australiacentral2 |
| Median price | 0.02809 | |
| Average price | 0.0288715 | |
| Top decile price (P90) | 0.0364796 | brazilsouth, brazilsoutheast, germanynorth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.0244674 | australiacentral2, centralindia, indiasouthcentral, northcentralus, uksouth, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v5 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.048233 | brazilsoutheast |
| Bottom price | 0.0151 | australiacentral2 |
| Median price | 0.02809 | |
| Average price | 0.0289032 | |
| Top decile price (P90) | 0.036812 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0244674 | australiacentral2, centralindia, indiasouthcentral, northcentralus, uksouth, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_E2s_v6 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.050635 | brazilsoutheast |
| Bottom price | 0.0159 | australiacentral2 |
| Median price | 0.029568 | |
| Average price | 0.0302352 | |
| Top decile price (P90) | 0.0385496 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0248374 | australiacentral2, eastus2, northcentralus, uksouth, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/hour | |

### Standard_F4 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0747 | brazilsoutheast |
| Bottom price | 0.026 | australiacentral2 |
| Median price | 0.0456 | |
| Average price | 0.0479319 | |
| Top decile price (P90) | 0.0587 | brazilsoutheast, germanynorth, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0398 | australiacentral2, centralindia, eastus, eastus2, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_F4s / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.122425 | eastus2 |
| Bottom price | 0.026 | australiacentral2 |
| Median price | 0.04717 | |
| Average price | 0.0514475 | |
| Top decile price (P90) | 0.0637696 | brazilsoutheast, canadacentral, eastus2, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.0413018 | australiacentral2, centralindia, francecentral, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_F4s_v2 / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.063017 | brazilsoutheast |
| Bottom price | 0.0222 | australiacentral2 |
| Median price | 0.034 | |
| Average price | 0.0366861 | |
| Top decile price (P90) | 0.043502 | brazilsoutheast, chilecentral, germanynorth, norwaywest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0319208 | australiacentral2, centralindia, northcentralus, southafricawest, westindia, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 55 | |
| Offered in | 96.5% of regions | |
| Unit | USD/hour | |

### Standard_FX4mds / Spot

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.13361 | brazilsoutheast |
| Bottom price | 0.068746 | eastus, eastus2, westus2 |
| Median price | 0.0818665 | |
| Average price | 0.082 | |
| Top decile price (P90) | 0.089554 | brazilsouth, brazilsoutheast |
| Bottom decile price (P10) | 0.068746 | eastus, eastus2, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 18 | |
| Offered in | 31.6% of regions | |
| Unit | USD/hour | |

## Blob storage

### Archive Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Premium SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Premium SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Standard SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.00826 | australiacentral, australiacentral2 |
| Bottom price | 0.002277 | swedencentral |
| Median price | 0.004 | |
| Average price | 0.00412202 | |
| Top decile price (P90) | 0.005 | australiacentral, australiacentral2, brazilsouth, centralindia, southindia, switzerlandwest |
| Bottom decile price (P10) | 0.00279 | germanynorth, germanywestcentral, northeurope, swedencentral, westeurope |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 41 | |
| Offered in | 71.9% of regions | |
| Unit | USD/GB/month | |

### Archive Tier / Standard SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Standard SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.005 | australiacentral2 |
| Bottom price | 0.00099 | eastus, northcentralus, northeurope, swedencentral, westus2, westus3 |
| Median price | 0.002 | |
| Average price | 0.00204922 | |
| Top decile price (P90) | 0.003024 | australiacentral, australiacentral2, brazilsouth, francesouth, switzerlandwest |
| Bottom decile price (P10) | 0.00099 | eastus, northcentralus, northeurope, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Archive Tier / Standard SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.00878 | switzerlandwest |
| Bottom price | 0.00279 | germanynorth, germanywestcentral, northeurope, swedencentral, westeurope |
| Median price | 0.004 | |
| Average price | 0.00422798 | |
| Top decile price (P90) | 0.00506 | australiacentral, australiacentral2, brazilsouth, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.00279 | germanynorth, germanywestcentral, northeurope, swedencentral, westeurope |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 41 | |
| Offered in | 71.9% of regions | |
| Unit | USD/GB/month | |

### Archive Tier / Standard SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Archive Tier / Standard SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cold Tier / Standard SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.04784 | brazilsoutheast |
| Bottom price | 0.02 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Median price | 0.023 | |
| Average price | 0.0248831 | |
| Top decile price (P90) | 0.03024 | brazilsouth, brazilsoutheast, eastus, northcentralus, westindia |
| Bottom decile price (P10) | 0.02 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Cold Tier / Standard SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0687 | francecentral |
| Bottom price | 0.0225 | centralus, eastus2, northeurope, southcentralus, westus2 |
| Median price | 0.0268 | |
| Average price | 0.0341586 | |
| Top decile price (P90) | 0.054905 | brazilsouth, eastasia, francecentral |
| Bottom decile price (P10) | 0.0225 | centralus, eastus2, northeurope, southcentralus, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 26 | |
| Offered in | 45.6% of regions | |
| Unit | USD/GB/month | |

### Cold Tier / Standard SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.02704 | brazilsoutheast |
| Bottom price | 0.01 | austriaeast, belgiumcentral, centralus, denmarkeast, eastus2, germanynorth, germanywestcentral, indonesiacentral, italynorth, malaysiawest, northeurope, polandcentral (+7 more) |
| Median price | 0.011 | |
| Average price | 0.0122004 | |
| Top decile price (P90) | 0.0152 | brazilsouth, brazilsoutheast, chilecentral, eastus, mexicocentral, northcentralus, westindia |
| Bottom decile price (P10) | 0.01 | austriaeast, belgiumcentral, centralus, denmarkeast, eastus2, germanynorth, germanywestcentral, indonesiacentral, italynorth, malaysiawest, northeurope, polandcentral (+7 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Cold Tier / Standard SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0598 | brazilsoutheast |
| Bottom price | 0.025 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Median price | 0.0288 | |
| Average price | 0.0311228 | |
| Top decile price (P90) | 0.0378 | brazilsouth, brazilsoutheast, eastus, northcentralus, westindia |
| Bottom decile price (P10) | 0.025 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Cold Tier / Standard SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0855 | brazilsouth |
| Bottom price | 0.0225 | swedencentral, westus3 |
| Median price | 0.0309 | |
| Average price | 0.0384907 | |
| Top decile price (P90) | 0.0587815 | brazilsouth, centralindia, japanwest |
| Bottom decile price (P10) | 0.025 | germanywestcentral, swedencentral, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 26 | |
| Offered in | 45.6% of regions | |
| Unit | USD/GB/month | |

### Cold Tier / Standard SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.026543 | chilecentral |
| Bottom price | 0.0125 | centralus, eastus2, indonesiacentral, malaysiawest, northeurope, southcentralus, spaincentral, swedencentral, westus2, westus3 |
| Median price | 0.01375 | |
| Average price | 0.0142658 | |
| Top decile price (P90) | 0.0158 | brazilsouth, chilecentral, eastus, mexicocentral |
| Bottom decile price (P10) | 0.0125 | centralus, eastus2, indonesiacentral, malaysiawest, northeurope, southcentralus, spaincentral, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 39 | |
| Offered in | 68.4% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.39 | brazilsoutheast |
| Bottom price | 0.15 | eastus, eastus2, swedencentral, westus2, westus3 |
| Median price | 0.203 | |
| Average price | 0.209362 | |
| Top decile price (P90) | 0.264 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.1713 | eastus, eastus2, mexicocentral, swedencentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Premium SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.399 | brazilsouth |
| Bottom price | 0.2 | eastus, eastus2, westus2, westus3 |
| Median price | 0.259 | |
| Average price | 0.262597 | |
| Top decile price (P90) | 0.2902 | brazilsouth, eastasia, newzealandnorth, southafricanorth |
| Bottom decile price (P10) | 0.21167 | eastus, eastus2, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 37 | |
| Offered in | 64.9% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.07498 | brazilsoutheast |
| Bottom price | 0.0368 | centralus, eastus2, northeurope, southcentralus, westcentralus, westus2, westus3 |
| Median price | 0.04 | |
| Average price | 0.0436168 | |
| Top decile price (P90) | 0.050544 | brazilsouth, brazilsoutheast, israelcentral, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.0368 | centralus, eastus2, northeurope, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.086112 | brazilsouth |
| Bottom price | 0.0414 | centralus, eastus2, southcentralus, westus2 |
| Median price | 0.046 | |
| Average price | 0.0523613 | |
| Top decile price (P90) | 0.062216 | brazilsouth, eastasia, southafricanorth |
| Bottom decile price (P10) | 0.0414 | centralus, eastus2, southcentralus, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 26 | |
| Offered in | 45.6% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.04238 | brazilsoutheast |
| Bottom price | 0.018 | indonesiacentral, malaysiawest |
| Median price | 0.02 | |
| Average price | 0.0212679 | |
| Top decile price (P90) | 0.025592 | brazilsouth, brazilsoutheast, chilecentral, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.0184 | centralus, eastus2, indonesiacentral, malaysiawest, southcentralus, spaincentral, swedencentral, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / RA-GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.09373 | brazilsoutheast |
| Bottom price | 0.046 | centralus, eastus2, northeurope, southcentralus, westcentralus, westus2, westus3 |
| Median price | 0.05 | |
| Average price | 0.0537534 | |
| Top decile price (P90) | 0.06228 | brazilsouth, brazilsoutheast, francesouth, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.046 | centralus, eastus2, northeurope, southcentralus, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 44 | |
| Offered in | 77.2% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / RA-GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.10764 | brazilsouth |
| Bottom price | 0.05175 | centralus, eastus2, southcentralus, westus2 |
| Median price | 0.059875 | |
| Average price | 0.0665262 | |
| Top decile price (P90) | 0.07777 | brazilsouth, eastasia, southafricanorth |
| Bottom decile price (P10) | 0.05175 | centralus, eastus2, southcentralus, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 26 | |
| Offered in | 45.6% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.04075 | brazilsouth |
| Bottom price | 0.0225 | germanywestcentral, indonesiacentral, malaysiawest, polandcentral |
| Median price | 0.025 | |
| Average price | 0.0251627 | |
| Top decile price (P90) | 0.02764 | brazilsouth, chilecentral, eastasia, mexicocentral |
| Bottom decile price (P10) | 0.0229 | germanywestcentral, indonesiacentral, malaysiawest, polandcentral |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 39 | |
| Offered in | 68.4% of regions | |
| Unit | USD/GB/month | |

## Block storage (managed disks)

### Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.296397 | brazilsoutheast |
| Bottom price | 0.118802 | southindia |
| Median price | 0.144 | |
| Average price | 0.149549 | |
| Top decile price (P90) | 0.193891 | brazilsouth, brazilsoutheast, francesouth, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.127189 | eastus2, southcentralus, southindia, westcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.341997 | brazilsouth |
| Bottom price | 0.18 | eastus2, southcentralus, westus2, westus3 |
| Median price | 0.216 | |
| Average price | 0.214764 | |
| Top decile price (P90) | 0.239573 | brazilsouth, chilecentral, norwayeast, southafricanorth |
| Bottom decile price (P10) | 0.194383 | eastus2, southcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 39 | |
| Offered in | 68.4% of regions | |
| Unit | USD/GB/month | |

### Standard HDD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.1248 | brazilsoutheast |
| Bottom price | 0.04 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, japanwest (+16 more) |
| Median price | 0.044 | |
| Average price | 0.0481474 | |
| Top decile price (P90) | 0.064 | australiacentral, australiacentral2, australiaeast, australiasoutheast, brazilsouth, brazilsoutheast, newzealandnorth, southafricawest |
| Bottom decile price (P10) | 0.04 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, japanwest (+16 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Standard HDD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Standard SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.210603 | brazilsoutheast |
| Bottom price | 0.075 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, japanwest (+16 more) |
| Median price | 0.0825 | |
| Average price | 0.0878587 | |
| Top decile price (P90) | 0.107248 | brazilsouth, brazilsoutheast, francesouth, southafricanorth, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.075 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, japanwest (+16 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Standard SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.21 | brazilsouth |
| Bottom price | 0.1125 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, koreacentral (+10 more) |
| Median price | 0.1125 | |
| Average price | 0.124177 | |
| Top decile price (P90) | 0.1539 | brazilsouth, chilecentral, newzealandnorth, southafricanorth |
| Bottom decile price (P10) | 0.1125 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, koreacentral (+10 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 39 | |
| Offered in | 68.4% of regions | |
| Unit | USD/GB/month | |

### Ultra Disk / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.23944 | brazilsouth |
| Bottom price | 0.11972 | brazilsoutheast, eastus, eastus2, westus2, westus3 |
| Median price | 0.15549 | |
| Average price | 0.161147 | |
| Top decile price (P90) | 0.206809 | brazilsouth, norwaywest, southafricawest, switzerlandwest, uaecentral |
| Bottom decile price (P10) | 0.123808 | brazilsoutheast, eastus, eastus2, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 48 | |
| Offered in | 84.2% of regions | |
| Unit | USD/GB/month | |

### Ultra Disk / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

## Azure Files

### Cool Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cool Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cool Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cool Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Cool Tier / Standard HDD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.07176 | brazilsoutheast |
| Bottom price | 0.03 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Median price | 0.0402 | |
| Average price | 0.0396991 | |
| Top decile price (P90) | 0.04926 | brazilsouth, brazilsoutheast, eastus, southafricawest, westus |
| Bottom decile price (P10) | 0.03 | centralus, eastus2, germanynorth, germanywestcentral, northeurope, southcentralus, swedencentral, westcentralus, westeurope, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Cool Tier / Standard HDD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.08314 | uaenorth |
| Bottom price | 0.0338 | centralus, eastus2, northeurope, westus2 |
| Median price | 0.0463625 | |
| Average price | 0.048917 | |
| Top decile price (P90) | 0.0728973 | southafricanorth, switzerlandnorth, uaenorth |
| Bottom decile price (P10) | 0.0338 | centralus, eastus2, northeurope, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 24 | |
| Offered in | 42.1% of regions | |
| Unit | USD/GB/month | |

### Cool Tier / Standard HDD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.04056 | brazilsoutheast |
| Bottom price | 0.014352 | israelcentral, qatarcentral |
| Median price | 0.0195 | |
| Average price | 0.0196165 | |
| Top decile price (P90) | 0.024 | brazilsouth, brazilsoutheast, chilecentral, eastasia, mexicocentral, southafricawest, southeastasia |
| Bottom decile price (P10) | 0.015 | austriaeast, belgiumcentral, centralus, denmarkeast, eastus2, germanynorth, germanywestcentral, israelcentral, italynorth, northeurope, polandcentral, qatarcentral (+7 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Cool Tier / Standard HDD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.039899 | chilecentral |
| Bottom price | 0.01794 | israelcentral, qatarcentral |
| Median price | 0.0211625 | |
| Average price | 0.0237651 | |
| Top decile price (P90) | 0.03 | brazilsouth, chilecentral, eastasia, mexicocentral, southeastasia |
| Bottom decile price (P10) | 0.01875 | austriaeast, belgiumcentral, denmarkeast, germanywestcentral, israelcentral, polandcentral, qatarcentral, spaincentral |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 40 | |
| Offered in | 70.2% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Hot Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.416 | brazilsoutheast |
| Bottom price | 0.16 | eastus, eastus2, northcentralus, norwaywest, westus2, westus3 |
| Median price | 0.192 | |
| Average price | 0.204634 | |
| Top decile price (P90) | 0.2544 | australiacentral, australiacentral2, brazilsouth, brazilsoutheast, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.1678 | eastus, eastus2, northcentralus, norwaywest, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.4 | brazilsouth |
| Bottom price | 0.2 | eastus, eastus2, northcentralus, westus2, westus3 |
| Median price | 0.24 | |
| Average price | 0.2407 | |
| Top decile price (P90) | 0.2806 | brazilsouth, eastasia, japanwest, norwayeast |
| Bottom decile price (P10) | 0.2 | eastus, eastus2, northcentralus, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 40 | |
| Offered in | 70.2% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard HDD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.1124 | brazilsoutheast |
| Bottom price | 0.0508 | eastus2, northeurope, westus2, westus3 |
| Median price | 0.06 | |
| Average price | 0.0625841 | |
| Top decile price (P90) | 0.07665 | brazilsouth, brazilsoutheast, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.053 | eastus2, northeurope, uksouth, ukwest, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 44 | |
| Offered in | 77.2% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard HDD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.10685 | southafricanorth |
| Bottom price | 0.0588 | northeurope |
| Median price | 0.0675 | |
| Average price | 0.0711379 | |
| Top decile price (P90) | 0.0917446 | southafricanorth, switzerlandnorth, uaenorth |
| Bottom decile price (P10) | 0.05942 | eastus2, northeurope, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 25 | |
| Offered in | 43.9% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard HDD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.063544 | brazilsoutheast |
| Bottom price | 0.0255 | eastus2, indonesiacentral, malaysiawest, westus2, westus3 |
| Median price | 0.0287 | |
| Average price | 0.0307031 | |
| Top decile price (P90) | 0.03796 | brazilsouth, brazilsoutheast, chilecentral, norwaywest, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.026 | eastus2, indonesiacentral, israelcentral, malaysiawest, qatarcentral, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Hot Tier / Standard HDD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.0611 | brazilsouth |
| Bottom price | 0.0317 | eastus2, northeurope, westus2 |
| Median price | 0.0345 | |
| Average price | 0.0365171 | |
| Top decile price (P90) | 0.0450331 | brazilsouth, chilecentral, southafricanorth, switzerlandnorth |
| Bottom decile price (P10) | 0.0319 | eastus2, indonesiacentral, malaysiawest, northeurope, swedencentral, westus2 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 40 | |
| Offered in | 70.2% of regions | |
| Unit | USD/GB/month | |

### Standard Tier / Premium SSD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Standard Tier / Premium SSD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Standard Tier / Premium SSD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Standard Tier / Premium SSD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Not offered in any region | | |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 0 | |
| Offered in | 0.0% of regions | |

### Standard Tier / Standard HDD / GRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.18814 | brazilsoutheast |
| Bottom price | 0.0962 | germanynorth, germanywestcentral |
| Median price | 0.11 | |
| Average price | 0.113389 | |
| Top decile price (P90) | 0.143287 | brazilsoutheast, francesouth, southafricanorth, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.1 | centralus, eastasia, eastus, eastus2, germanynorth, germanywestcentral, japaneast, japanwest, malaysiawest, northcentralus, northeurope, southcentralus (+10 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 45 | |
| Offered in | 78.9% of regions | |
| Unit | USD/GB/month | |

### Standard Tier / Standard HDD / GZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.20925 | japanwest |
| Bottom price | 0.135 | centralus, eastasia, eastus, eastus2, germanywestcentral, japaneast, northeurope, southeastasia, swedencentral, westeurope, westus2, westus3 |
| Median price | 0.1485 | |
| Average price | 0.15701 | |
| Top decile price (P90) | 0.19233 | japanwest, southafricanorth, switzerlandnorth |
| Bottom decile price (P10) | 0.135 | centralus, eastasia, eastus, eastus2, germanywestcentral, japaneast, northeurope, southeastasia, swedencentral, westeurope, westus2, westus3 |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 25 | |
| Offered in | 43.9% of regions | |
| Unit | USD/GB/month | |

### Standard Tier / Standard HDD / LRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.10634 | brazilsoutheast |
| Bottom price | 0.0577 | austriaeast, belgiumcentral, denmarkeast, germanynorth, germanywestcentral |
| Median price | 0.06 | |
| Average price | 0.0665601 | |
| Top decile price (P90) | 0.0847188 | brazilsoutheast, francesouth, norwaywest, southafricanorth, southafricawest, switzerlandwest |
| Bottom decile price (P10) | 0.05976 | austriaeast, belgiumcentral, denmarkeast, germanynorth, germanywestcentral, southindia |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 57 | |
| Offered in | 100.0% of regions | |
| Unit | USD/GB/month | |

### Standard Tier / Standard HDD / ZRS

| Statistic | Price/Count | Regions |
| --- | --- | --- |
| Top price | 0.108 | southafricanorth |
| Bottom price | 0.01875 | swedencentral |
| Median price | 0.075 | |
| Average price | 0.0800765 | |
| Top decile price (P90) | 0.09375 | brazilsouth, chilecentral, francecentral, southafricanorth, uksouth |
| Bottom decile price (P10) | 0.075 | austriaeast, belgiumcentral, centralus, denmarkeast, eastasia, eastus, eastus2, germanywestcentral, indonesiacentral, italynorth, japaneast, japanwest (+10 more) |
| Number of regions (incl. na) | 57 | |
| Number of regions with a price | 40 | |
| Offered in | 70.2% of regions | |
| Unit | USD/GB/month | |
