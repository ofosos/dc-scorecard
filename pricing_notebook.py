import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import json
    from pathlib import Path

    import pandas as pd

    return Path, json, pd


@app.cell
def _(Path):
    DATA_DIR = Path(__file__).parent
    return (DATA_DIR,)


@app.cell
def _(mo):
    mo.md(r"""
    # DC Scorecard pricing notebook

    Loads the annotated Azure regions and every pricing dataset (CSV) in
    this repository into pandas DataFrames, then shows an overview of all
    loaded pricing tables.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## az_regions_annotated

    Annotated Azure region list (region metadata plus country, ILO, and
    rights annotations), flattened for use as a lookup table.
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
    ## compute_prices_availability

    Virtual machine per-hour pricing (Linux and spot) and availability per
    Azure region and instance size.
    """)
    return


@app.cell
def _(DATA_DIR, pd):
    compute_prices_availability = pd.read_csv(
        DATA_DIR / "compute_prices_availability.csv"
    )
    compute_prices_availability
    return (compute_prices_availability,)


@app.cell
def _(mo):
    mo.md(r"""
    ## blob_storage_pricing

    Blob storage price per GB by region, access frequency, performance
    tier, and redundancy option.
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

    Managed disk (block storage) price per GB by region, performance tier,
    and redundancy option.
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
    ## files_pricing

    Azure Files price per GB by region, access frequency, performance
    tier, and redundancy option.
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
    ## Pricing overview

    Rows, columns, and column names of every pricing dataset loaded above.
    """)
    return


@app.cell
def _(blob_storage_pricing, block_storage_pricing, compute_prices_availability, files_pricing, mo, pd):
    _datasets = {
        "compute_prices_availability": compute_prices_availability,
        "blob_storage_pricing": blob_storage_pricing,
        "block_storage_pricing": block_storage_pricing,
        "files_pricing": files_pricing,
    }
    pricing_overview = pd.DataFrame(
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
    mo.ui.table(pricing_overview, selection=None)
    return


if __name__ == "__main__":
    app.run()
