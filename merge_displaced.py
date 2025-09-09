import geopandas as gpd
import glob
from shapely.geometry import Point

# 1️⃣ Load Afghanistan provinces (admin1)
provinces = gpd.read_file("gadm_afg/afg_provinces.geojson").to_crs(epsg=4326)

# 2️⃣ Load all displaced GeoJSONs
all_files = glob.glob("pop_*_points_displaced.geojson")
gdfs = [gpd.read_file(f).to_crs(epsg=4326) for f in all_files]

# 3️⃣ Merge into one GeoDataFrame
merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs="EPSG:4326")

# 4️⃣ Spatial join with provinces
merged = gpd.sjoin(merged, provinces[['geometry', 'NAME_1']], how='left', predicate='intersects')
merged = merged.rename(columns={'NAME_1': 'province'})

# 5️⃣ Export merged GeoJSON
merged.to_file("displaced_all_provinces.geojson", driver="GeoJSON")
print(f"Created displaced_all_provinces.geojson with {merged['estimated_displaced'].sum():.0f} estimated displaced people")
