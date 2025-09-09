import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
from rasterio import Affine

# --- Load image ---
img_path = "/Users/sapiensndatabaye/Desktop/APPS/AFGHAN QUAKE/layers/exposure.png"
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- Define the colors for each intensity (example: replace with your legend colors) ---
# Colors in RGB: [(R, G, B), ...]
intensity_colors = {
    "Low": (255, 255, 204),
    "Moderate": (255, 204, 102),
    "High": (255, 102, 102),
    "Very High": (204, 0, 0)
}

# --- Georeferencing (example affine, replace with real coordinates of corners) ---
# left, top, pixel size x, rotation, top, pixel size y
transform = Affine.translation(65.0, 38.0) * Affine.scale(0.01, -0.01)  # adjust to your map extent

polygons = []
intensity_labels = []

for label, color in intensity_colors.items():
    # Create a mask for the color
    mask = cv2.inRange(img_rgb, np.array(color), np.array(color))
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        # Convert pixel coordinates to map coordinates
        coords = []
        for point in cnt[:, 0, :]:
            x, y = point
            lon, lat = transform * (x, y)
            coords.append((lon, lat))
        if len(coords) >= 3:  # valid polygon
            polygons.append(Polygon(coords))
            intensity_labels.append(label)

# --- Save to shapefile ---
gdf = gpd.GeoDataFrame({'intensity': intensity_labels, 'geometry': polygons}, crs="EPSG:4326")
gdf.to_file("/Users/sapiensndatabaye/Desktop/APPS/AFGHAN QUAKE/layers/exposure.shp")

print("Shapefile created successfully!")