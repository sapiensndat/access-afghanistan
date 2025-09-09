#!/bin/bash
# Estimate population, houses, and displaced people by intensity zone

raster="pop_clipped.tif"
zones="intensity_zones.geojson"

# Loop through each unique intensity value
for label in $(ogrinfo -al -geom=no $zones | grep "intensity (String)" -A9999 | grep -v "intensity (String)" | grep "intensity" | awk -F= '{print $2}' | sort | uniq); do
    echo "Processing intensity $label ..."

    # Extract the zone
    ogr2ogr -where "intensity='$label'" zone_${label}.geojson $zones

    # Clip raster to the zone
    gdalwarp -cutline zone_${label}.geojson -crop_to_cutline -of GTiff $raster pop_${label}.tif -q

    # Convert to XYZ for summing
    gdal_translate -of XYZ pop_${label}.tif pop_${label}.xyz -q

    # Compute values
    pop=$(awk '$3 > 0 {s+=$3} END {print s}' pop_${label}.xyz)
    houses=$(echo "$pop / 6.5" | bc)
    displaced=$(echo "$pop * 0.3" | bc)

    # Output
    echo "Intensity $label → Population=$pop, Houses=$houses, Displaced=$displaced"
    echo ""
done
