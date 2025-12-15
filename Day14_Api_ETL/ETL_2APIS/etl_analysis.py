''' 🟩 4️⃣ Analysis (etl_analysis.py)
Read the loaded data from Supabase and perform:
A. KPI Metrics
City with highest average PM2.5
City with the highest severity score
Percentage of High/Moderate/Low risk hours
Hour of day with worst AQI

B. City Pollution Trend Report
For each city:
time → pm2_5, pm10, ozone

C. Export Outputs
Save the following CSVs into data/processed/:
summary_metrics.csv
city_risk_distribution.csv
pollution_trends.csv

D. Visualizations
Save the following PNG plots:
Histogram of PM2.5
Bar chart of risk flags per city
Line chart of hourly PM2.5 trends
Scatter: severity_score vs pm2_5'''

import os
import logging

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from supabase import create_client, Client

# --- Config ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

TABLE_NAME = "air_quality_data"
OUTPUT_DIR = os.path.join("data", "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_data(client: Client) -> pd.DataFrame:
    """
    Load full table from Supabase into a pandas DataFrame.
    Adjust select() if you want specific columns only.
    """
    logger.info("Fetching data from Supabase...")
    resp = client.table(TABLE_NAME).select("*").execute()  # [web:1]
    data = resp.data  # supabase-py returns .data as list[dict]
    df = pd.DataFrame(data)

    # Ensure time is datetime and hour is int
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])
    if "hour" in df.columns:
        df["hour"] = pd.to_numeric(df["hour"], errors="coerce").astype("Int64")

    logger.info("Loaded %d rows from Supabase", len(df))
    return df


def compute_kpi_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    A. KPI Metrics
    - City with highest average PM2.5
    - City with highest average severity score
    - Percentage of High/Moderate/Low risk hours
    - Hour of day with worst AQI (highest avg pm2_5)
    """
    metrics = {}

    # City with highest avg PM2.5
    pm25_by_city = df.groupby("city")["pm2_5"].mean().sort_values(ascending=False)
    if not pm25_by_city.empty:
        metrics["city_highest_avg_pm25"] = pm25_by_city.index[0]
        metrics["highest_avg_pm25_value"] = pm25_by_city.iloc[0]

    # City with highest avg severity_score
    if "severity_score" in df.columns:
        sev_by_city = df.groupby("city")["severity_score"].mean().sort_values(ascending=False)
        if not sev_by_city.empty:
            metrics["city_highest_severity"] = sev_by_city.index[0]
            metrics["highest_severity_value"] = sev_by_city.iloc[0]

    # Percentage of High/Moderate/Low risk hours
    if "risk_flag" in df.columns:
        risk_counts = df["risk_flag"].value_counts(dropna=True)
        risk_pct = (risk_counts / risk_counts.sum()) * 100
        # Fill missing risk levels with 0
        for level in ["High", "Moderate", "Low"]:
            metrics[f"pct_{level.lower()}_risk_hours"] = float(risk_pct.get(level, 0.0))

    # Hour of day with worst AQI (using pm2_5 as AQI proxy)
    if "hour" in df.columns:
        hour_pm25 = df.groupby("hour")["pm2_5"].mean().sort_values(ascending=False)
        if not hour_pm25.empty:
            metrics["worst_hour_pm25"] = int(hour_pm25.index[0])
            metrics["worst_hour_pm25_value"] = hour_pm25.iloc[0]

    summary_metrics_df = pd.DataFrame([metrics])
    return summary_metrics_df


def city_risk_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage/count of each risk_flag per city.
    """
    if "risk_flag" not in df.columns:
        return pd.DataFrame()

    counts = (
        df.groupby(["city", "risk_flag"])
        .size()
        .reset_index(name="count")
    )
    total_per_city = counts.groupby("city")["count"].transform("sum")
    counts["percentage"] = counts["count"] / total_per_city * 100
    return counts


def pollution_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    B. City Pollution Trend Report
    For each city: time, pm2_5, pm10, ozone
    (Just subset the columns; caller can group/plot later.)
    """
    cols = ["city", "time", "pm2_5", "pm10", "ozone"]
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols].sort_values(["city", "time"])


def save_csvs(summary_df, risk_df, trends_df):
    """
    C. Export Outputs
    Save summary_metrics.csv, city_risk_distribution.csv, pollution_trends.csv
    into data/processed/
    """
    summary_path = os.path.join(OUTPUT_DIR, "summary_metrics.csv")
    risk_path = os.path.join(OUTPUT_DIR, "city_risk_distribution.csv")
    trends_path = os.path.join(OUTPUT_DIR, "pollution_trends.csv")

    summary_df.to_csv(summary_path, index=False)  # [web:9]
    risk_df.to_csv(risk_path, index=False)
    trends_df.to_csv(trends_path, index=False)

    logger.info("Saved CSVs to %s", OUTPUT_DIR)


def create_plots(df: pd.DataFrame):
    """
    D. Visualizations (saved as PNGs):
    - Histogram of PM2.5
    - Bar chart of risk flags per city
    - Line chart of hourly PM2.5 trends
    - Scatter: severity_score vs pm2_5
    """
    # Histogram of PM2.5
    if "pm2_5" in df.columns:
        plt.figure()
        df["pm2_5"].dropna().plot(kind="hist", bins=30)
        plt.title("Histogram of PM2.5")
        plt.xlabel("PM2.5")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "hist_pm25.png"))
        plt.close()

    # Bar chart of risk flags per city
    if "risk_flag" in df.columns:
        plt.figure()
        risk_counts = df.groupby(["city", "risk_flag"]).size().unstack(fill_value=0)
        risk_counts.plot(kind="bar", stacked=True)
        plt.title("Risk Flags per City")
        plt.xlabel("City")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "bar_risk_flags_per_city.png"))
        plt.close()

    # Line chart of hourly PM2.5 trends
    if "hour" in df.columns and "pm2_5" in df.columns:
        plt.figure()
        hourly_pm25 = df.groupby("hour")["pm2_5"].mean().sort_index()
        hourly_pm25.plot(kind="line", marker="o")
        plt.title("Hourly PM2.5 Trend")
        plt.xlabel("Hour of Day")
        plt.ylabel("Average PM2.5")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "line_hourly_pm25.png"))
        plt.close()

    # Scatter: severity_score vs pm2_5
    if "severity_score" in df.columns and "pm2_5" in df.columns:
        plt.figure()
        plt.scatter(df["pm2_5"], df["severity_score"], alpha=0.5)
        plt.title("Severity Score vs PM2.5")
        plt.xlabel("PM2.5")
        plt.ylabel("Severity Score")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "scatter_severity_vs_pm25.png"))
        plt.close()

    logger.info("Saved plots to %s", OUTPUT_DIR)


def main():
    client = get_supabase_client()
    df = fetch_data(client)

    # A. KPI Metrics
    summary_df = compute_kpi_metrics(df)

    # A (part) + B. City risk distribution + Pollution trends
    risk_df = city_risk_distribution(df)
    trends_df = pollution_trends(df)

    # C. Export CSVs
    save_csvs(summary_df, risk_df, trends_df)

    # D. Visualizations
    create_plots(df)


if __name__ == "__main__":
    main()




