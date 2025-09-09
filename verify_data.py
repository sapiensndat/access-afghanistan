import os
import geopandas as gpd
import ee
import rasterio
import urllib.request
from shapely.geometry import box

# ---------- Config ----------
CHECKPOINTS_GEOJSON = "checkpoints.geojson"
CONFLICT_ZONES_GEOJSON = "conflict_zones.geojson"
CHECKPOINTS_URL = "https://maphub.net/MappingInsurgencies/taliban-checkpoints/download/geojson"
CONFLICT_ZONES_URL = "https://data.humdata.org/dataset/afghanistan-border-monitoring-unofficial-crossing-points-2023/resource/geojson"
RASTER_PATH = "tmp_change_mask.tif"

# ---------- Helper ----------
def download_file(url, path):
    if not os.path.exists(path) or os.path.getsize(path) < 100:
        print(f"📥 Downloading {url} ...")
        urllib.request.urlretrieve(url, path)
        print(f"✅ Saved to {path}")
    else:
        print(f"✅ {path} exists and seems valid.")

def check_geojson(path):
    if os.path.exists(path):
        gdf = gpd.read_file(path)
        print(f"{path}: {len(gdf)} features loaded")
        if len(gdf) == 0:
            print(f"⚠️ Warning: {path} is empty")
        return gdf
    else:
        print(f"⚠️ {path} not found!")
        return None

# ---------- Verify checkpoints & conflict zones ----------
download_file(CHECKPOINTS_URL, CHECKPOINTS_GEOJSON)
download_file(CONFLICT_ZONES_URL, CONFLICT_ZONES_GEOJSON)

cp_gdf = check_geojson(CHECKPOINTS_GEOJSON)
cz_gdf = check_geojson(CONFLICT_ZONES_GEOJSON)

# ---------- Initialize Earth Engine ----------
ee.Initialize()

# ---------- AOI bounds check ----------
# Dummy AOI for checking
aoi = ee.Geometry.Polygon([[[-77.037,38.907],[-77.037,38.908],[-77.036,38.908],[-77.036,38.907]]])
s1_ic = ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(aoi)
s2_ic = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)
print("Sentinel-1 images in AOI:", s1_ic.size().getInfo())
print("Sentinel-2 images in AOI:", s2_ic.size().getInfo())

# ---------- Raster check ----------
if os.path.exists(RASTER_PATH):
    with rasterio.open(RASTER_PATH) as src:
        arr = src.read(1)
        print(f"Raster {RASTER_PATH}: min={arr.min()}, max={arr.max()}, mean={arr.mean()}")
else:
    print(f"⚠️ Raster {RASTER_PATH} not found")