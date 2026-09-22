import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import json
    from pathlib import Path

    import numpy as np
    import pandas as pd

    return Path, json, pd


@app.cell
def _(Path):
    DATA_DIR = Path(__file__).parent
    return (DATA_DIR,)


@app.cell
def _(mo):
    mo.md(r"""
    # DC Scorecard data

    Loads every JSON and CSV dataset in this repository into a pandas
    DataFrame (non-tabular JSON is exposed as Python objects), and finishes
    with an overview of all loaded datasets.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## azure_carbon_intensity

    Grid carbon intensity per Azure region (current and 24h average).
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    azure_carbon_intensity = pd.read_csv(DATA_DIR / "azure_carbon_intensity.csv")
    azure_carbon_intensity
    return (azure_carbon_intensity,)


@app.cell
def _(mo):
    mo.md(r"""
    ## blob_storage_pricing

    Azure Blob Storage pricing per region (price per GB by tier, performance, redundancy).
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    blob_storage_pricing = pd.read_csv(DATA_DIR / "blob_storage_pricing.csv")
    blob_storage_pricing
    return (blob_storage_pricing,)


@app.cell
def _(mo):
    mo.md(r"""
    ## block_storage_pricing

    Azure managed disk (block storage) pricing per region by performance and redundancy.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    block_storage_pricing = pd.read_csv(DATA_DIR / "block_storage_pricing.csv")
    block_storage_pricing
    return (block_storage_pricing,)


@app.cell
def _(mo):
    mo.md(r"""
    ## compute_prices_availability

    Compute instance pricing and availability per region (Linux and spot hourly prices).
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    compute_prices_availability = pd.read_csv(DATA_DIR / "compute_prices_availability.csv")
    compute_prices_availability
    return (compute_prices_availability,)


@app.cell
def _(mo):
    mo.md(r"""
    ## files_pricing

    Azure Files pricing per region by tier, performance, and redundancy.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    files_pricing = pd.read_csv(DATA_DIR / "files_pricing.csv")
    files_pricing
    return (files_pricing,)


@app.cell
def _(mo):
    mo.md(r"""
    ## ged_azure

    UCDP GED conflict events mapped to Azure regions (full event list).
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    ged_azure = pd.read_csv(DATA_DIR / "ged-azure.csv", index_col=0)
    ged_azure
    return (ged_azure,)


@app.cell
def _(mo):
    mo.md(r"""
    ## ged_azure_agg

    UCDP GED conflict events aggregated per Azure region by type of violence.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    ged_azure_agg = pd.read_csv(DATA_DIR / "ged-azure-agg.csv", index_col=0)
    ged_azure_agg
    return (ged_azure_agg,)


@app.cell
def _(mo):
    mo.md(r"""
    ## global_rights_index

    Global Rights Index country ratings.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    global_rights_index = pd.read_csv(DATA_DIR / "global-rights-index.csv")
    global_rights_index
    return (global_rights_index,)


@app.cell
def _(mo):
    mo.md(r"""
    ## global_rights_azure_regions

    Global Rights Index ratings mapped to Azure regions.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    global_rights_azure_regions = pd.read_csv(DATA_DIR / "global_rights_azure_regions.csv")
    global_rights_azure_regions
    return (global_rights_azure_regions,)


@app.cell
def _(mo):
    mo.md(r"""
    ## ilo_core_conventions

    Ratification years of core ILO conventions per country.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    ilo_core_conventions = pd.read_csv(DATA_DIR / "ilo-core-conventions.csv")
    ilo_core_conventions
    return (ilo_core_conventions,)


@app.cell
def _(mo):
    mo.md(r"""
    ## ilo_azure_regions

    Azure regions annotated with country and ILO convention ratification data.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    ilo_azure_regions = pd.read_csv(DATA_DIR / "ilo_azure_regions.csv")
    ilo_azure_regions
    return (ilo_azure_regions,)


@app.cell
def _(mo):
    mo.md(r"""
    ## region_temperatures_sweatscore

    Sweat score (heat-based ranking) per Azure region.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    region_temperatures_sweatscore = pd.read_csv(DATA_DIR / "region_temperatures_sweatscore.csv")
    region_temperatures_sweatscore
    return (region_temperatures_sweatscore,)


@app.cell
def _(mo):
    mo.md(r"""
    ## az_regions

    Azure region list (name, display names, metadata), flattened from the ListRegions API response.
    """)
    return


@app.cell
def _(DATA_DIR, json, pd):
    az_regions = pd.json_normalize(
        json.loads((DATA_DIR / "az_regions.json").read_text()), sep="_"
    )
    az_regions
    return (az_regions,)


@app.cell
def _(mo):
    mo.md(r"""
    ## az_regions_annotated

    Annotated Azure region list (region metadata plus country, ILO, and rights annotations).
    """)
    return


@app.cell
def _(DATA_DIR, json, pd):
    az_regions_annotated = pd.json_normalize(
        json.loads((DATA_DIR / "az_regions_annotated.json").read_text()), sep="_"
    )
    az_regions_annotated
    return (az_regions_annotated,)


@app.cell
def _(mo):
    mo.md(r"""
    ## region_temperatures

    Daily temperature time series per Azure region (date, temperature).
    """)
    return


@app.cell
def _(DATA_DIR, json, pd):
    _rows = [
        (region, entry[0], entry[1])
        for region, series in json.loads(
            (DATA_DIR / "region_temperatures.json").read_text()
        ).items()
        for entry in series
    ]
    region_temperatures = pd.DataFrame(
        _rows, columns=["region", "date", "temperature"]
    )
    region_temperatures
    return (region_temperatures,)


@app.cell
def _(mo):
    mo.md(r"""
    ## gdacs_events

    GDACS disaster events mapped to Azure regions.
    """)
    return


@app.cell
def _(DATA_DIR, json, pd):
    _rows = [
        {"region": region, **event}
        for region, events in json.loads(
            (DATA_DIR / "gdacs_events_by_region.json").read_text()
        ).items()
        for event in events
    ]
    gdacs_events = pd.DataFrame(_rows)
    gdacs_events
    return (gdacs_events,)


@app.cell
def _(DATA_DIR, json, mo):
    gdac_swagger = json.loads((DATA_DIR / "gdac-swagger.json").read_text())
    mo.md(
        f"""
        ## gdac_swagger

        GDACS API OpenAPI specification — `{gdac_swagger["info"]["title"]}`,
        version `{gdac_swagger["info"]["version"]}`,
        {len(gdac_swagger["paths"])} endpoint paths.

        Loaded as the Python dict `gdac_swagger`.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dataset overview

    Rows and columns of every dataset loaded above.
    """)
    return


@app.cell
def _(
    az_regions,
    az_regions_annotated,
    azure_carbon_intensity,
    blob_storage_pricing,
    block_storage_pricing,
    compute_prices_availability,
    files_pricing,
    gdacs_events,
    ged_azure,
    ged_azure_agg,
    global_rights_azure_regions,
    global_rights_index,
    ilo_azure_regions,
    ilo_core_conventions,
    mo,
    pd,
    region_temperatures,
    region_temperatures_sweatscore,
):
    _datasets = {
        "az_regions": az_regions,
        "az_regions_annotated": az_regions_annotated,
        "azure_carbon_intensity": azure_carbon_intensity,
        "blob_storage_pricing": blob_storage_pricing,
        "block_storage_pricing": block_storage_pricing,
        "compute_prices_availability": compute_prices_availability,
        "files_pricing": files_pricing,
        "gdacs_events": gdacs_events,
        "ged_azure": ged_azure,
        "ged_azure_agg": ged_azure_agg,
        "global_rights_azure_regions": global_rights_azure_regions,
        "global_rights_index": global_rights_index,
        "ilo_azure_regions": ilo_azure_regions,
        "ilo_core_conventions": ilo_core_conventions,
        "region_temperatures": region_temperatures,
        "region_temperatures_sweatscore": region_temperatures_sweatscore,
    }
    dataset_overview = pd.DataFrame(
        [
            {
                "dataset": name,
                "rows": df.shape[0],
                "columns": df.shape[1],
                "column_names": ", ".join(map(str, df.columns)),
            }
            for name, df in _datasets.items()
        ]
    )
    mo.ui.table(dataset_overview, selection=None)
    return


if __name__ == "__main__":
    app.run()
