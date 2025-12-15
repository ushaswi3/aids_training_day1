

'''A global environmental analytics company, AtmosTrack, wants to build an automated Air Quality Monitoring system that collects hourly pollutant readings for major Indian metro cities. The company wants to analyze pollution trends, assess risk levels, and generate daily reports for internal dashboards.
AtmosTrack has chosen the Open-Meteo Air Quality API, which is free and does not require tokens.
You are required to build a complete ETL Pipeline (Extract → Transform → Load → Analyze) using Python.
 
1️⃣ Extract (extract.py)
Use the following API endpoint:
https://air-quality-api.open-meteo.com/v1/air-quality
    ?latitude=<lat>
    &longitude=<lon>
    &hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide,uv_index
Cities to fetch (with coordinates):
City	Latitude	Longitude
Delhi	28.7041	77.1025
Mumbai	19.0760	72.8777
Bengaluru	12.9716	77.5946
Hyderabad	17.3850	78.4867
Kolkata	22.5726	88.3639
Extraction Requirements
Fetch hourly pollutant data for all 5 cities.
Each API call must save raw JSON into:
Implement:
Retry logic (3 attempts)
Graceful failure handling
Logging of API errors
Return a list of all saved file paths.
data/raw/<city>_raw_<timestamp>.json'''



import json
import logging
from datetime import datetime
from pathlib import Path
import requests
import time

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[0]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CITIES = {
    "Delhi":      (28.7041, 77.1025),
    "Mumbai":     (19.0760, 72.8777),
    "Bengaluru":  (12.9716, 77.5946),
    "Hyderabad":  (17.3850, 78.4867),
    "Kolkata":    (22.5726, 88.3639),
}

HOURLY_PARAMS = "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide,uv_index"

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------

LOG_FILE = BASE_DIR / "extract.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


# ---------------------------------------------------------
# Helper: Save JSON
# ---------------------------------------------------------

def save_json(city: str, data: dict, tag="raw") -> Path:
    """Save JSON with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = RAW_DIR / f"{city.lower()}_{tag}_{timestamp}.json"
    filename.write_text(json.dumps(data, indent=2))
    return filename


# ---------------------------------------------------------
# Extract one city
# ---------------------------------------------------------

def extract_city(city: str, lat: float, lon: float) -> Path:
    print(f"\n⏳ Fetching AQI for {city} ({lat}, {lon}) ...")

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": HOURLY_PARAMS
    }

    attempts = 0
    last_error = None

    while attempts < MAX_RETRIES:
        attempts += 1

        try:
            response = requests.get(URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            # Empty API response
            if not data:
                logger.warning(f"Empty API response for {city}")
                fallback = {"city": city, "error": "Empty API response"}
                return save_json(city, fallback, tag="empty")

            # Success
            saved_path = save_json(city, data, tag="raw")
            print(f"✅ Saved AQI data for {city} → {saved_path}")
            logger.info(f"Success: {city} saved to {saved_path}")
            return saved_path

        except Exception as e:
            last_error = str(e)
            logger.error(f"Attempt {attempts} failed for {city}: {e}")
            print(f"⚠️ Attempt {attempts}/{MAX_RETRIES} failed for {city}: {e}")

            if attempts < MAX_RETRIES:
                print(f"⏳ Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)

    # All retries failed
    print(f"❌ Failed to fetch AQI for {city} after {MAX_RETRIES} attempts.")
    error_payload = {"city": city, "error": last_error}
    error_path = save_json(city, error_payload, tag="error")
    logger.error(f"FAILED {city}. Error file saved → {error_path}")
    return error_path


# ---------------------------------------------------------
# Extract all cities
# ---------------------------------------------------------

def extract_all_cities():
    saved_files = []

    print("\n🌍 Starting AQI extraction for all cities...\n")

    for city, (lat, lon) in CITIES.items():
        path = extract_city(city, lat, lon)
        saved_files.append(str(path))
        time.sleep(0.5)   # polite delay

    print("\n🎉 Extraction Completed! Saved files:")
    for f in saved_files:
        print(" -", f)

    return saved_files


# ---------------------------------------------------------
# Run Script
# ---------------------------------------------------------

if __name__ == "__main__":
    extract_all_cities()




















'''import json
import logging
from datetime import datetime
from pathlib import Path
import requests
import time

BASE_DIR = Path(__file__).resolve().parents[0]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CITIES = ["Delhi", "Bengaluru", "Hyderabad", "Mumbai", "Kolkata"]

URL = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=17.3850&longitude=78.4867&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide"

MAX_RETRIES = 3
SLEEP_BETWEEN_RETRIES = 2  # seconds

# ---------------- LOGGING ------------------
LOG_FILE = BASE_DIR / "extract.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


def save_json(city: str, data: dict, type_tag="normal") -> Path:
    """Save JSON with timestamp and return path."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = RAW_DIR / f"{city.lower()}_{type_tag}_{timestamp}.json"
    filename.write_text(json.dumps(data, indent=2))
    return filename


def extract_aqi_data(city: str):
    """
    Fetch AQI data for a given city with:
    - Retry logic (3 attempts)
    - Graceful failure handling
    - Logging
    """
    print(f"⏳ Requesting AQI data for city={city} ...")

    attempts = 0
    last_error = None

    while attempts < MAX_RETRIES:
        attempts += 1
        try:
            resp = requests.get(URL, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Check for empty response
            if not data:
                logger.warning(f"Empty response for city={city}")
                fallback = {"city": city, "error": "Empty API response"}
                saved_path = save_json(city, fallback, type_tag="empty")
                return saved_path

            saved_path = save_json(city, data)
            print(f"✅ Saved AQI data for {city} → {saved_path}")
            logger.info(f"Success: {city} saved to {saved_path}")
            return saved_path

        except Exception as e:
            last_error = str(e)
            logger.error(f"Attempt {attempts} failed for city={city} → {e}")
            print(f"⚠️ Attempt {attempts}/{MAX_RETRIES} failed for {city}: {e}")

            if attempts < MAX_RETRIES:
                print(f"⏳ Retrying in {SLEEP_BETWEEN_RETRIES} seconds...\n")
                time.sleep(SLEEP_BETWEEN_RETRIES)

    # After 3 failed attempts → save fallback error file
    print(f"❌ Failed to fetch AQI for {city} after {MAX_RETRIES} attempts.")
    fallback_data = {"city": city, "error": last_error}
    error_path = save_json(city, fallback_data, type_tag="error")
    logger.error(f"FAILED {city} → Error saved to {error_path}")
    return error_path


def extract_all_cities():
    saved_files = []
    for city in CITIES:
        path = extract_aqi_data(city)
        saved_files.append(str(path))

    print("🎉 AQI extraction completed!")
    print("Saved files:")
    for file in saved_files:
        print(" -", file)

    return saved_files


if __name__ == "__main__":
    extract_all_cities()
'''

