import numpy as np
import pandas as pd
import json

EARTH_RADIUS_KM = 6371.0088


def _haversine_km(lat1, lon1, lat2, lon2):
    """Vectorized haversine distance in kilometers."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(a))


def load_ged_events(csv_path="GEDEvent_v26_1.csv",
                    point=None,
                    radius_km=100,
                    start_year=None):
    """
    Load UCDP GED events and filter by location and time.

    Parameters
    ----------
    csv_path : str
        Path to the GEDEvent_v26_1.csv file.
    point : tuple(float, float) or None
        Geolocation as (latitude, longitude). If None, no location filter.
    radius_km : float
        Radius in kilometers around `point` (default 100).
    start_year : int or None
        Only return events occurring in this calendar year or later.
        If None, no time filter.

    Returns
    -------
    pandas.DataFrame
        Matching events (one row per event).
    """
    df = pd.read_csv(csv_path, low_memory=False)

    # Drop rows without usable coordinates
    df = df.dropna(subset=["latitude", "longitude"])

    # --- Temporal filter ---
    if start_year is not None:
        df = df[df["year"] >= start_year]

    # --- Spatial filter ---
    if point is not None:
        lat0, lon0 = point
        dist = _haversine_km(lat0, lon0,
                             df["latitude"].to_numpy(),
                             df["longitude"].to_numpy())
        df = df[dist <= radius_km]

    return df

def load_az_regions(json_path="az_regions.json"):
    """
    Load Azure regions from the `az account list-locations`-style JSON.
    Returns a DataFrame with columns:
    name, displayName, latitude, longitude, physicalLocation, geography.
    Regions without coordinates (metadata missing/empty) are skipped.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        regions = json.load(f)

    rows = []
    for r in regions:
        meta = r.get("metadata") or {}
        lat, lon = meta.get("latitude"), meta.get("longitude")
        if lat is None or lon is None:
            continue  # e.g. logical regions without a physical location
        rows.append({
            "name": r["name"],
            "displayName": r.get("displayName"),
            "physicalLocation": meta.get("physicalLocation"),
            "geography": meta.get("geography"),
            "latitude": float(lat),
            "longitude": float(lon),
        })
    return pd.DataFrame(rows)

def events_by_az_region(ged_csv="GEDEvent_v26_1.csv",
                        az_json="az_regions.json",
                        radius_km=100,
                        start_year=2020):
    """
    For every Azure region centroid, return the GED events that overlap
    with the region's radius (default 100 km) and occurred in `start_year`
    or later.

    Returns a DataFrame of all matching events with an added column
    `az_region` naming the matched Azure region. An event can appear
    multiple times if it falls within radius of several regions.
    """
    regions = load_az_regions(az_json)
    ged = load_ged_events(ged_csv, start_year=start_year)

    if regions.empty or ged.empty:
        return pd.DataFrame(columns=ged.columns.tolist() + ["az_region"])

    ev_lat = ged["latitude"].to_numpy()
    ev_lon = ged["longitude"].to_numpy()

    matched = []
    for _, region in regions.iterrows():
        dist = _haversine_km(region["latitude"], region["longitude"],
                             ev_lat, ev_lon)
        hits = ged[dist <= radius_km]
        if not hits.empty:
            hits = hits.copy()
            hits["az_region"] = region["name"]
            hits["distance_km"] = dist[dist <= radius_km]
            matched.append(hits)

    if not matched:
        return pd.DataFrame(columns=ged.columns.tolist() + ["az_region"])

    return pd.concat(matched, ignore_index=True)

def aggregate_events_by_region(events_df):
    """
    Aggregate events returned by events_by_az_region per Azure region.

    Parameters
    ----------
    events_df : pandas.DataFrame
        Output of events_by_az_region (must contain 'az_region'
        and 'type_of_violence' columns).

    Returns
    -------
    pandas.DataFrame
        One row per Azure region with columns:
        az_region, total_events, type_1_state_based,
        type_2_non_state, type_3_one_sided.
        Regions are sorted by total_events (descending).
    """
    type_labels = {
        1: "type_1_state_based",
        2: "type_2_non_state",
        3: "type_3_one_sided",
    }

    if events_df is None or events_df.empty:
        return pd.DataFrame(columns=["az_region", "total_events",
                                     *type_labels.values()])

    agg = (events_df
           .groupby("az_region")["type_of_violence"]
           .value_counts()
           .unstack(fill_value=0)          # columns: 1, 2, 3
           .reindex(columns=[1, 2, 3], fill_value=0)  # ensure all types present
           .astype(int))

    agg = agg.rename(columns=type_labels)
    agg["total_events"] = agg.sum(axis=1)
    agg = (agg.reset_index()
              .sort_values("total_events", ascending=False)
              .reset_index(drop=True))

    return agg


if __name__ == "__main__":
	events = events_by_az_region()
	events.to_csv("ged-azure.csv")

	agg = aggregate_events_by_region(events)
	agg.to_csv("ged-azure-agg.csv")
