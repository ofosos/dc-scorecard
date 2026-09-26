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
def _(
    blob_storage_pricing,
    block_storage_pricing,
    compute_prices_availability,
    files_pricing,
    mo,
    pd,
):
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


@app.cell
def _(mo):
    mo.md(r"""
    ## Silos

    Data silo definitions: each silo maps to a list of Azure regions.
    """)
    return


@app.cell
def _(DATA_DIR, json):
    silos = json.loads((DATA_DIR / "silos.json").read_text())
    return (silos,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Price basket

    A configurable basket of resources whose prices are looked up per
    region in the pricing datasets loaded above. Adjust the amount of each
    item below; the basket and totals recalculate automatically.

    Note on units: VM prices are per hour, storage prices are per GB, so
    each line item's sum is `amount x price` in the item's own unit and
    the per-region total adds those sums up.
    """)
    return


@app.cell
def _(mo):
    item_amounts = {
        "vm_e2s_v4": 730,
        "vm_d4s_v5": 730,
        "blob_hot": 1000,
        "blob_cold": 5000,
        "block_std_ssd": 500,
        "block_premium_ssd": 100,
        "files_cool": 1000,
        "files_standard": 1000,
        "files_hot": 200,
    }
    amounts = mo.ui.dictionary(
        {
            key: mo.ui.number(0, 1_000_000, value=value, label=key)
            for key, value in item_amounts.items()
        }
    )
    amounts
    return (amounts,)


@app.cell
def _():
    BASKET = [
        {
            "id": "vm_e2s_v4",
            "item": "VM: Standard_E2s_v4 / Linux on-demand",
            "unit": "hours",
            "kind": "vm",
            "instance": "Standard_E2s_v4",
        },
        {
            "id": "vm_d4s_v5",
            "item": "VM: Standard_D4s_v5 / Linux on-demand",
            "unit": "hours",
            "kind": "vm",
            "instance": "Standard_D4s_v5",
        },
        {
            "id": "blob_hot",
            "item": "Blob storage: Hot Tier / Standard / LRS",
            "unit": "GB",
            "kind": "blob",
            "access_frequency": "Hot Tier",
            "performance": "Standard",
            "redundancy": "LRS",
        },
        {
            "id": "blob_cold",
            "item": "Blob storage: Cold Tier / Standard / LRS",
            "unit": "GB",
            "kind": "blob",
            "access_frequency": "Cold Tier",
            "performance": "Standard",
            "redundancy": "LRS",
        },
        {
            "id": "block_std_ssd",
            "item": "Block storage: Standard SSD / LRS",
            "unit": "GB",
            "kind": "block",
            "performance": "Standard SSD",
            "redundancy": "LRS",
        },
        {
            "id": "block_premium_ssd",
            "item": "Block storage: Premium SSD / LRS",
            "unit": "GB",
            "kind": "block",
            "performance": "Premium SSD",
            "redundancy": "LRS",
        },
        {
            "id": "files_cool",
            "item": "Azure Files: Cool Tier / Standard HDD / LRS",
            "unit": "GB",
            "kind": "files",
            "access_frequency": "Cool Tier",
            "performance": "Standard HDD",
            "redundancy": "LRS",
        },
        {
            "id": "files_standard",
            "item": "Azure Files: Transaction Optimized / Standard HDD / LRS",
            "unit": "GB",
            "kind": "files",
            "access_frequency": "Transaction Optimized",
            "performance": "Standard HDD",
            "redundancy": "LRS",
        },
        {
            "id": "files_hot",
            "item": "Azure Files: Hot Tier / Premium SSD / LRS",
            "unit": "GB",
            "kind": "files",
            "access_frequency": "Hot Tier",
            "performance": "Premium SSD",
            "redundancy": "LRS",
        },
    ]
    return (BASKET,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Basket per region

    One row per line item per region, with the looked-up price, the
    configured amount, and the line sum.
    """)
    return


@app.cell
def _(
    BASKET,
    amounts,
    blob_storage_pricing,
    block_storage_pricing,
    compute_prices_availability,
    files_pricing,
    pd,
):
    _access_priced = {"blob": blob_storage_pricing, "files": files_pricing}

    def _price_for(spec, region):
        if spec["kind"] == "vm":
            rows = compute_prices_availability[
                (compute_prices_availability["region"] == region)
                & (compute_prices_availability["instance"] == spec["instance"])
            ]
            price = pd.to_numeric(rows["linux_price_hourly"], errors="coerce")
        elif spec["kind"] == "block":
            rows = block_storage_pricing[
                (block_storage_pricing["Region"] == region)
                & (block_storage_pricing["Performance"] == spec["performance"])
                & (block_storage_pricing["Redundancy"] == spec["redundancy"])
            ]
            price = pd.to_numeric(rows["PricePerGB"], errors="coerce")
        else:
            frame = _access_priced[spec["kind"]]
            rows = frame[
                (frame["Region"] == region)
                & (frame["AccessFrequency"] == spec["access_frequency"])
                & (frame["Performance"] == spec["performance"])
                & (frame["Redundancy"] == spec["redundancy"])
            ]
            price = pd.to_numeric(rows["PricePerGB"], errors="coerce")
        if price.empty or pd.isna(price.iloc[0]):
            return float("nan")
        return float(price.iloc[0])

    basket_rows = []
    for region in sorted(compute_prices_availability["region"].unique()):
        for spec in BASKET:
            amount = amounts.value[spec["id"]]
            price = _price_for(spec, region)
            basket_rows.append(
                {
                    "region": region,
                    "item": spec["item"],
                    "unit": spec["unit"],
                    "amount": amount,
                    "price": price,
                    "sum": amount * price,
                }
            )
    basket = pd.DataFrame(basket_rows)
    basket
    return (basket,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Basket totals per region

    The total basket price for every region, cheapest first.
    """)
    return


@app.cell
def _(basket, pd):
    basket_totals = (
        basket.groupby("region", as_index=False)["sum"]
        .sum()
        .rename(columns={"sum": "basket_total"})
        .sort_values("basket_total")
        .reset_index(drop=True)
    )
    basket_totals
    return (basket_totals,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Basket scores per silo

    Same computation as the `global_rights` cell in `data_notebook.py`:
    for every silo, rank the member regions on their basket total
    (cheapest = rank 1) and compute count, average, and median; every
    tuple is inserted into `scores.db` with the adjustable KPI name
    below (default `basket_balanced`).
    """)
    return


@app.cell
def _(mo):
    kpi_input = mo.ui.text(value="basket_balanced", label="KPI")
    kpi_input
    return (kpi_input,)


@app.cell
def _():
    import sqlmodel

    DATABASE_URL = "sqlite:///scores.db"
    engine = sqlmodel.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(engine):
    from sqlmodel import Field, Session, SQLModel, insert

    class ScoreEntry(SQLModel, table=True):
        __table_args__ = {"extend_existing": True}
        id: int | None = Field(default=None, primary_key=True)
        silo: str
        region: str
        kpi: str
        value: float
        index: float
        tot_values: int
        average: float
        median: float

    SQLModel.metadata.create_all(engine)
    return ScoreEntry, Session, insert


@app.cell
def _(ScoreEntry, Session, basket_totals, engine, insert, kpi_input, silos):
    basket_data = []

    for silo, regions in silos.items():
        silo_spec = basket_totals[
            basket_totals["region"].isin(regions)
        ].copy()
        silo_spec["rank"] = silo_spec["basket_total"].rank(ascending=True)

        for _index, row in silo_spec.iterrows():
            basket_data.append(
                {
                    "silo": silo,
                    "region": row["region"],
                    "kpi": kpi_input.value,
                    "value": row["basket_total"],
                    "index": row["rank"],
                    "tot_values": silo_spec["region"].count(),
                    "average": silo_spec["basket_total"].mean(),
                    "median": silo_spec["basket_total"].median(),
                }
            )
        print(
            f"{kpi_input.value}, {silo}, count={silo_spec['region'].count()}, "
            f"median={silo_spec['basket_total'].median()}, "
            f"max={silo_spec['basket_total'].max()}, "
            f"min={silo_spec['basket_total'].min()}, "
            f"avg={silo_spec['basket_total'].mean()}"
        )

    with Session(engine) as session:
        session.exec(insert(ScoreEntry), params=basket_data)
        session.commit()
    return


if __name__ == "__main__":
    app.run()
