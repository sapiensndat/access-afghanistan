import os
import json
import requests
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime, timedelta
import pandas as pd

# ---------- CONFIG ----------
ACCESS_MAP_PATH = "/Users/sapiensndatabaye/Desktop/APPS/AFGHAN QUAKE/layers/access_map_yesterday.geojson"

ACLED_API = "https://api.acleddata.com/acled/read/?key=XB4T-5NYmfvaFASi8FKH&email=buhendwa.medi@ucbukavu.ac.cd"
GDACS_API = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/MAP?fromdate=2024-01-01&todate=2024-12-31"
USGS_API = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5"

# ---------- HELPER FUNCTIONS ----------
def fetch_acled():
    r = requests.get(ACLED_API)
    r.raise_for_status()
    data = r.json()
    events = data.get('data', [])
    records = []
    for e in events:
        lat = e.get('latitude')
        lon = e.get('longitude')
        if lat is None or lon is None:  # skip events without coords
            continue
        records.append({
            "geometry": Point(lon, lat),
            "disaster_category": e.get('event_type'),
            "disaster_sub_category": e.get('sub_event_type'),
            "people_affected": e.get('fatalities', 0),
            "description": e.get('notes', ""),
            "country": e.get('country'),
            "admin1": e.get('admin1'),
            "admin2": e.get('admin2'),
            "admin3": e.get('admin3')
        })
    return gpd.GeoDataFrame(records, geometry='geometry', crs='EPSG:4326')

def fetch_gdacs():
    r = requests.get(GDACS_API)
    r.raise_for_status()
    data = r.json()
    events = data.get('features', [])
    records = []
    for e in events:
        geom = e.get('geometry', {})
        if geom.get('type') != 'Point':
            continue
        coords = geom.get('coordinates')
        props = e.get('properties', {})
        records.append({
            "geometry": Point(coords[0], coords[1]),
            "disaster_category": props.get('eventtype'),
            "description": props.get('description', ""),
            "country": props.get('country', ""),
            "admin1": "",
            "admin2": "",
            "admin3": ""
        })
    return gpd.GeoDataFrame(records, geometry='geometry', crs='EPSG:4326')

def fetch_usgs():
    r = requests.get(USGS_API)
    r.raise_for_status()
    data = r.json()
    events = data.get('features', [])
    records = []
    for e in events:
        geom = e.get('geometry', {})
        coords = geom.get('coordinates', [None, None])
        lon, lat = coords[0], coords[1]
        if lon is None or lat is None:
            continue
        props = e.get('properties', {})
        records.append({
            "geometry": Point(lon, lat),
            "disaster_category": "Earthquake",
            "magnitude": props.get('mag', None),
            "description": props.get('place', ""),
            "country": "",
            "admin1": "",
            "admin2": "",
            "admin3": ""
        })
    return gpd.GeoDataFrame(records, geometry='geometry', crs='EPSG:4326')

# ---------- MAIN WORKFLOW ----------
def update_access_map():
    print("⏳ Loading existing access map...")
    access_gdf = gpd.read_file(ACCESS_MAP_PATH)

    print("⏳ Fetching ACLED events...")
    acled_gdf = fetch_acled()
    print(f"✅ {len(acled_gdf)} ACLED events loaded")

    print("⏳ Fetching GDACS events...")
    gdacs_gdf = fetch_gdacs()
    print(f"✅ {len(gdacs_gdf)} GDACS events loaded")

    print("⏳ Fetching USGS earthquakes...")
    usgs_gdf = fetch_usgs()
    print(f"✅ {len(usgs_gdf)} USGS events loaded")

    # Merge all hazard points
    all_events = gpd.GeoDataFrame(
        pd.concat([acled_gdf, gdacs_gdf, usgs_gdf], ignore_index=True),
        crs='EPSG:4326'
    )

    print("⏳ Updating access map with hazards...")

    # Project to a metric CRS (meters) for accurate buffering
    metric_crs = 'EPSG:3857'  # Web Mercator
    hazard_points = all_events.to_crs(metric_crs)
    buffer_m = 1000  # 1 km
    hazard_points['geometry'] = hazard_points.geometry.buffer(buffer_m)
    hazard_points = hazard_points.to_crs('EPSG:4326')

    access_gdf['hazard'] = access_gdf.geometry.apply(
        lambda geom: any(hazard_points.geometry.intersects(geom))
    )

    access_gdf['status'] = access_gdf.apply(
        lambda row: 'blocked' if row['hazard'] else row.get('status', 'open'), axis=1
    )

    print("⏳ Saving updated access map...")
    access_gdf.to_file(ACCESS_MAP_PATH, driver='GeoJSON')
    print(f"✅ Access map updated: {ACCESS_MAP_PATH}")

# ---------- RUN ----------
if __name__ == "__main__":
    update_access_map()