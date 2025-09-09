import json
import glob

# List of all GeoJSON files to combine (exclude news.json)
files = glob.glob("*.geojson")
files = [f for f in files if f != "news.json"]

combined = {"type": "FeatureCollection", "features": []}

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if data.get("features"):
            for feature in data["features"]:
                # Keep original properties, add source file info if needed
                feature["properties"]["source_file"] = file
                combined["features"].append(feature)

# Save combined file
with open("combined_all.geojson", "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f"Combined {len(files)} files into combined_all.geojson with {len(combined['features'])} features.")