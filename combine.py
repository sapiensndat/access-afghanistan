import os
import json
import pandas as pd
from shutil import copyfile

# Create DATA folder if it doesn't exist
os.makedirs("DATA", exist_ok=True)

# 1. Combine Points (population, displaced, FHH, disability)
points_files = [
    "pop_clipped_points_displaced.geojson",
    "pop_high_points_displaced.geojson",
    "pop_medium_points_displaced.geojson",
    "pop_low_points_displaced.geojson"
]

all_points = {"type": "FeatureCollection", "features": []}

for pf in points_files:
    if os.path.exists(pf):
        with open(pf) as f:
            data = json.load(f)
            # Ensure all features have source_file
            for feat in data.get("features", []):
                feat["properties"]["source_file"] = pf
            all_points["features"].extend(data.get("features", []))

# Save combined points
with open("DATA/points.geojson", "w") as f:
    json.dump(all_points, f)
print(f"Combined points saved: {len(all_points['features'])} features")

# 2. Combine Polygon / Boundaries layers (zone, intensity, admin)
polygon_files = [
    "zone_low.geojson",
    "zone_medium.geojson",
    "zone_high.geojson",
    "intensity_zones.geojson",
    "geoBoundaries-AFG-ADM1_simplified.geojson",
    "population_all_provinces.geojson",
    "population_by_province.geojson"
]

all_polygons = {"type": "FeatureCollection", "features": []}

for pf in polygon_files:
    if os.path.exists(pf):
        with open(pf) as f:
            data = json.load(f)
            all_polygons["features"].extend(data.get("features", []))

with open("DATA/polygons.geojson", "w") as f:
    json.dump(all_polygons, f)
print(f"Combined polygons saved: {len(all_polygons['features'])} features")

# 3. Copy population/reference CSVs
csv_files = [
    "afg_admpop_adm1_2021_v2.csv",
    "PIN_estimates.csv"
]

for cf in csv_files:
    if os.path.exists(cf):
        copyfile(cf, os.path.join("DATA", cf))
        print(f"Copied CSV: {cf}")

# 4. Copy News / Event / Partner JSONs
json_files = ["news.json", "event.json", "partner_coverage.json"]
for jf in json_files:
    if os.path.exists(jf):
        copyfile(jf, os.path.join("DATA", jf))
        print(f"Copied JSON: {jf}")

# 5. Copy other useful reference files (optional)
optional_files = ["PIN_gaps.geojson", "houses.geojson", "houses_high.geojson", "houses_medium.geojson", "houses_low.geojson", "epicenter_impact.geojson", "afg_fault_centroids.geojson"]
for of in optional_files:
    if os.path.exists(of):
        copyfile(of, os.path.join("DATA", of))
        print(f"Copied reference: {of}")

print("All main datasets organized in DATA folder.")