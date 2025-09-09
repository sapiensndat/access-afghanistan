import ee
import time

try:
    ee.Initialize(project='jovial-style-470913-i9')
except ee.EEException as e:
    print(f'Error initializing Earth Engine: {e}')
    exit()

# ----------------------
# Config
# ----------------------
aoi = ee.Geometry.Rectangle([69.2, 33.8, 72.0, 36.0])
pre_dates = ['2025-08-14', '2025-08-31']
post_dates = ['2025-09-01', '2025-09-03']
tile_size = 0.5
scale = 20

# ----------------------
# Function to get Sentinel-1 composite
# ----------------------
def get_s1_composite(dates):
    collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
        .filterBounds(aoi)
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        .filterDate(dates[0], dates[1])
        .select('VV')
        .median())
    return collection

# ----------------------
# Get pre- and post-event composites
# ----------------------
s1_pre = get_s1_composite(pre_dates)
s1_post = get_s1_composite(post_dates)

# ----------------------
# Change metric
# ----------------------
s1_diff = s1_pre.subtract(s1_post).abs().rename('s1_change')

# ----------------------
# Damage thresholds and cleaning
# ----------------------
likely_destroyed = s1_diff.gt(0.5)

# ----------------------
# Function to process each tile (Final Corrected Version)
# ----------------------
def process_tile(tile):
    tile_geom = ee.Geometry(tile)
    
    # Clip the binary image to the tile
    tile_mask = likely_destroyed.clip(tile_geom)
    
    # Use connectedPixelCount to find areas of a certain size
    min_size = 5
    destroyed_clean = tile_mask.connectedPixelCount(
        maxSize=1024,
        eightConnected=True
    ).gte(min_size).selfMask()
    
    # The reduceToVectors function handles empty images gracefully.
    vectors = destroyed_clean.reduceToVectors(
        geometry=tile_geom,
        scale=scale,
        geometryType='polygon',
        eightConnected=True,
        maxPixels=1e9,
    )
    
    return vectors.map(lambda f: ee.Feature(f.geometry().centroid(), {'damage_class': 'likely_destroyed'}))

# ----------------------
# Function to split AOI into tiles (Optimized)
# ----------------------
def split_aoi(aoi_geom, tile_size_deg):
    """Splits an AOI into a list of smaller tiles using standard Python."""
    coords = aoi_geom.bounds().coordinates().get(0).getInfo()
    x_min, y_min = coords[0]
    x_max, y_max = coords[2]
    
    tiles = []
    x = x_min
    while x < x_max:
        y = y_min
        x_next = x + tile_size_deg
        while y < y_max:
            y_next = y + tile_size_deg
            tiles.append(ee.Geometry.Rectangle([x, y, x_next, y_next]))
            y = y_next
        x = x_next
    return ee.List(tiles)

# ----------------------
# Execute the process
# ----------------------
print('Starting large-scale analysis. This may take a while...')

tiles = split_aoi(aoi, tile_size)
all_vectors = ee.FeatureCollection(tiles.map(process_tile)).flatten()

# Start the export task
task = ee.batch.Export.table.toDrive(
    collection=all_vectors,
    description='afg_s1_damage_points_tiled',
    fileFormat='GeoJSON'
)
task.start()

print('Export task started. Check your Google Earth Engine Code Editor or Google Drive "Tasks" tab for progress.')