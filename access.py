#!/usr/bin/env python3
"""
progressive_disaster_map.py

Generates three continuously updated GeoJSONs:
1. admin2_risk.geojson → polygons with risk_level per admin2
2. events/*.geojson → points of ACLED, GDACS, USGS events
3. access_map_yesterday.geojson → roads with access_level and hazards

Dependencies:
- geopandas, shapely, osmnx, requests, pandas, numpy, ee, geemap, rasterio
"""

import os
import json
import requests
import geopandas as gpd
import pandas as pd
import numpy as np
import osmnx as ox
from shapely.geometry import mapping, box
from shapely.ops import unary_union
from datetime import datetime, timedelta, timezone

# ---------------- CONFIG ----------------
ROOT = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()
OUT_DIR = ROOT
EVENTS_DIR = os.path.join(OUT_DIR, 'events')
os.makedirs(EVENTS_DIR, exist_ok=True)

YESTERDAY_DATE = (datetime.now(timezone.utc).date() - timedelta(days=1)).isoformat()
PRIOR_DATE     = (datetime.now(timezone.utc).date() - timedelta(days=8)).isoformat()
OSM_NETWORK_TYPE = 'drive'

ACCESS_GEOJSON   = os.path.join(OUT_DIR, "access_map_yesterday.geojson")
ACCESS_SHP_DIR   = os.path.join(OUT_DIR, "access_shapefile")
TEMP_RASTER_MASK = os.path.join(OUT_DIR, "tmp_change_mask.tif")

CHECKPOINTS_GEOJSON = os.path.join(OUT_DIR, "checkpoints.geojson")
CONFLICT_ZONES_GEOJSON = os.path.join(OUT_DIR, "conflict_zones.geojson")
FAULTS_GEOJSON = os.path.join(OUT_DIR, "afg_fault_centroids.geojson")

ADMIN2_IN = os.path.join(OUT_DIR, "geoBoundaries-AFG-ADM2.geojson")
ADMIN2_OUT = os.path.join(OUT_DIR, "geoBoundaries-AFG-ADM2_risk.geojson")

ACLED_API = "https://api.acleddata.com/acled/read/?key=XB4T-5NYmfvaFASi8FKH&email=buhendwa.medi@ucbukavu.ac.cd"
GDACS_API = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/MAP?fromdate=2024-01-01&todate=2024-12-31"
USGS_API  = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5"

# ---------------- HELPERS ----------------
def save_geojson_feature_collection(gdf, path):
    if gdf is None or gdf.empty:
        with open(path, 'w') as f:
            json.dump({"type":"FeatureCollection", "features":[]}, f)
        return
    gdf.to_file(path, driver='GeoJSON')

def fetch_acled_and_save(url, outpath):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    features = []
    for rec in data.get('data', []):
        lat, lon = rec.get('latitude'), rec.get('longitude')
        if lat is None or lon is None: continue
        props = rec.copy()
        props.pop('latitude', None)
        props.pop('longitude', None)
        features.append({"type":"Feature", "geometry":{"type":"Point","coordinates":[lon, lat]}, "properties":props})
    with open(outpath, 'w') as f:
        json.dump({"type":"FeatureCollection", "features":features}, f)
    return outpath

def read_geojson_if_exists(path):
    if os.path.exists(path):
        try:
            return gpd.read_file(path)
        except:
            return None
    return None

def split_aoi_for_osm(minx, miny, maxx, maxy, max_size=0.5):
    x_splits = max(1, int((maxx - minx)/max_size))
    y_splits = max(1, int((maxy - miny)/max_size))
    boxes = []
    for i in range(x_splits):
        for j in range(y_splits):
            bminx = minx + i*(maxx - minx)/x_splits
            bmaxx = minx + (i+1)*(maxx - minx)/x_splits
            bminy = miny + j*(maxy - miny)/y_splits
            bmaxy = miny + (j+1)*(maxy - miny)/y_splits
            boxes.append(box(bminx,bminy,bmaxx,bmaxy))
    return boxes

# ---------------- FETCH EVENTS ----------------
print("⏳ Fetching event feeds...")
for name, url in [("ACLED", ACLED_API), ("GDACS", GDACS_API), ("USGS", USGS_API)]:
    try:
        out = os.path.join(EVENTS_DIR, f"{name}.geojson")
        print(f"  - {name} -> {out}")
        if name=="ACLED": fetch_acled_and_save(url, out)
        else:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            with open(out, 'w') as f: json.dump(r.json(), f)
    except Exception as e:
        print(f"  ⚠️ {name} fetch failed:", e)

# ---------------- LOAD LOCAL INPUTS ----------------
cp_gdf = read_geojson_if_exists(CHECKPOINTS_GEOJSON)
cp_gdf = cp_gdf if cp_gdf is not None else gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs='EPSG:4326')

cz_gdf = read_geojson_if_exists(CONFLICT_ZONES_GEOJSON)
cz_gdf = cz_gdf if cz_gdf is not None else gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs='EPSG:4326')

faults_gdf = read_geojson_if_exists(FAULTS_GEOJSON)
faults_gdf = faults_gdf if faults_gdf is not None else gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs='EPSG:4326')

admin2_gdf = read_geojson_if_exists(ADMIN2_IN)

# ---------------- AOI ----------------
if admin2_gdf is not None and not admin2_gdf.empty:
    minx, miny, maxx, maxy = admin2_gdf.total_bounds
elif not cp_gdf.empty:
    minx, miny, maxx, maxy = cp_gdf.total_bounds
else:
    minx, miny, maxx, maxy = 69.10, 34.30, 69.50, 34.70
print("⏳ AOI bbox:", (minx, miny, maxx, maxy))

# ---------------- LOAD OSM ROADS ----------------
print("⏳ Loading OSM roads...")
roads_gdf_list = []
for idx, sub_poly in enumerate(split_aoi_for_osm(minx, miny, maxx, maxy, max_size=0.25)):
    try:
        G = ox.graph_from_polygon(sub_poly, network_type=OSM_NETWORK_TYPE)
        sub_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True).reset_index().rename(columns={"u":"u_id","v":"v_id"})
        sub_gdf = sub_gdf[sub_gdf.geometry.notnull()].copy()
        roads_gdf_list.append(sub_gdf)
        print(f"    ✅ Slice {idx+1} roads loaded:", len(sub_gdf))
    except Exception as e:
        print(f"    ⚠️ Slice {idx+1} OSM fetch failed:", e)
roads_gdf = pd.concat(roads_gdf_list, ignore_index=True) if roads_gdf_list else gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs='EPSG:4326')

# ---------------- LOAD EVENTS ----------------
event_gdfs = []
for fname in ("ACLED.geojson","GDACS.geojson","USGS.geojson"):
    p = os.path.join(EVENTS_DIR, fname)
    if os.path.exists(p):
        try:
            g = gpd.read_file(p)
            if not g.empty and g.geometry.iloc[0].geom_type == 'Point':
                g['source_feed'] = fname.split('.')[0]
                event_gdfs.append(g)
        except: continue
all_events = gpd.GeoDataFrame(pd.concat(event_gdfs, ignore_index=True), crs='EPSG:4326') if event_gdfs else gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs='EPSG:4326')

# ---------------- PROJECTIONS ----------------
metric_crs = 'EPSG:3857'
roads_gdf = roads_gdf.to_crs(metric_crs)
cp_gdf = cp_gdf.to_crs(metric_crs)
cz_gdf = cz_gdf.to_crs(metric_crs)
all_events = all_events.to_crs(metric_crs)
faults_gdf = faults_gdf.to_crs(metric_crs)
admin2_gdf = admin2_gdf.to_crs(metric_crs)

# ---------------- BUFFERS & UNION ----------------
cp_union = unary_union(cp_gdf.geometry) if not cp_gdf.empty else None
cz_union = unary_union(cz_gdf.geometry) if not cz_gdf.empty else None
event_union = unary_union(all_events.geometry) if not all_events.empty else None
fault_union = unary_union(faults_gdf.geometry) if not faults_gdf.empty else None

# ---------------- ROAD CLASSIFICATION ----------------
roads_gdf['near_checkpoint'] = roads_gdf.geometry.intersects(cp_union) if cp_union else False
roads_gdf['near_conflict_zone'] = roads_gdf.geometry.intersects(cz_union) if cz_union else False
roads_gdf['near_event'] = roads_gdf.geometry.intersects(event_union) if event_union else False
roads_gdf['near_fault'] = roads_gdf.geometry.intersects(fault_union) if fault_union else False

def classify_road(row):
    pct = float(row.get('mask_pct') or 0)
    hazards = []
    if row.get('near_event'): hazards.append('event')
    if row.get('near_conflict_zone'): hazards.append('conflict_zone')
    if row.get('near_checkpoint'): hazards.append('checkpoint')
    if row.get('near_fault'): hazards.append('fault')
    access_level, obstruct = 'open','none'
    if pct >= 0.4 or (row.get('near_event') and pct>0.05):
        access_level, obstruct = 'blocked','blocked_by_change_or_event'
    elif pct >= 0.1 or row.get('near_fault') or row.get('near_conflict_zone') or row.get('near_checkpoint'):
        access_level = 'partial'
        obstruct = 'ground_deformation' if row.get('near_fault') else 'security' if row.get('near_conflict_zone') else 'checkpoint' if row.get('near_checkpoint') else 'debris_or_damage'
    return pd.Series([access_level, obstruct, ",".join(hazards) if hazards else 'none'])

roads_gdf[['access_level','obstruction','hazards_nearby']] = roads_gdf.apply(classify_road, axis=1)
roads_gdf['confidence'] = roads_gdf['mask_pct'].clip(0,1)
roads_gdf['notes'] = roads_gdf.apply(lambda r: f"mask_pct={r.mask_pct:.3f}; hazards={r.hazards_nearby}", axis=1)

# ---------------- ADMIN2 RISK ----------------
if admin2_gdf is not None and not admin2_gdf.empty:
    admin2 = admin2_gdf.copy()
    admin2['admin2_id'] = admin2.index.astype(str)
    roads_agg = gpd.sjoin(roads_gdf[['geometry','mask_pct','access_level']], admin2[['admin2_id','geometry']], how='inner', predicate='intersects')
    road_stats = roads_agg.groupby('admin2_id').agg(mean_mask_pct=('mask_pct','mean'), n_roads=('mask_pct','count'), n_blocked=('access_level', lambda s: (s=='blocked').sum())).reset_index() if not roads_agg.empty else pd.DataFrame(columns=['admin2_id','mean_mask_pct','n_roads','n_blocked'])
    events_sjoin = gpd.sjoin(all_events[['geometry']], admin2[['admin2_id','geometry']], how='inner', predicate='intersects') if not all_events.empty else pd.DataFrame(columns=['admin2_id'])
    hazard_counts = events_sjoin.groupby('admin2_id').size().reset_index(name='n_events') if not events_sjoin.empty else pd.DataFrame(columns=['admin2_id','n_events'])
    stats = pd.merge(admin2[['admin2_id']], road_stats, on='admin2_id', how='left')
    stats = pd.merge(stats, hazard_counts, on='admin2_id', how='left').fillna({'mean_mask_pct':0,'n_roads':0,'n_blocked':0,'n_events':0})
    stats['event_norm'] = stats['n_events'] / max(1, int(stats['n_events'].max()))
    stats['risk_score'] = stats['mean_mask_pct']*0.7 + stats['event_norm']*0.3
    stats['risk_level'] = stats['risk_score'].apply(lambda s: 'High' if s>=0.35 else 'Medium' if s>=0.12 else 'Low' if s>0 else 'None')
    admin2 = admin2.merge(stats[['admin2_id','mean_mask_pct','n_roads','n_blocked','n_events','risk_score','risk_level']], on='admin2_id', how='left')
    admin2 = admin2.fillna({'mean_mask_pct':0,'n_roads':0,'n_blocked':0,'n_events':0,'risk_score':0,'risk_level':'None'})
    save_geojson_feature_collection(admin2.to_crs(epsg=4326), ADMIN2_OUT)
    print("✅ Admin2 risk exported:", ADMIN2_OUT)

# ---------------- EXPORT ROADS ----------------
os.makedirs(ACCESS_SHP_DIR, exist_ok=True)
roads_export = roads_gdf.to_crs(epsg=4326).rename(columns={
    'access_level':'access_lev','mask_pct':'mask_pct','confidence':'confidence','obstruction':'obstruct','hazards_nearby':'hazards'
})
save_geojson_feature_collection(roads_export, ACCESS_GEOJSON)
roads_export.to_file(os.path.join(ACCESS_SHP_DIR,'access_map.shp'))
print("✅ Roads exported:", ACCESS_GEOJSON)

print("✅ All GeoJSONs generated successfully.")