import geopandas as gpd
import pandas as pd
import glob
import fiona

# Load provinces explicitly with fiona
with fiona.open('afg_provinces.geojson', driver='GeoJSON') as src:
    provinces = gpd.GeoDataFrame.from_features(src, crs="EPSG:4326")

# Load all displaced points
all_files = glob.glob('pop_*_points_displaced.geojson')
gdfs = []
for f in all_files:
    with fiona.open(f, driver='GeoJSON') as src:
        gdf = gpd.GeoDataFrame.from_features(src, crs="EPSG:4326")
        gdfs.append(gdf)

# Merge all
merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs='EPSG:4326')

# Spatial join with provinces
merged = gpd.sjoin(merged, provinces[['geometry','NAME_1']], how='left', predicate='intersects')
merged = merged.rename(columns={'NAME_1':'province'})

# Export
merged.to_file('displaced_all_provinces.geojson', driver='GeoJSON')
print(f'Created displaced_all_provinces.geojson with {merged["estimated_displaced"].sum():.0f} estimated displaced people')
