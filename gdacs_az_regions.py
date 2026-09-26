#!/usr/bin/env python3
"""Map GDACS events to Azure regions by circle overlap.

Fetches recent GDACS events (default back to 2021-01-01) from the official
GDACS API (https://www.gdacs.org/gdacsapi/swagger/index.html), resolves the
real event geometry via /api/Polygons/getgeometry whenever the search
endpoint only returns a centroid (Class == "Point_Centroid" or a bare Point
geometry), and assigns each event to every Azure region whose radius circle
(default 100 km) around the region coordinates overlaps the event geometry.
Events that overlap multiple region circles are assigned to all of them.

The geodata processing uses GeoPandas algorithms: event geometries are
parsed with Shapely, each Azure region becomes a true WGS84 geodesic
circle (built by geodesic densification with pyproj.Geod) and the
circle-polygon overlap test is a single geopandas.sjoin spatial join
with predicate="intersects".

Usage
-----

    python3 gdacs_az_regions.py            # since 2021-01-01, all event
                                            # types, yellow+red alerts
    python3 gdacs_az_regions.py --event-types floods droughts \
        --start-date 2025-01-01 --end-date 2026-09-20 \
        --radius-km 150 --output my_regions.json

CLI options:
  --regions-file  Azure regions JSON (default az_regions_annotated.json;
                  `az account list-locations` output or a dict keyed by
                  programmatic region name with latitude/longitude)
  --output        Output JSON (default gdacs_events_by_region.json)
  --error-log     Error log (default <output>.error.log)
  --start-date    Time window start (default 2021-01-01)
  --end-date      Time window end (default: now)
  --event-types   Friendly names (earthquakes, cyclones, floods, volcanoes,
                  droughts, wildfires) or GDACS codes (EQ TC FL VO DR WF);
                  default: all
  --alert-levels  green, yellow (GDACS "orange"), red, orange;
                  default: yellow red
  --radius-km    Region circle radius (default 100)
  --max-events    Cap number of events (testing)
  -v              Verbose logging

The GDACSClient class can also be used programmatically:

    from gdacs_az_regions import GDACSClient

    client = GDACSClient(
        start_date="2021-01-01",            # or a datetime
        end_date=None,                       # default: now
        event_types=["floods", "volcanoes"],  # or ["FL", "VO"], default: all
        alert_levels=["yellow", "red"],       # "yellow" maps to GDACS orange
    )
    events = client.search_events()  # paged until exhausted

Output
------

gdacs_events_by_region.json is keyed by the programmatic Azure region name;
each value is the list of GDACS events matching that region (type, ids,
name, alert level, dates, countries, severity, geometry source, urls and
the full list of matched regions).

API usage (per the official swagger / gdac-swagger.json)
-------------------------------------------------------

  - GET /api/Events/geteventlist/search
      params: eventlist (e.g. "EQ;FL;DR;VO;TC;WF"), alertlevel (e.g.
      "green;orange;red"), fromDate, toDate (date-time), pageSize (max 100),
      pageNumber. Returns a GeoJSON FeatureCollection; empty result sets are
      served as HTTP 204 with an empty body, which is handled and logged.
  - GET /api/Polygons/getgeometry
      params: eventtype, eventid, episodeid. Returns the true polygonal
      geometry of the event (centroid, affected area, intensity zones, ...).
      The search endpoint only returns a centroid, so this endpoint supplies
      the geometry the circle-overlap test runs against.
  - GET /api/Events/geteventdata
      params: eventtype, eventid. Fallback source of the url.geometry link.

Any API response that is expected to be JSON but isn't (e.g. HTTP 204 with
an empty body) is logged and its raw non-conforming text is dumped into the
error log.

Dependencies: geopandas, pandas, requests
"""

import argparse
import json
import logging
import math
import sys
from datetime import datetime, timezone

import geopandas as gpd
import pandas as pd
import requests
from pyproj import Geod
from shapely.geometry import Point, Polygon, shape
from shapely.ops import nearest_points

DEFAULT_BASE_URL = "https://www.gdacs.org/gdacsapi/api"
DEFAULT_START_DATE = "2021-01-01"
DEFAULT_RADIUS_KM = 100.0
DEFAULT_ALERT_LEVELS = ["yellow", "red"]
DEFAULT_EVENT_TYPES = ["EQ", "TC", "FL", "VO", "DR", "WF"]

# Friendly event type names accepted by the client / CLI.
EVENT_TYPE_NAMES = {
    "earthquake": "EQ", "earthquakes": "EQ", "eq": "EQ",
    "cyclone": "TC", "cyclones": "TC", "tropicalcyclone": "TC",
    "storm": "TC", "storms": "TC", "tc": "TC",
    "flood": "FL", "floods": "FL", "fl": "FL",
    "volcano": "VO", "volcanoes": "VO", "volcanic": "VO", "vo": "VO",
    "drought": "DR", "droughts": "DR", "dr": "DR",
    "wildfire": "WF", "wildfires": "WF", "fire": "WF", "fires": "WF",
    "forestfire": "WF", "forestfires": "WF", "wf": "WF",
}

# GDACS only knows Green / Orange / Red alert levels.
ALERT_LEVEL_ALIASES = {
    "green": ["green"],
    "yellow": ["orange"],
    "orange": ["orange"],
    "red": ["red"],
}

WGS84 = "EPSG:4326"

# WGS84 geodesic used for circle densification and distance measurement.
GEOD = Geod(ellps="WGS84")

# Maximum inward deviation (meters) of the densified circle boundary from
# the true geodesic circle. 100 m is far below the ~1 km accuracy of the
# GDACS event polygons.
DEFAULT_CIRCLE_TOLERANCE_METERS = 100

logger = logging.getLogger("gdacs_az")


# ---------------------------------------------------------------------------
# GDACS API client
# ---------------------------------------------------------------------------

class GDACSClient:
    """Client for the official GDACS API.

    Options:
      - start_date / end_date: restrict the event time window (datetime or
        ISO date strings). end_date defaults to "now".
      - event_types: restrict to GDACS event type codes, e.g.
        ["EQ", "TC", "FL", "VO", "DR", "WF"] (earthquakes, tropical
        cyclones, floods, volcanoes, droughts, wildfires).
      - alert_levels: restrict to GDACS alert levels; accepts the common
        alias "yellow" which GDACS calls "orange". Default ["yellow", "red"].
    """

    EVENT_TYPES = DEFAULT_EVENT_TYPES
    PAGE_SIZE = 100  # swagger: "Max 100"

    def __init__(self, base_url=DEFAULT_BASE_URL, timeout=60, max_retries=3,
                 start_date=DEFAULT_START_DATE, end_date=None,
                 event_types=None, alert_levels=None, session=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = session or requests.Session()
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)
        self.event_types = self._normalize_event_types(event_types)
        self.alert_levels = self._normalize_alert_levels(alert_levels)

    # -- option normalization ---------------------------------------------

    @staticmethod
    def _parse_date(value):
        if value in (None, ""):
            return None
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(str(value)[:len(fmt) + 2], fmt)
            except ValueError:
                continue
        raise ValueError(f"Unparseable date: {value!r}")

    @staticmethod
    def _normalize_event_types(event_types):
        if not event_types:
            return list(GDACSClient.EVENT_TYPES)
        codes = []
        for item in event_types:
            for code in str(item).replace(",", ";").split(";"):
                code = code.strip()
                if not code:
                    continue
                mapped = EVENT_TYPE_NAMES.get(code.lower(), code.upper())
                if mapped not in codes:
                    codes.append(mapped)
        return codes

    @staticmethod
    def _normalize_alert_levels(alert_levels):
        if not alert_levels:
            alert_levels = DEFAULT_ALERT_LEVELS
        levels = []
        for item in alert_levels:
            for level in str(item).replace(",", ";").split(";"):
                level = level.strip().lower()
                if not level:
                    continue
                for mapped in ALERT_LEVEL_ALIASES.get(level, [level]):
                    if mapped not in levels:
                        levels.append(mapped)
        return levels

    # -- low-level helpers --------------------------------------------------

    def _get(self, url, params=None, expect_json=True, description="request"):
        """GET with retries. Any response that is expected to be JSON but is
        not parseable JSON (e.g. empty 204 bodies or HTML error pages) is
        dumped verbatim into the error log."""
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
                if resp.status_code in (429, 500, 502, 503, 504):
                    last_exc = requests.HTTPError(
                        f"{description}: HTTP {resp.status_code}")
                    logger.warning("%s: HTTP %s (attempt %d/%d)",
                                   description, resp.status_code, attempt,
                                   self.max_retries)
                    continue
                if expect_json:
                    return self._decode_json(resp, description)
                return resp
            except requests.RequestException as exc:
                last_exc = exc
                logger.warning("%s: %s (attempt %d/%d)", description, exc,
                               attempt, self.max_retries)
        raise last_exc or requests.RequestException(
            f"{description}: retries exhausted")

    def _decode_json(self, resp, description):
        content_type = (resp.headers.get("content-type") or "").lower()
        body = resp.text or ""
        if resp.status_code == 204 or not body.strip():
            # GDACS signals "no results" with 204 + empty body: not an error,
            # but it is a non-JSON response where JSON is expected, so log it.
            logger.debug("%s: empty non-JSON response (HTTP %d, %d bytes)",
                         description, resp.status_code, len(body))
            return None
        try:
            return resp.json()
        except (ValueError, requests.exceptions.JSONDecodeError):
            logger.error(
                "%s: expected JSON but got non-JSON response "
                "(HTTP %d, content-type=%s). Raw body follows:\n%s",
                description, resp.status_code, content_type, body[:5000])
            return None

    # -- API operations ------------------------------------------------------

    def search_events(self):
        """GET /api/Events/geteventlist/search with paging until exhausted.

        Returns a list of event property dicts, one per GDACS event."""
        params = {
            "eventlist": ";".join(self.event_types),
            "alertlevel": ";".join(self.alert_levels),
            "pageSize": self.PAGE_SIZE,
            "pageNumber": 1,
        }
        if self.start_date:
            params["fromDate"] = self.start_date.strftime("%Y-%m-%dT%H:%M:%S")
        if self.end_date:
            params["toDate"] = self.end_date.strftime("%Y-%m-%dT%H:%M:%S")

        events = []
        page = 1
        while True:
            params["pageNumber"] = page
            data = self._get(
                f"{self.base_url}/Events/geteventlist/search",
                params=params,
                description=f"event search page {page}",
            )
            if data is None:
                logger.info("Search exhausted (no JSON) at page %d", page)
                break
            features = data.get("features", []) if isinstance(data, dict) else []
            if not features:
                logger.info("Search exhausted at page %d (0 features)", page)
                break
            for feature in features:
                props = feature.get("properties", {})
                props["_search_geometry"] = feature.get("geometry")
                events.append(props)
            logger.info("Search page %d: %d events", page, len(features))
            if len(features) < self.PAGE_SIZE:
                break
            page += 1
        return events

    def get_event_data(self, eventtype, eventid):
        """GET /api/Events/geteventdata — fallback source for url.geometry."""
        data = self._get(
            f"{self.base_url}/Events/geteventdata",
            params={"eventtype": eventtype, "eventid": eventid},
            description=f"event data {eventtype}/{eventid}",
        )
        if isinstance(data, dict):
            return data.get("properties", data)
        return None

    def get_geometry(self, eventtype, eventid, episodeid):
        """GET /api/Polygons/getgeometry — the true event geometry.

        Returns a list of GeoJSON features (centroid, affected area,
        intensity polygons, ...)."""
        data = self._get(
            f"{self.base_url}/Polygons/getgeometry",
            params={"eventtype": eventtype, "eventid": eventid,
                    "episodeid": episodeid},
            description=f"geometry {eventtype}/{eventid}/{episodeid}",
        )
        if isinstance(data, dict):
            return data.get("features", [])
        return []


# ---------------------------------------------------------------------------
# Geometry helpers (GeoPandas / Shapely)
# ---------------------------------------------------------------------------

def geometry_from_geojson(geometry):
    """Parse a GeoJSON geometry dict into a Shapely geometry (WGS84 lon/lat
    coordinate order). Returns None for empty/missing geometry."""
    try:
        geom = shape(geometry)
        return None if geom.is_empty else geom
    except (AttributeError, ValueError, TypeError):
        return None


def is_bare_point(feature_geometry, props):
    """True when the search/geteventdata result only carries a centroid:
    properties Class == 'Point_Centroid' or the geometry is a bare Point."""
    if isinstance(props, dict) and str(props.get("Class", "")).strip().lower() \
            == "point_centroid":
        return True
    if isinstance(feature_geometry, dict) \
            and feature_geometry.get("type") == "Point":
        return True
    return False


def geodesic_circle(center_lon, center_lat, radius_km,
                    tolerance_m=DEFAULT_CIRCLE_TOLERANCE_METERS):
    """Build a Shapely Polygon approximating a WGS84 geodesic circle.

    The boundary is densified geodesically: `pyproj.Geod.fwd` projects
    boundary points from the center at evenly spaced azimuths and the
    geodesic distance radius_km, so the circle follows the ellipsoid and
    its radius is correct at every latitude. The number of boundary
    points is chosen so the polygon stays within tolerance_m of the true
    geodesic circle. Circles wide enough to wrap the antimeridian are
    not supported (no Azure region is affected).
    """
    radius_m = radius_km * 1000.0
    tol = min(float(tolerance_m), radius_m)
    half_angle = 2 * math.asin(math.sqrt(tol / (2 * radius_m)))
    n = max(int(math.ceil(math.pi / half_angle)), 8)
    azimuths = [360.0 * i / n for i in range(n)]
    lons, lats, _ = GEOD.fwd([float(center_lon)] * n,
                             [float(center_lat)] * n,
                             azimuths, [radius_m] * n)
    return Polygon(zip(lons, lats))


def geodesic_distance_km(lon1, lat1, lon2, lat2):
    """WGS84 geodesic distance in kilometers between two points, computed
    with pyproj.Geod.inv (replaces the haversine approximation)."""
    _, _, dist_m = GEOD.inv(lon1, lat1, lon2, lat2)
    return dist_m / 1000.0


def geodesic_distance_to_geometry_km(lon, lat, geom):
    """WGS84 geodesic distance in kilometers from a point to the nearest
    point of a Shapely geometry (0 when the point is inside it). Uses
    shapely.ops.nearest_points to pick the closest point and pyproj.Geod
    for the distance, replacing the custom segment-distance code."""
    point = Point(float(lon), float(lat))
    if geom.covers(point):
        return 0.0
    near = nearest_points(geom, point)[0]
    return geodesic_distance_km(lon, lat, near.x, near.y)


def resolve_event_geometry(client, props):
    """Resolve the true geometry of an event.

    If /search (or geteventdata) returned a real polygon, use it directly.
    If it only returned a centroid (Class == "Point_Centroid" or a bare
    Point geometry), follow the event's url.geometry link
    (/api/Polygons/getgeometry) to fetch the actual polygon, and test the
    circle overlap against that.

    Returns (geometry, source) where geometry is a Shapely geometry in
    WGS84 (lon/lat) coordinates."""
    eventtype = props.get("eventtype")
    eventid = props.get("eventid")
    episodeid = props.get("episodeid")
    search_geom = props.get("_search_geometry")

    if not is_bare_point(search_geom, props):
        geom = geometry_from_geojson(search_geom)
        if geom is not None and not isinstance(geom, Point):
            return geom, "search-polygon"

    # Only a centroid: follow url.geometry (fall back to geteventdata).
    geom_url = None
    urls = props.get("url")
    if isinstance(urls, dict):
        geom_url = urls.get("geometry")
    if not geom_url and episodeid is not None:
        detail = client.get_event_data(eventtype, eventid)
        if isinstance(detail, dict):
            urls = detail.get("url")
            if isinstance(urls, dict):
                geom_url = urls.get("geometry")
    if not geom_url:
        geom_url = (f"{client.base_url}/Polygons/getgeometry"
                    f"?eventtype={eventtype}&eventid={eventid}"
                    f"&episodeid={episodeid}")

    features = client.get_geometry(eventtype, eventid, episodeid)
    if not features and geom_url:
        resp = client._get(geom_url, expect_json=True,
                           description=f"geometry link {eventtype}/{eventid}")
        features = resp.get("features", []) if isinstance(resp, dict) else []

    # Prefer the actual area polygons, skip the centroid and global layers.
    best = None
    for feat in features or []:
        fprops = feat.get("properties", {})
        fclass = str(fprops.get("Class", ""))
        geom_dict = feat.get("geometry", {})
        if geom_dict.get("type") == "Point":
            continue
        if fclass.startswith("Poly_Global"):
            continue
        geom = geometry_from_geojson(geom_dict)
        if geom is None or isinstance(geom, Point):
            continue
        if fclass in ("Poly_area", "Poly_Affected"):
            best = geom
            break
        if fclass.startswith("Poly_Circle"):
            best = best or geom
        elif "SMPInt" in fclass:
            best = best or geom
        elif best is None:
            best = geom
    if best is None:
        for feat in features or []:
            geom_dict = feat.get("geometry", {})
            if geom_dict.get("type") != "Point":
                geom = geometry_from_geojson(geom_dict)
                if geom is not None and not isinstance(geom, Point):
                    best = geom
                    break
    if best is None:
        # Fall back to the centroid itself as a zero-area geometry.
        geom = geometry_from_geojson(search_geom) if search_geom else None
        if geom is not None:
            return geom, "centroid-only"
        return None, "no-geometry"
    return best, "getgeometry-polygon"


# ---------------------------------------------------------------------------
# Region matching
# ---------------------------------------------------------------------------

def match_events_to_regions(client, regions, radius_km, events=None,
                            verbose=True):
    """Assign each GDACS event to every region whose radius circle overlaps
    the event geometry. Returns (output dict, per-event summary DataFrame).

    GeoPandas algorithm: every Azure region centroid is buffered into a
    true WGS84 geodesic circle (pyproj.Geod densification) and all
    event geometries are joined to the circles with one geopandas.sjoin
    spatial join (predicate="intersects"), replacing the custom
    haversine / ray-casting / segment-distance overlap test.
    """
    if events is None:
        events = client.search_events()
    logger.info("Fetched %d GDACS events", len(events))

    region_names = list(regions.keys())
    region_circles = gpd.GeoDataFrame(
        {"region": region_names},
        geometry=[geodesic_circle(regions[name]["longitude"],
                                  regions[name]["latitude"],
                                  radius_km)
                  for name in region_names],
        crs=WGS84)

    resolved = []
    rows = []
    for idx, props in enumerate(events, 1):
        eventtype = props.get("eventtype")
        eventid = props.get("eventid")
        label = f"{eventtype}/{eventid}"
        geom, source = resolve_event_geometry(client, props)
        if geom is None or geom.is_empty:
            logger.warning("%s: no usable geometry; skipping", label)
            rows.append({"eventtype": eventtype, "eventid": eventid,
                         "name": props.get("name", ""),
                         "matched_regions": 0, "geometry_source": source,
                         "min_distance_km": None})
            continue
        resolved.append((idx, props, geom, source))

    if resolved:
        event_geoms = gpd.GeoDataFrame(
            {"event_idx": [r[0] for r in resolved],
             "eventtype": [r[1].get("eventtype") for r in resolved],
             "eventid": [r[1].get("eventid") for r in resolved]},
            geometry=[r[2] for r in resolved],
            crs=WGS84)
        joined = gpd.sjoin(event_geoms, region_circles, how="left",
                            predicate="intersects")
    else:
        joined = gpd.GeoDataFrame(columns=["event_idx", "eventtype",
                                           "eventid", "region", "geometry"],
                                   crs=WGS84)

    matches_by_idx = {}
    for row in joined.itertuples():
        region = getattr(row, "region", None)
        if region is None or (isinstance(region, float) and math.isnan(region)):
            continue
        matches_by_idx.setdefault(row.event_idx, []).append(region)

    output = {name: [] for name in region_names}
    for idx, props, geom, source in resolved:
        eventtype = props.get("eventtype")
        eventid = props.get("eventid")
        label = f"{eventtype}/{eventid}"
        matched = [name for name in region_names
                  if name in matches_by_idx.get(idx, [])]

        min_dist = float("inf")
        for rname in matched:
            dist = geodesic_distance_to_geometry_km(
                regions[rname]["longitude"], regions[rname]["latitude"],
                geom)
            if dist < min_dist:
                min_dist = dist

        event_summary = {
            "eventtype": eventtype,
            "eventid": eventid,
            "episodeid": props.get("episodeid"),
            "eventname": props.get("eventname"),
            "name": props.get("name"),
            "description": props.get("description"),
            "alertlevel": props.get("alertlevel"),
            "alertscore": props.get("alertscore"),
            "fromdate": props.get("fromdate"),
            "todate": props.get("todate"),
            "country": props.get("country"),
            "iso3": props.get("iso3"),
            "severitydata": props.get("severitydata"),
            "glide": props.get("glide"),
            "geometry_source": source,
            "url_geometry": (props.get("url") or {}).get("geometry"),
            "url_report": (props.get("url") or {}).get("report"),
            "matched_azure_regions": matched,
        }
        for rname in matched:
            output[rname].append(event_summary)

        rows.append({"eventtype": eventtype, "eventid": eventid,
                     "name": props.get("name", ""),
                     "matched_regions": len(matched),
                     "geometry_source": source,
                     "min_distance_km": None if min_dist == float("inf")
                     else round(min_dist, 1)})
        if verbose:
            logger.info("%s (%s): matched %d region(s)%s", label, source,
                        len(matched),
                        f" {matched}" if len(matched) <= 8 else "")

    df = pd.DataFrame(rows)
    return output, df


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_regions(path):
    """Load Azure regions from `az_regions_annotated.json`.

    Two formats are supported:
      - list of `az account list-locations` entries (the format in this
        repository): each item has "name" and
        "metadata"{"latitude", "longitude"};
      - a dict keyed by programmatic region name with
        "latitude"/"longitude" values.

    Returns a dict: programmatic region name -> {latitude, longitude}.
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    regions = {}
    if isinstance(data, dict):
        for name, entry in data.items():
            lat = entry.get("latitude")
            lon = entry.get("longitude")
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                regions[name] = {"latitude": lat, "longitude": lon}
        return regions

    if isinstance(data, list):
        for entry in data:
            name = entry.get("name")
            meta = entry.get("metadata") or {}
            lat = meta.get("latitude")
            lon = meta.get("longitude")
            if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
                logger.warning("Region %s has no usable coordinates; skipping",
                                name)
                continue
            regions[name] = {"latitude": lat, "longitude": lon}
        return regions

    raise ValueError(f"Unsupported regions file structure in {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Map GDACS events to Azure regions by circle overlap.")
    parser.add_argument("--regions-file", default="az_regions_annotated.json",
                        help="JSON file with Azure regions; either `az "
                             "account list-locations` output or a dict keyed "
                             "by region name (default: "
                             "az_regions_annotated.json)")
    parser.add_argument("--output", default="gdacs_events_by_region.json",
                        help="Output JSON file")
    parser.add_argument("--error-log", default=None,
                        help="Error log file (default: <output>.error.log)")
    parser.add_argument("--start-date", default=DEFAULT_START_DATE,
                        help="Start date, default 2021-01-01")
    parser.add_argument("--end-date", default=None,
                        help="End date, default: now")
    parser.add_argument("--event-types", nargs="*", default=None,
                        help="GDACS event types: friendly names (earthquakes, "
                             "cyclones, floods, volcanoes, droughts, "
                             "wildfires) or codes (EQ TC FL VO DR WF); "
                             "default: all")
    parser.add_argument("--alert-levels", nargs="*", default=None,
                        help="Alert levels, e.g. yellow red green orange "
                             "(default: yellow red)")
    parser.add_argument("--radius-km", type=float, default=DEFAULT_RADIUS_KM,
                        help="Region circle radius in km (default: 100)")
    parser.add_argument("--max-events", type=int, default=None,
                        help="Limit number of events (for testing)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose logging")
    args = parser.parse_args(argv)

    log_file = args.error_log or (args.output + ".error.log")
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file, mode="w", encoding="utf-8"),
                  logging.StreamHandler(sys.stdout)])

    regions = load_regions(args.regions_file)
    logger.info("Loaded %d Azure regions from %s", len(regions),
                args.regions_file)

    client = GDACSClient(
        start_date=args.start_date,
        end_date=args.end_date,
        event_types=args.event_types,
        alert_levels=args.alert_levels,
    )
    logger.info("Client config: types=%s levels=%s window=%s..%s",
                client.event_types, client.alert_levels, client.start_date,
                client.end_date)

    events = client.search_events()
    if args.max_events:
        events = events[:args.max_events]

    output, df = match_events_to_regions(client, regions, args.radius_km,
                                         events=events)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)
    logger.info("Wrote %s (%d regions, %d with events, %d event slots)",
                args.output, len(output),
                sum(1 for v in output.values() if v),
                sum(len(v) for v in output.values()))

    print("\n=== Summary ===")
    if not df.empty:
        print(df.groupby("eventtype").agg(
            events=("eventid", "count"),
            with_matches=("matched_regions", lambda s: int((s > 0).sum())),
            avg_matches=("matched_regions", "mean"),
        ).round(2).to_string())
        multi = df[df["matched_regions"] > 1]
        print(f"\nEvents assigned to multiple regions: {len(multi)}")
        if len(multi):
            print(multi[["eventtype", "eventid", "name",
                         "matched_regions"]].head(20).to_string(index=False))
    else:
        print("No events fetched.")
    print(f"\nOutput: {args.output}\nError log: {log_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
