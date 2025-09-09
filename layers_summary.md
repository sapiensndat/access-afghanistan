# Layers Files Summary and Dashboard Usage
## afg_admgz.xlsx
- Type: Microsoft Excel 2007+
- Sheets: 
- Dashboard usage: Convert to CSV/JSON, then use for tables, charts, or population/pyramid data

## afg_admpop_adm1_2021_v2.csv
- Type: CSV text
- Columns: Admin0_Name,Admin0_Code,Admin1_Name,Admin1_Code,F_TL,M_TL,T_TL,F_00_04,M_00_04,T_00_04,F_05_09,M_05_09,T_05_09,F_10_14,M_10_14,T_10_14,F_15_19,M_15_19,T_15_19,F_20_24,M_20_24,T_20_24,F_25_29,M_25_29,T_25_29,F_30_34,M_30_34,T_30_34,F_35_39,M_35_39,T_35_39,F_40_44,M_40_44,T_40_44,F_45_49,M_45_49,T_45_49,F_50_54,M_50_54,T_50_54,F_55_59,M_55_59,T_55_59,F_60_64,M_60_64,T_60_64,F_65_69,M_65_69,T_65_69,F_70_74,M_70_74,T_70_74,F_75_79,M_75_79,T_75_79,F_80plus,M_80plus,T_80plus
- Rows:       34
- Dashboard usage: Use for tables, charts, or linking to map layers

## afg_fault_centroids.geojson
- Type: ASCII text, with very long lines (65536), with no line terminators
- Features count: 138996
- Properties: [
  "count",
  "label"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## afg_pd_2020_1km.tif
- Type: TIFF image data, little-endian
- Info: Size is 1726, 1095
Pixel Size = (0.008333333300000,-0.008333333300000)
Band 1 Block=512x512 Type=Float32, ColorInterp=Gray
- Dashboard usage: Use for heatmaps, raster overlays, or population density maps

## calculate_needs.py
- Type: Python script text executable, Unicode text, UTF-8 text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## cities.json
- Type: JSON data
- Top-level keys: [
  "all_cities",
  "onepager_cities"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## combine_geojson.py
- Type: ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## combine.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## combined_all.geojson
- Type: ASCII text
- Features count: 218766
- Properties: [
  "count",
  "depth_km",
  "estimated_displaced",
  "index_right",
  "intensity",
  "label",
  "latitude",
  "longitude",
  "magnitude",
  "notes_gap",
  "notes_need",
  "notes_reached",
  "population",
  "population_density",
  "population_total",
  "province",
  "sector_specific_needs_gap",
  "sector_specific_needs_need",
  "sector_specific_needs_reached",
  "shapeGroup",
  "shapeID",
  "shapeISO",
  "shapeName",
  "shapeType",
  "source_file",
  "type",
  "zone_name"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## damage_analysis.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## Dashboard_Data_Columns.txt
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## disability_data.json
- Type: JSON data
- Top-level keys: [
  "disability_data"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## earthquake_summary.json
- Type: JSON data
- Top-level keys: [
  "high",
  "low",
  "medium"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## epicenter_impact.geojson
- Type: JSON data
- Features count: 2
- Properties: [
  "depth_km",
  "magnitude",
  "type"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## epicenter.py
- Type: ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## estimate_by_intensity.sh
- Type: Bourne-Again shell script text executable, Unicode text, UTF-8 text
- Unknown file type, check manually for dashboard use

## estimate_displaced.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## event.json
- Type: JSON data
- Top-level keys: [
  "event",
  "pager",
  "shakemap"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## exposure.cpg
- Type: ASCII text, with no line terminators
- Unknown file type, check manually for dashboard use

## exposure.dbf
- Type: FoxBase+/dBase III DBF, no records * 25, update-date 125-9-2
- Unknown file type, check manually for dashboard use

## exposure.png
- Type: PNG image data, 700 x 700, 8-bit/color RGBA, non-interlaced
- Unknown file type, check manually for dashboard use

## exposure.prj
- Type: ASCII text, with no line terminators
- Unknown file type, check manually for dashboard use

## exposure.shp
- Type: ESRI Shapefile version 1000 length 50 type PolyLine
- Unknown file type, check manually for dashboard use

## exposure.shx
- Type: ESRI Shapefile version 1000 length 50 type PolyLine
- Unknown file type, check manually for dashboard use

## extract_pop_geojson.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## fhh_data.json
- Type: JSON data
- Top-level keys: [
  "fhh_data"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## geoBoundaries-AFG-ADM1_simplified.geojson
- Type: JSON data
- Features count: 34
- Properties: [
  "shapeGroup",
  "shapeID",
  "shapeISO",
  "shapeName",
  "shapeType"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## geoBoundaries.gpkg
- Type: SQLite 3.x database (OGC GeoPackage file), user version 10400, last written using SQLite version 3050003, file counter 10, database pages 47, cookie 0x21, schema 4, UTF-8, version-valid-for 10
- Unknown file type, check manually for dashboard use

## Hospitals.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## houses_high.geojson
- Type: JSON data
- Features count: 59
- Properties: [
  "label"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## houses_low.geojson
- Type: JSON data
- Features count: 352
- Properties: [
  "label"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## houses_medium.geojson
- Type: JSON data
- Features count: 181
- Properties: [
  "label"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## houses.geojson
- Type: JSON data
- Features count: 352
- Properties: [
  "label"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## Houses.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## inspect_layers.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## intensity_zones.geojson
- Type: JSON data
- Features count: 3
- Properties: [
  "intensity",
  "zone_name"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## intensity.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## layers_summary.md
- Type: ASCII text, with very long lines (484), with CRLF, LF line terminators
- Unknown file type, check manually for dashboard use

## list_drive_contents.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## losses.json
- Type: JSON data
- Top-level keys: [
  "empirical_economic",
  "empirical_fatality",
  "semi_empirical_fatalities"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## map_data.json
- Type: JSON data
- Top-level keys: [
  "map_data",
  "notes"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## merge_displaced_fix.py
- Type: ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## merge_displaced_fix2.py
- Type: ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## merge_displaced.py
- Type: Python script text executable, Unicode text, UTF-8 text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## monitor_news.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## news.json
- Type: JSON data
- Top-level keys: [
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## partner_coverage.json
- Type: JSON data
- Top-level keys: [
  "map_data",
  "notes"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## PIN_estimates.csv
- Type: CSV text
- Columns: province,sector,PIN_estimated
- Rows:      171
- Dashboard usage: Use for tables, charts, or linking to map layers

## PIN_gaps.geojson
- Type: JSON data
- Features count: 2
- Properties: [
  "notes_gap",
  "notes_need",
  "notes_reached",
  "sector_specific_needs_gap",
  "sector_specific_needs_need",
  "sector_specific_needs_reached",
  "shapeGroup",
  "shapeID",
  "shapeISO",
  "shapeName",
  "shapeType"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## PIN_pyramid.json
- Type: JSON data
- Top-level keys: [
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  25,
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## PIN.py
- Type: Python script text executable, Unicode text, UTF-8 text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## pop_clipped_points_displaced.geojson
- Type: ASCII text
- Features count: 6916
- Properties: [
  "estimated_displaced",
  "index_right",
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_clipped_points.geojson
- Type: ASCII text
- Features count: 9874
- Properties: [
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_clipped.tif
- Type: TIFF image data, little-endian, direntries=17, height=107, bps=32, compression=none, PhotometricIntepretation=BlackIsZero, width=129
- Info: Size is 129, 107
Pixel Size = (0.008333333300000,-0.008333333300000)
Band 1 Block=129x15 Type=Float32, ColorInterp=Gray
- Dashboard usage: Use for heatmaps, raster overlays, or population density maps

## pop_clipped.tif.aux.xml
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## pop_clipped.xyz
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## pop_high_points_displaced.geojson
- Type: JSON data
- Features count: 3490
- Properties: [
  "estimated_displaced",
  "index_right",
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_high_points.geojson
- Type: JSON data
- Features count: 1745
- Properties: [
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_high.tif
- Type: TIFF image data, little-endian, direntries=17, height=42, bps=32, compression=none, PhotometricIntepretation=BlackIsZero, width=51
- Info: Size is 51, 42
Pixel Size = (0.008333333300000,-0.008333333300000)
Band 1 Block=51x40 Type=Float32, ColorInterp=Gray
- Dashboard usage: Use for heatmaps, raster overlays, or population density maps

## pop_high.xyz
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## pop_low_points_displaced.geojson
- Type: ASCII text
- Features count: 6916
- Properties: [
  "estimated_displaced",
  "index_right",
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_low_points.geojson
- Type: ASCII text
- Features count: 9874
- Properties: [
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_low.tif
- Type: TIFF image data, little-endian, direntries=17, height=107, bps=32, compression=none, PhotometricIntepretation=BlackIsZero, width=129
- Info: Size is 129, 107
Pixel Size = (0.008333333300000,-0.008333333300000)
Band 1 Block=129x15 Type=Float32, ColorInterp=Gray
- Dashboard usage: Use for heatmaps, raster overlays, or population density maps

## pop_low.xyz
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## pop_medium_points_displaced.geojson
- Type: ASCII text
- Features count: 6916
- Properties: [
  "estimated_displaced",
  "index_right",
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_medium_points.geojson
- Type: ASCII text
- Features count: 5157
- Properties: [
  "latitude",
  "longitude",
  "population"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## pop_medium.tif
- Type: TIFF image data, little-endian, direntries=17, height=75, bps=32, compression=none, PhotometricIntepretation=BlackIsZero, width=90
- Info: Size is 90, 75
Pixel Size = (0.008333333300000,-0.008333333300000)
Band 1 Block=90x22 Type=Float32, ColorInterp=Gray
- Dashboard usage: Use for heatmaps, raster overlays, or population density maps

## pop_medium.xyz
- Type: ASCII text
- Unknown file type, check manually for dashboard use

## population_all_provinces.geojson
- Type: ASCII text
- Features count: 26650
- Properties: [
  "index_right",
  "latitude",
  "longitude",
  "population",
  "province"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## population_by_province.geojson
- Type: JSON data
- Features count: 34
- Properties: [
  "population_total",
  "shapeGroup",
  "shapeID",
  "shapeISO",
  "shapeName",
  "shapeType"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## population_pyramid.json
- Type: JSON data
- Top-level keys: [
  "notes",
  "pyramid_data"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## population.geojson
- Type: ASCII text
- Features count: 1210
- Properties: [
  "count",
  "population",
  "population_density"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## population.gpkg
- Type: SQLite 3.x database (OGC GeoPackage file), user version 10400, last written using SQLite version 3050003, file counter 17, database pages 127, cookie 0x2f, schema 4, UTF-8, version-valid-for 17
- Unknown file type, check manually for dashboard use

## population.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## python.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## response_data.json
- Type: JSON data
- Top-level keys: [
  "notes",
  "response_data"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## Roads.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## Schools.py
- Type: Python script text executable, ASCII text
- Python script, not directly used in dashboard, may generate data or preprocess layers

## sector_specific_needs.json
- Type: JSON data
- Top-level keys: [
  "notes",
  "sector_specific_needs"
]
- Dashboard usage: Use for charts, summaries, or API data feeds

## wdclogobg-DaW87GU_.png
- Type: PNG image data, 726 x 726, 8-bit/color RGBA, non-interlaced
- Unknown file type, check manually for dashboard use

## zone_high.geojson
- Type: JSON data
- Features count: 1
- Properties: [
  "intensity",
  "zone_name"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## zone_low.geojson
- Type: JSON data
- Features count: 1
- Properties: [
  "intensity",
  "zone_name"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

## zone_medium.geojson
- Type: JSON data
- Features count: 1
- Properties: [
  "intensity",
  "zone_name"
]
- Dashboard usage: Use Leaflet/Mapbox to display features, style by properties, attach popups with key properties

