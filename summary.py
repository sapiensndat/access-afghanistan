import json
from pathlib import Path
from datetime import datetime
import time

# Paths to local data
POP_FILE = Path("population_by_province.geojson")
DISPLACED_FILE = Path("pop_clipped_points_displaced.geojson")
DAMAGES_FILE = Path("houses.geojson")  # or houses_high.geojson, etc.

OUTPUT_MD = Path("summary.md")
OUTPUT_JSON = Path("summary.json")

def read_population(provinces=None):
    total_pop = 0
    if POP_FILE.exists():
        with open(POP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for feature in data.get("features", []):
                name = feature.get("properties", {}).get("shapeName", "")
                if provinces and name not in provinces:
                    continue
                pop_str = feature.get("properties", {}).get("population_total", 0) or 0
                try:
                    pop_int = int(pop_str)
                except:
                    pop_int = 0
                total_pop += pop_int
    return total_pop

def read_displaced():
    total_displaced = 0
    if DISPLACED_FILE.exists():
        with open(DISPLACED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for feature in data.get("features", []):
                displaced = feature.get("properties", {}).get("displaced", 0) or 0
                try:
                    total_displaced += int(displaced)
                except:
                    continue
    return total_displaced

def read_damages():
    total_houses = 0
    if DAMAGES_FILE.exists():
        with open(DAMAGES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            total_houses = len(data.get("features", []))
    return total_houses

def generate_situation_text(provinces=None):
    total_population = read_population(provinces)
    displaced = read_displaced()
    damaged_houses = read_damages()
    today = datetime.now().strftime("%d %B %Y %H:%M:%S")
    
    text = f"""**Situation Summary - {today}**

Affected Provinces: {', '.join(provinces) if provinces else 'All'}

Total population in affected areas: {total_population:,}
Estimated number of displaced people: {displaced:,}
Estimated number of houses damaged: {damaged_houses:,}

The recent earthquake has caused significant human and material losses. The affected communities face immediate needs for Health, Nutrition, Protection, Shelter, and WASH services. Vulnerable populations, including children, elderly, and persons with disabilities, are at high risk.

The disaster has disrupted livelihoods, social infrastructure, and basic services. Urgent humanitarian assistance is required, including food, medical care, temporary shelter, clean water, and protection interventions.

Humanitarian actors, including UN agencies, NGOs, and local partners, are responding, but gaps remain. Donors are urged to increase flexible funding to support timely, appropriate, and effective interventions.

Authorities and partners should continue to coordinate emergency response, strengthen preparedness, and plan long-term recovery and resilience measures.
"""
    return text

def save_summary(text):
    OUTPUT_MD.write_text(text, encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps({"summary": text}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    earthquake_provinces = ["Kunar", "Nangarhar"]
    
    while True:
        summary_text = generate_situation_text(provinces=earthquake_provinces)
        print(summary_text)
        save_summary(summary_text)
        print("Summary updated. Waiting 5 minutes before next update...")
        time.sleep(300)  # 5 minutes interval