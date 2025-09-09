import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import re
from langdetect import detect

# List of URLs to monitor
urls = [
    "https://time.com/7313842/afghanistan-earthquake-relief-organizations-how-to-help/",
    "https://www.bbc.com/news/articles/cwye0lpj9z6o",
    "https://www.ifrc.org/press-release/ifrc-launches-emergency-appeal-support-afghanistan-earthquake-recovery",
    "https://www.doctorswithoutborders.org/latest/how-msf-responding-earthquake-afghanistan",
    "https://www.amnesty.org/en/latest/news/2025/09/afghanistan-earthquake/",
    "https://www.theguardian.com/world/2025/sep/02/afghanistan-earthquake-taliban-appeals-for-international-aid-as-rescue-teams-search-for-survivors",
    "https://news.un.org/en/story/2025/09/1165766",
    "https://www.aljazeera.com/news/2025/9/3/hope-fades-for-finding-survivors-after-afghan-quake-kills-more-than-1400",
    "https://abcnews.go.com/International/afghanistan-earthquake-death-toll-rises/story?id=125172025",
    "https://reliefweb.int/report/afghanistan/afghanistan-flash-update-2-earthquake-nangarhar-province-2-september-2025-1600",
    "https://earthquake.usgs.gov/earthquakes/eventpage/us7000qsvj",
    "https://www.rescue.org/article/afghanistan-earthquake-whats-happening-and-how-help",
    "https://en.wikipedia.org/wiki/2025_Afghanistan_earthquake",
    "https://www.unrefugees.org/news/unhcr-calls-for-urgent-aid-to-afghanistan-s-earthquake-hit-communities/",
    "https://www.cnn.com/2025/09/02/asia/afghanistan-earthquake-taliban-us-intl-hnk",
    "https://www.reuters.com/world/asia-pacific/afghanistan-earthquake-kills-800-injures-2800-taliban-asks-world-help-2025-09-01/",
    "https://abcnews.go.com/International/impacted-afghanistan-earthquake-charities-organizations-support-relief-efforts/story?id=125191723",
    "https://www.bbc.com/news/live/cy8kkxxxj3xt",
    "https://www.abc.net.au/news/2025-09-04/afghanistan-earthquake-challenges-taliban-health-aid-workers/105732408",
    "https://reliefweb.int/disaster/eq-2025-000153-afg",
    "https://www.emro.who.int/afg/afghanistan-news/who-steps-up-response-to-meet-rising-health-needs-after-earthquake-in-eastern-afghanistan.html",
    "https://www.icrc.org/en/article/icrc-response-deadly-earthquake-afghanistan",
    "https://www.directrelief.org/2025/09/after-a-catastrophic-earthquake-in-afghanistan-direct-relief-commits-50000-prepares-emergency-medical-shipment/"
]

# Load existing news.json or create empty list
def load_news():
    try:
        with open("news.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Save news.json
def save_news(news):
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, indent=2, ensure_ascii=False)

# Regex for organization names (English & Arabic)
org_regex = re.compile(r'([A-Z][\w&.,\-\s]{1,50}|[\u0600-\u06FF\s]{2,50})')

# Extract organization names
def extract_organizations(text):
    names = set()
    for match in org_regex.findall(text):
        name = match.strip()
        if len(name) > 2 and not name.lower().startswith("the "):
            names.add(name)
    return list(names)

# Detect main activity from text
def detect_activity(text):
    activities = {
        "Relief": ["relief", "aid", "support", "assistance"],
        "Medical": ["hospital", "medical", "health", "clinic"],
        "Shelter": ["shelter", "tent", "housing", "camp"],
        "Rescue": ["rescue", "search", "recover"]
    }
    text_lower = text.lower()
    for key, keywords in activities.items():
        if any(k in text_lower for k in keywords):
            return key
    return "Unknown"

# Map activity to official OCHA sector
def detect_sector(activity):
    mapping = {
        "Relief": "Nutrition",
        "Medical": "Health",
        "Shelter": "Shelter",
        "Rescue": "Protection",
        "Unknown": "Other"
    }
    return mapping.get(activity, "Other")

# Extract info from a URL
def extract_info(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.content, "html.parser")
        body = soup.get_text(separator=" ").strip()
        lang = detect(body)
        orgs = extract_organizations(body)
        entries = []
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for org in orgs:
            activity = detect_activity(body)
            entry = {
                "organization": org,
                "type": "Unknown",  # Could detect UN Agency / INGO / Local NGO
                "main_activity": activity,
                "sector": detect_sector(activity),
                "people_reached": 0,
                "funding_received": 0,
                "source_url": url,
                "source_time": date_time,
                "language": lang,
                "status": "Active",
                "impact_level": 3
            }
            entries.append(entry)
        return entries
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return []

# Main monitoring loop
def monitor():
    news_data = load_news()
    seen_urls = {entry["source_url"] for entry in news_data}

    while True:
        for url in urls:
            if url not in seen_urls:
                entries = extract_info(url)
                if entries:
                    news_data.extend(entries)
                    save_news(news_data)
                    seen_urls.add(url)
                    print(f"Added {len(entries)} organizations from {url}")
        print("Sleeping 5 minutes before next check...")
        time.sleep(300)

if __name__ == "__main__":
    monitor()