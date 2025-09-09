import ee

# Initialize Earth Engine
try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
    print("Earth Engine initialized successfully")
except Exception as e:
    print("Error initializing Earth Engine:", e)
    exit()

# Epicenter & impact area
EPICENTER = ee.Geometry.Point([70.734, 34.519])
IMPACT_RADIUS = 50000  # 50 km
IMPACT_AREA = EPICENTER.buffer(IMPACT_RADIUS)
print("Impact area defined")

# Create distance image
distances = ee.Image.pixelLonLat().distance(EPICENTER).clip(IMPACT_AREA)
print("Distance image created")

# Define thresholds
THRESHOLDS = ee.List([10000, 30000, 50000])

try:
    # Create a classified image based on distance thresholds
    def classify_distance(distance):
        classified = ee.Image(0)
        classified = classified.where(distances.lt(THRESHOLDS.get(0)), 1)  # High: < 10km
        classified = classified.where(distances.gte(THRESHOLDS.get(0)).And(distances.lt(THRESHOLDS.get(1))), 2)  # Medium: 10-30km
        classified = classified.where(distances.gte(THRESHOLDS.get(1)).And(distances.lt(THRESHOLDS.get(2))), 3)  # Low: 30-50km
        return classified

    intensity_image = classify_distance(distances).rename('intensity')
    print("Classified image created")

    # Export to Google Drive as GeoTIFF
    task = ee.batch.Export.image.toDrive(
        image=intensity_image,
        description="intensity_zones_tiff",
        folder="EE_Exports",
        fileNamePrefix="intensity_zones",
        region=IMPACT_AREA,
        scale=1000,
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    task.start()
    print("Export task submitted for intensity_zones.tif. Check Earth Engine Tasks tab for completion.")

except Exception as e:
    print("Error exporting intensity zones:", e)