#!/bin/bash
# damage_analysis.sh
# Count houses, estimate population and displaced by intensity zone
# Works for multiple GeoJSON files

total_houses=0
total_population=0
total_displaced=0

for file in houses_*.geojson; do
    # Extract intensity label from filename
    label=$(basename "$file" .geojson | cut -d'_' -f2)

    # Count houses (each feature = one house)
    houses=$(grep -o '"type": "Feature"' "$file" | wc -l)
    houses=$(echo $houses)  # trim spaces

    # Estimate population and displaced
    pop=$((houses * 65 / 10))      # 6.5 people per house
    displaced=$((pop / 2))         # 50% displaced

    echo "Intensity $label → Houses=$houses, Population=$pop, Displaced=$displaced"

    # Add to totals
    total_houses=$((total_houses + houses))
    total_population=$((total_population + pop))
    total_displaced=$((total_displaced + displaced))
done

echo "----------------------------------------"
echo "TOTAL → Houses=$total_houses, Population=$total_population, Displaced=$total_displaced"