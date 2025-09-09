import geopandas as gpd
import pandas as pd
import json
import glob

def main():
    # Load provinces
    provinces = gpd.read_file('geoBoundaries-AFG-ADM1_simplified.geojson').to_crs(epsg=4326)

    # Merge population points
    pop_files = glob.glob('pop_*_points.geojson')
    pop_gdfs = [gpd.read_file(f).to_crs(epsg=4326) for f in pop_files]
    pop_merged = gpd.GeoDataFrame(pd.concat(pop_gdfs, ignore_index=True), crs='EPSG:4326')
    if "index_right" in pop_merged.columns:
        pop_merged = pop_merged.drop(columns=["index_right"])
    for col in ["index_right","index_left"]:
        if col in pop_merged.columns: pop_merged=pop_merged.drop(columns=[col])
        if col in provinces.columns: provinces=provinces.drop(columns=[col])
    pop_merged = gpd.sjoin(pop_merged, provinces[["geometry","shapeName"]], how="left", predicate="intersects")
    pop_merged = pop_merged.rename(columns={'shapeName':'province'})
    pop_prov = pop_merged.dissolve(by='province', aggfunc='sum')[['population']]

    # Merge displaced points
    disp_files = glob.glob('pop_*_points_displaced.geojson')
    disp_gdfs = [gpd.read_file(f).to_crs(epsg=4326) for f in disp_files]
    disp_merged = gpd.GeoDataFrame(pd.concat(disp_gdfs, ignore_index=True), crs='EPSG:4326')
    if "index_right" in disp_merged.columns:
        disp_merged = disp_merged.drop(columns=["index_right"])
    for col in ["index_right","index_left"]:
        if col in disp_merged.columns: disp_merged=disp_merged.drop(columns=[col])
        if col in provinces.columns: provinces=provinces.drop(columns=[col])
    disp_merged = gpd.sjoin(disp_merged, provinces[["geometry","shapeName"]], how="left", predicate="intersects")
    disp_merged = disp_merged.rename(columns={'shapeName':'province'})
    disp_prov = disp_merged.dissolve(by='province', aggfunc='sum')[['estimated_displaced']]

    # Join population & displaced
    df = pop_prov.join(disp_prov, how='left').fillna(0)

    # Load intensity zones
    intensity = gpd.read_file('intensity_zones.geojson').dissolve(by='NAME_1', aggfunc='mean')[['intensity']]
    df = df.join(intensity, how='left').fillna(0)

    # Load vulnerable and disability data
    pop_pyramid = pd.read_json('population_pyramid.json')
    disability = pd.read_json('disability_data.json')
    df = df.merge(pop_pyramid[['province','vulnerable_pct']], on='province', how='left')
    df = df.merge(disability[['province','disability_pct']], on='province', how='left').fillna(0)

    # Load sector needs
    with open('sector_specific_needs.json') as f:
        sector_data = json.load(f)['sector_specific_needs']

    # Calculate people in need per sector
    alpha, beta = 0.3, 0.3
    for sector, info in sector_data.items():
        S = info['need'] / pop_merged['population'].sum()
        df[f'need_{sector}'] = (
            df['population'] * df['intensity']
            * (1 + alpha*df['vulnerable_pct'])
            * (1 + beta*df['disability_pct'])
            * S
        )

    # Total need
    sector_cols = [c for c in df.columns if c.startswith('need_')]
    df['total_need'] = df[sector_cols].sum(axis=1)

    # Export
    df.to_csv('people_in_need_per_province.csv')
    df.to_file('people_in_need_per_province.geojson', driver='GeoJSON')

    # Print summary
    print("✅ Total estimated people in need per cluster:")
    print(df[sector_cols].sum())

if __name__ == "__main__":
    main()