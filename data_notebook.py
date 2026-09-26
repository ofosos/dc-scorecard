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
    # DC Scorecard "soft" data

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silos

    Load silos
    """)
    return


@app.cell
def _(DATA_DIR, json):
    silos = json.loads((DATA_DIR / "silos.json").read_text())
    return (silos,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Materialize Silos / Indexes
    """)
    return


@app.cell
def _():
    import sqlmodel

    DATABASE_URL = "sqlite:///scores.db"
    engine = sqlmodel.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(engine):
    from sqlmodel import Field, Session, SQLModel, insert, select


    class SiloRegionMapping(SQLModel, table=True):
        __table_args__ = {'extend_existing': True}
        id: int | None = Field(default=None, primary_key=True)
        silo: str
        region: str

    class ScoreEntry(SQLModel, table=True):
        __table_args__ = {'extend_existing': True}
        id: int | None = Field(default=None, primary_key=True)
        silo: str
        region: str
        kpi: str
        value: float
        index: int
        tot_values: int
        average: float
        median: int

    SQLModel.metadata.create_all(engine)
    return ScoreEntry, Session, SiloRegionMapping, insert, select


@app.cell
def _(Session, SiloRegionMapping, engine, select, silos):
    for silo, regions in silos.items():
        for region in regions:
            with Session(engine) as session:

                statement = select(SiloRegionMapping).where(SiloRegionMapping.silo == silo).where(SiloRegionMapping.region == region)
                results = session.exec(statement)  

                srm = results.first()

                if srm == None:
                    srm = SiloRegionMapping(silo=silo, region=region)
                    session.add(srm)
                    session.commit()
    return


@app.cell
def global_rights(
    ScoreEntry,
    Session,
    engine,
    global_rights_azure_regions,
    insert,
    silos,
):
    global_rights_data = []

    for siloi, regionsi in silos.items():
        silo_spec = global_rights_azure_regions[global_rights_azure_regions["Region"].isin(regionsi)]

        for index, row in silo_spec.iterrows():

            global_rights_data.append(ScoreEntry(
                silo=siloi,
                region=row["Region"], 
                kpi="global_rights", 
                value=row["Rating"], 
                index=0,
                tot_values=silo_spec['Rating'].count(),
                average=silo_spec['Rating'].mean(),
                median=silo_spec['Rating'].median(),
            ))
        print(f"global_rights, {siloi}, count={silo_spec['Rating'].count()}, median={silo_spec['Rating'].median()}, max={silo_spec['Rating'].max()}, min={silo_spec['Rating'].min()}, avg={silo_spec['Rating'].mean()}")

    with Session(engine) as grsession:
        grsession.exec(insert(ScoreEntry), params=global_rights_data)

        grsession.commit()
    return


@app.cell
def _(ScoreEntry, Session, azure_carbon_intensity, engine, insert, silos):
    import math
    co2i_data = []

    for siloc, regionsc in silos.items():
        silo_spec_co2 = azure_carbon_intensity[azure_carbon_intensity["region"].isin(regionsc)]

        silo_spec_co2["rank"] = silo_spec_co2["carbon_intensity_avg24h"].rank(ascending=True)

        for indexc, rowc in silo_spec_co2.iterrows():

            if not math.isnan(rowc["carbon_intensity_avg24h"]):
                co2i_data.append(ScoreEntry(
                    silo=siloc,
                    region=rowc["region"], 
                    kpi="carbon_intensity", 
                    value=rowc["carbon_intensity_avg24h"], 
                    index=rowc["rank"],
                    tot_values=silo_spec_co2['region'].count(),
                    average=silo_spec_co2['carbon_intensity_avg24h'].mean(),
                    median=silo_spec_co2['carbon_intensity_avg24h'].median(),
                ))
        print(f"co2i, {siloc}, count={silo_spec_co2['region'].count()}, median={silo_spec_co2['carbon_intensity_avg24h'].median()}, max={silo_spec_co2['carbon_intensity_avg24h'].max()}, min={silo_spec_co2['carbon_intensity_avg24h'].min()}, avg={silo_spec_co2['carbon_intensity_avg24h'].mean()}")

    with Session(engine) as cosession:
        cosession.exec(insert(ScoreEntry), params=co2i_data)

        cosession.commit()
    return math, regionsc


@app.cell
def _(
    ScoreEntry,
    Session,
    engine,
    ged_azure_agg,
    insert,
    math,
    regionsc,
    silos,
):
    ged_data = []

    for silog in silos:
        silo_spec_ged = ged_azure_agg[ged_azure_agg["az_region"].isin(regionsc)]

        silo_spec_ged["rank"] = silo_spec_ged["total_events"].rank(ascending=True)

        for indexg, rowg in silo_spec_ged.iterrows():

            if not math.isnan(rowg["total_events"]):
                ged_data.append(ScoreEntry(
                    silo=silog,
                    region=rowg["az_region"], 
                    kpi="armed_conflict", 
                    value=rowg["total_events"], 
                    index=rowg["rank"],
                    tot_values=silo_spec_ged['az_region'].count(),
                    average=silo_spec_ged['total_events'].mean(),
                    median=silo_spec_ged['total_events'].median(),
                ))
        print(f"co2i, {silog}, count={silo_spec_ged['az_region'].count()}, median={silo_spec_ged['total_events'].median()}, max={silo_spec_ged['total_events'].max()}, min={silo_spec_ged['total_events'].min()}, avg={silo_spec_ged['total_events'].mean()}")

    with Session(engine) as gedsession:
        gedsession.exec(insert(ScoreEntry), params=ged_data)

        gedsession.commit()
    return


@app.cell
def _(
    ScoreEntry,
    Session,
    engine,
    insert,
    math,
    region_temperatures_sweatscore,
    silos,
):
    sweat_data = []

    for silosw, regionss in silos.items():
        silo_spec_sweat = region_temperatures_sweatscore[region_temperatures_sweatscore["Region"].isin(regionss)]

        silo_spec_sweat["rank"] = silo_spec_sweat["SweatScore"].rank(ascending=True)

        for indexs, rows in silo_spec_sweat.iterrows():

            if not math.isnan(rows["SweatScore"]):
                sweat_data.append(ScoreEntry(
                    silo=silosw,
                    region=rows["Region"], 
                    kpi="sweat_score", 
                    value=rows["SweatScore"], 
                    index=rows["rank"],
                    tot_values=silo_spec_sweat['Region'].count(),
                    average=silo_spec_sweat['SweatScore'].mean(),
                    median=silo_spec_sweat['SweatScore'].median(),
                ))
        print(f"co2i, {silosw}, count={silo_spec_sweat['Region'].count()}, median={silo_spec_sweat['SweatScore'].median()}, max={silo_spec_sweat['SweatScore'].max()}, min={silo_spec_sweat['SweatScore'].min()}, avg={silo_spec_sweat['SweatScore'].mean()}")

    with Session(engine) as sweat_session:
        sweat_session.exec(insert(ScoreEntry), params=sweat_data)

        sweat_session.commit()
    return


@app.cell
def _(gdacs_events):
    gdacs_events.groupby('region').agg(total=('eventid','count'))
    return


if __name__ == "__main__":
    app.run()
