import rasterio, geopandas as gpd, pandas as pd
from shapely.geometry import Point
import numpy as np, glob, os

for tif_file in glob.glob("pop_*.tif"):
    raster = rasterio.open(tif_file)
    arr = raster.read(1)
    rows, cols = np.where(arr > 0)
    coords = [raster.xy(r, c) for r, c in zip(rows, cols)]
    values = arr[rows, cols]
    df = pd.DataFrame(coords, columns=["longitude", "latitude"])
    df["population"] = values
    gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.longitude, df.latitude)], crs="EPSG:4326")
    out_file = os.path.splitext(tif_file)[0] + "_points.geojson"
    gdf.to_file(out_file, driver="GeoJSON")
    print(f"Created {out_file}")
