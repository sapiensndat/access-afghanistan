# roads.py
import osmnx as ox
import json
from shapely.geometry import mapping

center = (34.519, 70.734)
distance_m = 50000

tags = {'highway': True}  # all types of roads
roads_gdf = ox.geometries_from_point(center, tags=tags, dist=distance_m)

features = []
for _, row in roads_gdf.iterrows():
    geom = mapping(row.geometry)
    features.append({
        "type": "Feature",
        "geometry": geom,
        "properties": {"type": row.get('highway', 'road')}
    })

geojson = {"type": "FeatureCollection", "features": features}

with open("roads.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Roads layer saved as roads.geojson with {len(features)} roads") 