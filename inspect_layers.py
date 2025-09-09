import os
import pandas as pd
import json
import fiona

def inspect_file(filepath):
    """
    Inspects a file and prints its columns/keys and data types.
    """
    filename, file_extension = os.path.splitext(filepath)
    file_extension = file_extension.lower()

    if file_extension == '.csv':
        try:
            df = pd.read_csv(filepath)
            print(f"File: {filepath}")
            print("Columns and Data Types:")
            print(df.info())
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    elif file_extension == '.xlsx':
        try:
            df = pd.read_excel(filepath)
            print(f"File: {filepath}")
            print("Columns and Data Types:")
            print(df.info())
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    elif file_extension in ['.json', '.geojson']:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            print(f"File: {filepath}")
            print("Top-level keys:")
            if isinstance(data, dict):
                print(list(data.keys()))
            elif isinstance(data, list) and data:
                print(f"This is a list of {len(data)} items. Keys of the first item:")
                if isinstance(data[0], dict):
                    print(list(data[0].keys()))
                else:
                    print(f"First item is of type: {type(data[0])}")
            else:
                print(f"Data is of type: {type(data)}")

            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    elif file_extension == '.gpkg':
        try:
            # For GeoPackage files, list the layers
            layers = fiona.listlayers(filepath)
            print(f"File: {filepath}")
            print("GeoPackage layers:")
            print(layers)
            for layer_name in layers:
                with fiona.open(filepath, 'r', layer=layer_name) as collection:
                    print(f"  Layer: {layer_name}")
                    print(f"  Schema: {collection.schema}")
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    elif file_extension == '.shp':
        try:
            with fiona.open(filepath, 'r') as collection:
                print(f"File: {filepath}")
                print("Shapefile Schema:")
                print(collection.schema)
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    elif file_extension == '.tif':
        # For raster files, simply note their presence. More detailed inspection requires
        # libraries like rasterio, which is beyond the scope of a simple column check.
        print(f"File: {filepath}")
        print("This is a raster file (.tif). It contains pixel data, not columns. Use a GIS tool or Python's `rasterio` library to inspect it.")
        print("\n" + "="*50 + "\n")

    else:
        # Ignore other files like .py, .txt, .png, etc.
        pass

def inspect_directory(directory='.'):
    """
    Iterates through a directory and inspects supported files.
    """
    print(f"Inspecting files in directory: {os.path.abspath(directory)}\n")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            inspect_file(filepath)

if __name__ == "__main__":
    inspect_directory()
