# hospitals.py
import osmnx as ox
import json
from shapely.geometry import mapping

center = (34.519, 70.734)
distance_m = 50000

tags = {'amenity': 'hospital'}
hospitals_gdf = ox.geometries_from_point(center, tags=tags, dist=distance_m)

features = []
for _, row in hospitals_gdf.iterrows():
    geom = mapping(row.geometry)
    features.append({
        "type": "Feature",
        "geometry": geom,
        "properties": {"name": row.get('name', 'N/A')}
    })

geojson = {"type": "FeatureCollection", "features": features}

with open("hospitals.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Hospitals layer saved as hospitals.geojson with {len(features)} hospitals")