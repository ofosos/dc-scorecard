#!/usr/bin/env python3
"""Spatial matching of UCDP GED events to Azure regions with GeoPandas.

The custom haversine point/circle intersection was replaced by GeoPandas
algorithms:

  - `filter_events_by_distance` performs the point/circle intersection
    with `geopandas.sjoin` (`predicate="within"`) against a geodesic
    circle around the query point;
  - `events_by_az_region` buffers every Azure region centroid into a
    geodesic circle and assigns all events with a single spatial join.

The circles are true WGS84 geodesic circles: the boundary points are
placed on the ellipsoid with `pyproj.Geod.fwd` (geodesic densification),
so the radius is correct at every latitude without any planar projection.
Distances in the `distance_km` column are computed with `pyproj.Geod.inv`,
the WGS84 geodesic inverse, replacing the haversine approximation.

Dependencies: geopandas, pandas, pyproj
"""

import json
import math

import geopandas as gpd
import pandas as pd
from pyproj import Geod
from shapely.geometry import Polygon

GEOD = Geod(ellps="WGS84")

WGS84 = "EPSG:4326"

# Maximum inward deviation (meters) of the densified circle boundary from
# the true geodesic circle. 100 m is well below the coordinate precision
# of the event data.
DEFAULT_CIRCLE_TOLERANCE_METERS = 100


def geodesic_circle(lon, lat, radius_km,
                    tolerance_m=DEFAULT_CIRCLE_TOLERANCE_METERS):
    """Build a Shapely Polygon approximating a WGS84 geodesic circle.

    The boundary is densified geodesically: `pyproj.Geod.fwd` projects
    boundary points from the center at evenly spaced azimuths and the
    geodesic distance radius_km, so the circle follows the ellipsoid
    instead of a planar projection. The number of boundary points is
    chosen so the polygon stays within tolerance_m of the true geodesic
    circle. The polygon is valid for the default 100 km radius; circles
    wide enough to wrap the antimeridian are not supported (no Azure
    region is affected).
    """
    radius_m = radius_km * 1000.0
    tol = min(float(tolerance_m), radius_m)
    half_angle = 2 * math.asin(math.sqrt(tol / (2 * radius_m)))
    n = max(int(math.ceil(math.pi / half_angle)), 8)
    azimuths = [360.0 * i / n for i in range(n)]
    lons, lats, _ = GEOD.fwd([float(lon)] * n, [float(lat)] * n,
                             azimuths, [radius_m] * n)
    return Polygon(zip(lons, lats))


def events_geodataframe(df):
    """Convert a DataFrame with latitude/longitude columns to a
    GeoDataFrame of WGS84 points (a copy; the geometry column is last)."""
    return gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=WGS84)


def filter_events_by_distance(df, point, radius_km,
                              tolerance_m=DEFAULT_CIRCLE_TOLERANCE_METERS):
    """Return the rows of `df` within `radius_km` (geodesic) of `point`.

    Parameters
    ----------
    df : pandas.DataFrame with "latitude" and "longitude" columns.
    point : (latitude, longitude) tuple or None. If None, `df` is
        returned unchanged.
    radius_km : float
        Geodesic radius of the circle around `point`.

    Notes
    -----
    GeoPandas point/circle intersection: events are joined to the
    geodesic circle with `geopandas.sjoin` and `predicate="within"`.
    """
    if point is None:
        return df
    events = events_geodataframe(df)
    circle = gpd.GeoDataFrame(geometry=[geodesic_circle(point[1], point[0],
                                                        radius_km,
                                                        tolerance_m)],
                              crs=WGS84)
    hits = gpd.sjoin(events, circle, how="inner", predicate="within")
    return hits.drop(columns=["index_right", "geometry"])


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

    # --- Spatial filter (GeoPandas point/circle intersection) ---
    return filter_events_by_distance(df, point, radius_km)


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

    Returns a DataFrame of all matching events with added columns
    `az_region` naming the matched Azure region and `distance_km`, the
    WGS84 geodesic distance from the event to the region centroid. An
    event can appear multiple times if it falls within radius of several
    regions.

    GeoPandas algorithm: every region centroid becomes a geodesic circle
    and all events are assigned in one `geopandas.sjoin` spatial join
    (`predicate="within"`), replacing the per-region haversine loop.
    """
    regions = load_az_regions(az_json)
    ged = load_ged_events(ged_csv, start_year=start_year)

    if regions.empty or ged.empty:
        return pd.DataFrame(columns=ged.columns.tolist() +
                            ["az_region", "distance_km"])

    region_circles = gpd.GeoDataFrame(
        regions[["name"]].rename(columns={"name": "az_region"}),
        geometry=[geodesic_circle(lon, lat, radius_km)
                  for lon, lat in zip(regions["longitude"],
                                      regions["latitude"])],
        crs=WGS84)
    events = events_geodataframe(ged).assign(_event_order=range(len(ged)))

    joined = gpd.sjoin(events, region_circles, how="inner", predicate="within")

    # Keep the historical row order: region order, then event order.
    joined = joined.sort_values(["index_right", "_event_order"])

    # WGS84 geodesic distance per matched (event, region) pair.
    region_lon = dict(zip(regions["name"], regions["longitude"]))
    region_lat = dict(zip(regions["name"], regions["latitude"]))
    _, _, dist_m = GEOD.inv(joined["longitude"].to_numpy(),
                            joined["latitude"].to_numpy(),
                            joined["az_region"].map(region_lon).to_numpy(),
                            joined["az_region"].map(region_lat).to_numpy())
    joined["distance_km"] = dist_m / 1000.0

    drop = [c for c in ["index_right", "geometry", "_event_order"]
            if c in joined.columns]
    return joined.drop(columns=drop).reset_index(drop=True)


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
