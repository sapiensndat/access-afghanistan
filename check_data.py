import ee
import rasterio
import osmnx as ox
import geopandas as gpd
from shapely.geometry import box

# ---------- Initialize Earth Engine ----------
ee.Initialize(project='jovial-style-470913-i9')

# ---------- AOI Polygon ----------
bounds = [[-77.037, 38.907],
          [-77.037, 38.908],
          [-77.036, 38.908],
          [-77.036, 38.907]]

aoi_geom = ee.Geometry.Polygon(bounds)

# ---------- 1️⃣ Check Sentinel Collections ----------
s1_ic = ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(aoi_geom)
s2_ic = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi_geom)

print("Sentinel-1 images:", s1_ic.size().getInfo())
print("Sentinel-2 images:", s2_ic.size().getInfo())

# ---------- 2️⃣ Check Raster ----------
raster_path = "tmp_change_mask.tif"
try:
    with rasterio.open(raster_path) as src:
        arr = src.read(1)
        print(f"Raster {raster_path}: min={arr.min()}, max={arr.max()}, mean={arr.mean():.4f}")
except FileNotFoundError:
    print(f"Raster file {raster_path} not found!")

# ---------- 3️⃣ Check OSM Roads ----------
xs = [p[0] for p in bounds]
ys = [p[1] for p in bounds]
aoi_bbox = {'xmin': min(xs), 'xmax': max(xs), 'ymin': min(ys), 'ymax': max(ys)}

roads_gdf = ox.graph_to_gdfs(
    ox.graph_from_polygon(
        box(aoi_bbox['xmin'], aoi_bbox['ymin'], aoi_bbox['xmax'], aoi_bbox['ymax']),
        network_type='drive'
    ),
    nodes=False, edges=True
)
print("Number of roads loaded:", len(roads_gdf))

# ---------- 4️⃣ Check Checkpoints & Conflict Zones ----------
try:
    cp_gdf = gpd.read_file("checkpoints.geojson")
    print("Checkpoints loaded:", len(cp_gdf))
except Exception as e:
    print("Error loading checkpoints.geojson:", e)

try:
    cz_gdf = gpd.read_file("conflict_zones.geojson")
    print("Conflict zones loaded:", len(cz_gdf))
except Exception as e:
    print("Error loading conflict_zones.geojson:", e)

print("✅ All checks completed.")