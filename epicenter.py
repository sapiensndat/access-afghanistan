# epicenter.py
import ee
import json

# Initialize Earth Engine with your project ID
ee.Initialize(project='jovial-style-470913-i9')

# --- EPICENTER & IMPACT AREA ---
EPICENTER = ee.Geometry.Point([70.734, 34.519])
IMPACT_RADIUS = 50000  # in meters
IMPACT_AREA = EPICENTER.buffer(IMPACT_RADIUS)

epicenter_features = [
    {
        "type": "Feature",
        "geometry": EPICENTER.getInfo(),
        "properties": {
            "type": "epicenter",
            "magnitude": 6.1,
            "depth_km": 10
        }
    },
    {
        "type": "Feature",
        "geometry": IMPACT_AREA.getInfo(),
        "properties": {
            "type": "impact_area",
            "magnitude": 6.1,
            "depth_km": 10
        }
    }
]

epicenter_geojson = {"type": "FeatureCollection", "features": epicenter_features}

with open("epicenter_impact.geojson", "w") as f:
    json.dump(epicenter_geojson, f, indent=2)

print("Epicenter & impact area saved as epicenter_impact.geojson")


# --- INTENSITY ZONES ---
zones = [
    {"name": "High", "radius": 20000, "intensity": "high"},
    {"name": "Medium", "radius": 35000, "intensity": "medium"},
    {"name": "Low", "radius": 50000, "intensity": "low"}
]

intensity_features = []
for z in zones:
    circle = EPICENTER.buffer(z["radius"])
    intensity_features.append({
        "type": "Feature",
        "geometry": circle.getInfo(),
        "properties": {
            "zone_name": z["name"],
            "intensity": z["intensity"]
        }
    })

intensity_geojson = {"type": "FeatureCollection", "features": intensity_features}

with open("intensity_zones.geojson", "w") as f:
    json.dump(intensity_geojson, f, indent=2)

print("Intensity zones saved as intensity_zones.geojson")