import json
import pandas as pd

# -------------------------------
# 1️⃣ Load population data (Admin1-level)
# -------------------------------
pop_df = pd.read_csv('afg_admpop_adm1_2021_v2.csv')
pop_df['province'] = pop_df['Admin1_Name']

# -------------------------------
# 2️⃣ Load displaced points
# -------------------------------
def load_displaced(file):
    with open(file, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data['features'])
    return df

displaced_low = load_displaced('pop_low_points_displaced.geojson')
displaced_medium = load_displaced('pop_medium_points_displaced.geojson')
displaced_high = load_displaced('pop_high_points_displaced.geojson')

displaced_all = pd.concat([displaced_low, displaced_medium, displaced_high], ignore_index=True)

if 'properties.Admin1_Name' in displaced_all.columns:
    displaced_by_prov = displaced_all.groupby('properties.Admin1_Name')['properties.estimated_displaced'].sum().reset_index()
    displaced_by_prov.rename(columns={'properties.Admin1_Name':'province', 
                                      'properties.estimated_displaced':'displaced'}, inplace=True)
else:
    displaced_by_prov = pd.DataFrame({'province': pop_df['province'], 'displaced': 0})

# -------------------------------
# 3️⃣ Load sector needs
# -------------------------------
with open('sector_specific_needs.json', 'r') as f:
    sector_needs_json = json.load(f)

# Only the actual sector dict
sector_needs = sector_needs_json.get('sector_specific_needs', {})

# Normalize total need for weighting
total_need = sum(info.get('need', 0) for info in sector_needs.values())

# -------------------------------
# 4️⃣ Demographic weight function
# -------------------------------
def demographic_weight(row):
    children = row['T_00_04'] + row['T_05_09'] + row['T_10_14']
    elderly = row['T_65_69'] + row['T_70_74'] + row['T_75_79'] + row['T_80plus']
    women_total = row['F_TL']
    total = row['T_TL']
    weighted = (children*0.3 + elderly*0.2 + women_total*0.5)/total
    return min(weighted, 1.0)

pop_df['demo_weight'] = pop_df.apply(demographic_weight, axis=1)

# -------------------------------
# 5️⃣ Merge population and displaced
# -------------------------------
pin_df = pd.merge(pop_df[['province','T_TL','demo_weight']], displaced_by_prov, on='province', how='left')
pin_df['displaced'] = pin_df['displaced'].fillna(0)

# -------------------------------
# 6️⃣ Calculate PIN estimates
# -------------------------------
pins = []
for idx, row in pin_df.iterrows():
    province = row['province']
    pop = row['T_TL']
    demo_w = row['demo_weight']
    displaced = row['displaced']
    
    for sector, info in sector_needs.items():
        need = info.get('need', 0)
        factor = need / total_need if total_need > 0 else 1
        pin_est = displaced + pop * demo_w * factor
        pins.append({'province': province, 'sector': sector, 'PIN_estimated': round(pin_est)})

# -------------------------------
# 7️⃣ Save final DataFrame
# -------------------------------
pin_final = pd.DataFrame(pins)
pin_final.to_csv('PIN_estimates.csv', index=False)
print(pin_final.head())
print(f"✅ PIN estimates saved: {len(pin_final)} rows")