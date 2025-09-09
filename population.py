import ee
import json

# Initialize Earth Engine
try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
except Exception as e:
    print("Error initializing Earth Engine:", e)
    exit()

# Epicenter & impact area
EPICENTER = ee.Geometry.Point([70.734, 34.519])
IMPACT_RADIUS = 50000  # 50 km
IMPACT_AREA = EPICENTER.buffer(IMPACT_RADIUS)

# Load population density image from GPWv4.11
try:
    # Load the image collection and select the 2020 image
    pop_collection = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density")
    POP_LAYER = pop_collection.filterDate('2020-01-01', '2020-12-31').first().select('population_density').clip(IMPACT_AREA)

    # Convert population density to integer (round to nearest integer to preserve data)
    POP_LAYER = POP_LAYER.round().toInt32()

    # Reduce population raster to vectors (polygons)
    vectors = POP_LAYER.reduceToVectors(
        geometry=IMPACT_AREA,
        scale=1000,
        geometryType='polygon',
        eightConnected=False,
        labelProperty='population_density',
        maxPixels=1e12
    ).getInfo()

    # Assign population property to each feature
    for f in vectors['features']:
        f['properties']['population'] = f['properties'].get('population_density', 0)

    # Create GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": vectors['features']
    }

    # Save locally
    with open("population.geojson", "w") as f:
        json.dump(geojson, f, indent=2)

    print("Population layer saved as population.geojson")

except Exception as e:
    print("Error exporting population:", e)