'''2️⃣ Transform (transform.py)
Each city’s JSON must be flattened into tabular format with one row per hour.
A. Required Columns
city
time
pm10
pm2_5
carbon_monoxide
nitrogen_dioxide
sulphur_dioxide
ozone
uv_index
B. Derived Features (Feature Engineering)
1. AQI based on PM2.5
0–50     → Good
51–100   → Moderate
101–200  → Unhealthy
201–300  → Very Unhealthy>300     → Hazardous 
2. Pollution Severity Score
Use weighted pollutants:
severity = (pm2_5 * 5) + (pm10 * 3) +
           (nitrogen_dioxide * 4) + (sulphur_dioxide * 4) +
           (carbon_monoxide * 2) + (ozone * 3)
3. Risk Classification
severity > 400 → "High Risk"severity > 200 → "Moderate Risk" else           → "Low Risk" 
4. Temperature Hour-of-Day Feature (Optional)
Extract hour:
hour = time.hour
C. Transform Requirements
Convert timestamps into datetime format
Convert all pollutant values to numeric
Remove records where all pollutant readings are missing
Save transformed data into:
data/staged/air_quality_transformed.'''

#!/usr/bin/env python3
"""
transform.py

Flatten Open-Meteo hourly air-quality JSON files (data/raw/) into tabular format:
Required columns:
  city, time, pm10, pm2_5, carbon_monoxide, nitrogen_dioxide,
  sulphur_dioxide, ozone, uv_index

Derived features:
 - aqi_pm25 (Good, Moderate, Unhealthy, Very Unhealthy, Hazardous) based on pm2_5
 - severity: weighted sum
 - risk: High/Moderate/Low based on severity thresholds
 - hour: hour of day extracted from time

Saves combined transformed table to:
  data/staged/air_quality_transformed.csv
  data/staged/air_quality_transformed.parquet
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import pandas as pd
import numpy as np

# ---------------- Config ----------------
PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
STAGED_DIR = PROJECT_ROOT / "data" / "staged"
STAGED_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUT = STAGED_DIR / "air_quality_transformed.csv"
PARQUET_OUT = STAGED_DIR / "air_quality_transformed.parquet"

# Pollutant keys we expect (names used in Open-Meteo hourly)
POLLUTANTS = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "uv_index",
]

# Logging
LOG_FILE = PROJECT_ROOT / "transform.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())  # also print to stdout

# ---------------- Helpers ----------------


def infer_city_from_filename(path: Path) -> str:
    """
    Infer city name from filename.
    Examples: delhi_raw_20251211_123000.json -> delhi
              delhi_openaq_latest_20251211T123000Z.json -> delhi
    """
    name = path.stem.lower()
    # take first token before underscore or dash
    token = name.split("_")[0].split("-")[0]
    return token.capitalize()


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def aqi_label_from_pm25(pm25: float) -> str:
    """Return AQI label based on pm2.5 value (ranges inclusive per spec)."""
    if pd.isna(pm25):
        return None
    try:
        v = float(pm25)
    except Exception:
        return None
    if v <= 50:
        return "Good"
    if 51 <= v <= 100:
        return "Moderate"
    if 101 <= v <= 200:
        return "Unhealthy"
    if 201 <= v <= 300:
        return "Very Unhealthy"
    if v > 300:
        return "Hazardous"
    return None


def compute_severity(row: pd.Series) -> float:
    """
    severity = (pm2_5 * 5) + (pm10 * 3) +
               (nitrogen_dioxide * 4) + (sulphur_dioxide * 4) +
               (carbon_monoxide * 2) + (ozone * 3)
    Missing values treated as 0 for severity calculation.
    """
    def val(k):
        v = row.get(k)
        return 0.0 if pd.isna(v) else float(v)

    return (
        val("pm2_5") * 5.0
        + val("pm10") * 3.0
        + val("nitrogen_dioxide") * 4.0
        + val("sulphur_dioxide") * 4.0
        + val("carbon_monoxide") * 2.0
        + val("ozone") * 3.0
    )


def classify_risk(severity: float) -> str:
    if pd.isna(severity):
        return "Low Risk"
    if severity > 400:
        return "High Risk"
    if severity > 200:
        return "Moderate Risk"
    return "Low Risk"


# ---------------- Main transform routine ----------------


def flatten_openeo_meteo_hourly(payload: dict, city: str) -> pd.DataFrame:
    """
    Given an Open-Meteo air-quality JSON payload and a city name,
    return a DataFrame with one row per hourly timestamp and pollutant columns.
    """
    # payload expected structure:
    # { "hourly": { "time": [...], "pm10": [...], "pm2_5": [...], ... }, ... }
    hourly = payload.get("hourly") or {}
    times = hourly.get("time") or []

    if not times:
        logger.warning("No 'time' array in hourly payload for city=%s", city)
        return pd.DataFrame()  # empty

    # build dict of arrays for each pollutant; if missing use list of None
    data = {"time": times}
    n = len(times)
    for p in POLLUTANTS:
        arr = hourly.get(p)
        if arr is None:
            # try alternative key name mapping (if underscores vs dots etc.)
            arr = hourly.get(p.replace("_", ".")) or hourly.get(p.replace(".", "_"))
        if arr is None:
            # fill with Nones
            arr = [None] * n
        # ensure length matches times; if shorter, pad with None
        if len(arr) < n:
            arr = list(arr) + [None] * (n - len(arr))
        data[p] = arr

    df = pd.DataFrame(data)
    df["city"] = city

    # Convert time column to datetime
    # Open-Meteo returns ISO strings like "2025-12-11T13:00"
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")

    # Cast pollutants to numeric (coerce errors -> NaN)
    for p in POLLUTANTS:
        df[p] = pd.to_numeric(df[p], errors="coerce")

    # Reorder columns as requested
    cols = ["city", "time"] + POLLUTANTS
    df = df[cols]

    return df


def transform_all(raw_dir: Path) -> pd.DataFrame:
    """
    Process all JSON files under raw_dir and return combined transformed DataFrame.
    """
    files: List[Path] = sorted(raw_dir.glob("**/*.*"))  # include nested directories
    logger.info("Found %d raw files under %s", len(files), raw_dir)

    dfs: List[pd.DataFrame] = []
    for f in files:
        # consider only json files
        if f.suffix.lower() not in [".json", ".txt"]:
            continue
        try:
            payload = load_json(f)
        except Exception as e:
            logger.error("Skipping file %s - failed to load JSON: %s", f, e)
            continue

        city = infer_city_from_filename(f)
        df = flatten_openeo_meteo_hourly(payload, city)
        if df.empty:
            logger.warning("No hourly rows produced for file %s (city=%s)", f, city)
            continue

        dfs.append(df)

    if not dfs:
        logger.warning("No dataframes produced from raw files.")
        return pd.DataFrame(columns=["city", "time"] + POLLUTANTS)

    combined = pd.concat(dfs, ignore_index=True)
    logger.info("Combined rows before cleaning: %d", len(combined))

    # Remove records where all pollutant readings are missing
    pollutant_cols = POLLUTANTS
    combined["all_missing"] = combined[pollutant_cols].isna().all(axis=1)
    before = len(combined)
    combined = combined[~combined["all_missing"]].drop(columns=["all_missing"])
    after = len(combined)
    logger.info("Dropped %d rows where all pollutant readings are missing", before - after)

    # Derived features
    combined["aqi_pm25"] = combined["pm2_5"].apply(aqi_label_from_pm25)
    # severity - use apply row-wise
    combined["severity"] = combined.apply(compute_severity, axis=1)
    combined["risk"] = combined["severity"].apply(classify_risk)

    # hour of day feature (local hour or UTC hour?). We'll extract UTC hour from the timestamp.
    combined["hour"] = combined["time"].dt.hour

    # final column ordering
    final_cols = [
        "city",
        "time",
        "hour",
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone",
        "uv_index",
        "aqi_pm25",
        "severity",
        "risk",
    ]
    # Some columns might be missing if payload lacked them, ensure they exist
    for c in final_cols:
        if c not in combined.columns:
            combined[c] = pd.NA

    combined = combined[final_cols]

    # Sort by city/time
    combined = combined.sort_values(["city", "time"]).reset_index(drop=True)

    return combined


def main():
    logger.info("Starting transform step")
    df = transform_all(RAW_DIR)
    if df.empty:
        logger.warning("Transformed dataframe is empty — nothing to save.")
    else:
        # Save CSV and parquet
        df.to_csv(CSV_OUT, index=False)
        try:
            df.to_parquet(PARQUET_OUT, index=False)
        except Exception as e:
            logger.warning("Could not write parquet file: %s", e)
        logger.info("Saved transformed CSV -> %s", CSV_OUT)
        logger.info("Saved transformed Parquet -> %s", PARQUET_OUT)
        print(f"Saved transformed data to:\n - {CSV_OUT}\n - {PARQUET_OUT}")

    logger.info("Transform step finished.")


if __name__ == "__main__":
    main()
