import geopandas as gpd
import glob
import os
from shapely.geometry import Point

HOUSEHOLD_SIZE = 8  # average household size

# Load intensity zones (high and medium damage)
zones = gpd.read_file("intensity_zones.geojson").to_crs(epsg=4326)
zones = zones[zones['intensity'].isin(['high', 'medium'])]

# Process population points
for pop_file in glob.glob("pop_*_points.geojson"):
    pop_gdf = gpd.read_file(pop_file).to_crs(epsg=4326)
    
    # Spatial join: only keep points in damaged zones
    displaced = gpd.sjoin(pop_gdf, zones[['geometry']], how='inner', predicate='intersects')
    
    # Apply displacement formula
    # Estimated displaced = population / household size
    displaced['estimated_displaced'] = displaced['population'] / HOUSEHOLD_SIZE
    
    # Export to GeoJSON
    out_file = os.path.splitext(pop_file)[0] + "_displaced.geojson"
    displaced.to_file(out_file, driver="GeoJSON")
    print(f"Created {out_file} with {displaced['estimated_displaced'].sum():.0f} estimated displaced people")
