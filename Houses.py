# houses.py
import osmnx as ox
import json
from shapely.geometry import mapping

center = (34.519, 70.734)
distance_m = 50000  # 50 km

tags = {'building': True}
buildings_gdf = ox.features_from_point(center, tags=tags, dist=distance_m)

features = []
for _, row in buildings_gdf.iterrows():
    geom = mapping(row.geometry)
    features.append({
        "type": "Feature",
        "geometry": geom,
        "properties": {"label": row.get('building', 'building')}
    })

geojson = {"type": "FeatureCollection", "features": features}

with open("houses.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Houses layer saved as houses.geojson with {len(features)} buildings")