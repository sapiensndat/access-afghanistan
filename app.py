from flask import Flask, jsonify
from flask_cors import CORS
import ee
import json

app = Flask(__name__)
CORS(app, resources={r"/data": {"origins": "http://127.0.0.1:7700"}})

# Initialize Earth Engine
try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
    print("Earth Engine initialized successfully")
except Exception as e:
    print(f"EE initialization error: {e}")
    exit(1)

# Epicenter & impacted area
EPICENTER = ee.Geometry.Point([70.734, 34.519])
IMPACT_RADIUS = 50000  # 50 km
IMPACT_AREA = EPICENTER.buffer(IMPACT_RADIUS)

# Population layer
try:
    POP_LAYER = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density") \
        .filterDate('2020-01-01', '2020-12-31') \
        .first() \
        .select('population_density') \
        .round() \
        .toInt32() \
        .clip(IMPACT_AREA)
    print("Population layer loaded")
except Exception as e:
    print(f"Error loading population layer: {e}")
    POP_LAYER = ee.Image(0).clip(IMPACT_AREA)  # Fallback empty image

# Infrastructure counts (replace with real datasets)
NUM_ROADS = 50
NUM_HOSPITALS = 5
NUM_SCHOOLS = 8

# Sample population points (bubbles)
POP_POINTS = [
    {'lat': 34.55, 'lon': 70.70, 'population': 2000, 'need_score': 0.75},
    {'lat': 34.60, 'lon': 70.75, 'population': 5000, 'need_score': 0.45},
    {'lat': 34.50, 'lon': 70.72, 'population': 12000, 'need_score': 0.88},
    {'lat': 34.53, 'lon': 70.74, 'population': 8000, 'need_score': 0.60}
]

def generate_intensity_zones():
    """
    Generate high, medium, low intensity zones with population and polygons.
    """
    try:
        # Create distance image
        distances = ee.Image.pixelLonLat().distance(EPICENTER).clip(IMPACT_AREA)
        print("Distance image created")

        # Define thresholds and labels
        THRESHOLDS = ee.List([10000, 30000, 50000])
        LABELS = {1: 'high', 2: 'medium', 3: 'low', 0: 'unknown'}

        # Create classified image
        def classify_distance(distance):
            classified = ee.Image(0)
            classified = classified.where(distances.lt(THRESHOLDS.get(0)), 1)  # High: < 10km
            classified = classified.where(distances.gte(THRESHOLDS.get(0)).And(distances.lt(THRESHOLDS.get(1))), 2)  # Medium: 10-30km
            classified = classified.where(distances.gte(THRESHOLDS.get(1)).And(distances.lt(THRESHOLDS.get(2))), 3)  # Low: 30-50km
            return classified

        intensity_image = classify_distance(distances).rename('intensity')
        print("Classified image created")

        # Calculate population for each zone server-side
        def compute_population(index, result):
            index = ee.Number(index)
            zone_mask = intensity_image.eq(index.add(1))
            pop_masked = POP_LAYER.updateMask(zone_mask)
            pop_stats = pop_masked.reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=IMPACT_AREA,
                scale=1000,
                maxPixels=1e12
            )
            label = ee.List(['high', 'medium', 'low']).get(index)
            population = ee.Dictionary(pop_stats).get('population_density', 0)
            return ee.List(result).add(ee.Dictionary({
                'intensity': label,
                'population': population,
                'polygons': []  # Placeholder, filled later
            }))

        # Generate zones list for indices 0, 1, 2 (for intensity 1, 2, 3)
        zones_list = ee.List.sequence(0, 2).iterate(compute_population, ee.List([]))
        zones_info = zones_list.getInfo()
        print("Population computed for zones:", [z['intensity'] for z in zones_info])

        # Reduce to vectors for all zones
        vectors = intensity_image.reduceToVectors(
            geometry=IMPACT_AREA,
            scale=1000,
            geometryType='polygon',
            eightConnected=False,
            labelProperty='intensity',
            maxPixels=1e13
        )
        print("Vectors created, number of features:", vectors.size().getInfo())

        # Get FeatureCollection as Python dictionary
        vectors_info = vectors.getInfo()
        print("FeatureCollection fetched")

        # Assign polygons to zones locally
        zones = zones_info
        for zone in zones:
            intensity_value = list(LABELS.keys())[list(LABELS.values()).index(zone['intensity'])]
            zone['polygons'] = [
                f['geometry'] for f in vectors_info['features']
                if f['properties'].get('intensity', 0) == intensity_value
            ]

        return zones

    except Exception as e:
        print(f"Error generating intensity zones: {e}")
        return [{'intensity': label, 'population': 0, 'polygons': []} for label in ['high', 'medium', 'low']]

@app.route("/data")
def get_data():
    try:
        coords = EPICENTER.coordinates().getInfo()
        epicenter = {'lon': coords[0], 'lat': coords[1]}
    except Exception:
        epicenter = {'lon': 70.734, 'lat': 34.519}

    intensity_zones = generate_intensity_zones()

    return jsonify({
        'epicenter': epicenter,
        'key_metrics': {
            'total_population': sum([z['population'] for z in intensity_zones]),
            'num_roads': NUM_ROADS,
            'num_hospitals': NUM_HOSPITALS,
            'num_schools': NUM_SCHOOLS
        },
        'intensity_zones': intensity_zones,
        'population_points': POP_POINTS
    })

if __name__ == "__main__":
    app.run(debug=True, port=7700)  # Match CORS port