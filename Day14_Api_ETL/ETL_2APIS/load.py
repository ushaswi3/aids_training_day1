''' 3️⃣ Load (load.py) – Supabase
Create table:
air_quality_data (
    id BIGSERIAL PRIMARY KEY,
    city TEXT,
    time TIMESTAMP,
    pm10 FLOAT,
    pm2_5 FLOAT,
    carbon_monoxide FLOAT,
    nitrogen_dioxide FLOAT,
    sulphur_dioxide FLOAT,
    ozone FLOAT,
    uv_index FLOAT,
    aqi_category TEXT,
    severity_score FLOAT,
    risk_flag TEXT,
    hour INTEGER)
Load Requirements
Batch insert records (batch size = 200)
Auto-convert NaN → NULL
Convert datetime to ISO formatted strings
Retry failed batches (2 retries)
Print summary of inserted rows'''


import os
import time
import logging

from typing import List, Dict, Any

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# --- Config ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

TABLE_NAME = "air_quality_data"
CSV_PATH = os.path.join("data", "staged", "air_quality_transformed.csv")

BATCH_SIZE = 200
MAX_RETRIES = 2
RETRY_SLEEP = 2  # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at {path}. Run transform.py first.")
    df = pd.read_csv(path, parse_dates=["time"])
    logger.info("Read CSV with %d rows", len(df))
    return df


def normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    - Drop index column
    - NaN/NaT -> None
    - time -> ISO string
    - Map aqi_pm25 -> aqi_category, severity -> severity_score, risk -> risk_flag
    - Ensure hour is int or None
    """
    # Drop index if present
    row.pop("index", None)

    normalized: Dict[str, Any] = {}

    for key, value in row.items():
        # Convert NaN/NaT to None
        if pd.isna(value):
            normalized[key] = None
            continue

        if key == "time":
            # Convert pandas Timestamp or string to ISO string
            if hasattr(value, "isoformat"):
                normalized[key] = value.isoformat()
            else:
                normalized[key] = str(value)
        elif key == "hour":
            try:
                normalized[key] = int(value)
            except Exception:
                normalized[key] = None
        else:
            normalized[key] = value

    # Rename columns to match DB schema
    rename_map = {
        "aqi_pm25": "aqi_category",
        "severity": "severity_score",
        "risk": "risk_flag",
    }
    for old, new in rename_map.items():
        if old in normalized:
            normalized[new] = normalized.pop(old)

    # Keep only DB columns
    db_cols = [
        "city",
        "time",
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone",
        "uv_index",
        "aqi_category",
        "severity_score",
        "risk_flag",
        "hour",
    ]
    return {c: normalized.get(c) for c in db_cols}


def insert_batch(client: Client, rows: List[Dict[str, Any]]) -> None:
    """
    Insert a batch, with simple retry logic.
    Raises an exception if all attempts fail.
    """
    attempt = 0
    while attempt <= MAX_RETRIES:
        attempt += 1
        try:
            logger.info("Inserting batch of %d rows (attempt %d)", len(rows), attempt)
            client.table(TABLE_NAME).insert(rows).execute()
            logger.info("Batch inserted successfully")
            return
        except Exception as e:
            logger.error("Batch insert failed: %s", e)
            if attempt > MAX_RETRIES:
                raise
            sleep_for = RETRY_SLEEP * attempt
            logger.info("Retrying in %d seconds...", sleep_for)
            time.sleep(sleep_for)


def load_to_supabase(df: pd.DataFrame, client: Client) -> None:
    # Convert to list of dicts and normalize
    records = [normalize_row(r) for r in df.to_dict(orient="records")]

    total_rows = len(records)
    inserted_rows = 0
    failed_batches = 0

    for start in range(0, total_rows, BATCH_SIZE):
        batch = records[start:start + BATCH_SIZE]
        try:
            insert_batch(client, batch)
            inserted_rows += len(batch)
        except Exception:
            failed_batches += 1
            logger.exception(
                "Failed to insert batch rows %d-%d",
                start + 1,
                start + len(batch),
            )

    # Print summary
    print("\n=== LOAD SUMMARY ===")
    print("Total rows:", total_rows)
    print("Rows inserted:", inserted_rows)
    print("Batches attempted:", (total_rows + BATCH_SIZE - 1) // BATCH_SIZE)
    print("Failed batches:", failed_batches)


def main():
    logger.info("Starting load job")
    client = get_supabase_client()
    df = read_csv(CSV_PATH)
    load_to_supabase(df, client)
    logger.info("Load job finished")


if __name__ == "__main__":
    main()
