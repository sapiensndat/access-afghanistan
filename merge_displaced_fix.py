import geopandas as gpd
import pandas as pd
import glob

# Load provinces with Fiona driver
provinces = gpd.read_file('afg_provinces.geojson', driver='GeoJSON').to_crs(epsg=4326)

# Load all displaced points
all_files = glob.glob('pop_*_points_displaced.geojson')
gdfs = [gpd.read_file(f, driver='GeoJSON').to_crs(epsg=4326) for f in all_files]

# Merge all
merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs='EPSG:4326')

# Spatial join with provinces
merged = gpd.sjoin(merged, provinces[['geometry','NAME_1']], how='left', predicate='intersects')
merged = merged.rename(columns={'NAME_1':'province'})

# Export
merged.to_file('displaced_all_provinces.geojson', driver='GeoJSON')
print(f'Created displaced_all_provinces.geojson with {merged["estimated_displaced"].sum():.0f} estimated displaced people')
