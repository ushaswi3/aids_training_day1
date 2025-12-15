'''VALIDATION SCRIPT (validate.py)
After load, write a script that checks:
No missing values in:
tenure, MonthlyCharges, TotalCharges
Unique count of rows = original dataset
Row count matches Supabase table
All segments (tenure_group, monthly_charge_segment) exist
Contract codes are only {0,1,2}
Print a validation summary.
 '''

# validate.py
# Purpose: Validate loaded data in Supabase after import

import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

def get_supabase_client():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

def validate(staged_csv_path: str, table_name: str = "telco_customer"):
    # read local staged file
    if not os.path.isabs(staged_csv_path):
        staged_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), staged_csv_path))

    if not os.path.exists(staged_csv_path):
        print(f"❌ Staged file not found at {staged_csv_path}. Run transform.py and load.py first.")
        return

    df = pd.read_csv(staged_csv_path)
    original_count = len(df)
    print(f"ℹ️  Original staged rows: {original_count}")

    # Prepare column names (same normalization as load.py)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Checks to run
    checks = []
    # 1. No missing values in tenure, monthlycharges, totalcharges
    for col in ["tenure", "monthlycharges", "totalcharges"]:
        if col in df.columns:
            missing = df[col].isna().sum()
            checks.append((f"missing_{col}", missing == 0, missing))
        else:
            checks.append((f"column_missing_{col}", False, f"{col} not in staged file"))

    # 2. Unique count of rows = original dataset 
    checks.append(("unique_count_equals_total", df.drop_duplicates().shape[0] == original_count, df.drop_duplicates().shape[0]))

    # 3. Connect to Supabase and fetch counts
    supabase = get_supabase_client()
    try:
        resp = supabase.table(table_name).select("count", count="exact").execute()
        if isinstance(resp, dict):
            error = resp.get("error")
            data = resp.get("data")
        else:
            error = getattr(resp, "error", None)
            data = getattr(resp, "data", None)

        if error:
            print(f"⚠️  Could not fetch count from Supabase: {error}")
            supabase_count = None
        else:
            # When using select count='exact', data may be empty and the client returns count in metadata.
            # Fallback: fetch all rows and count (works but may be heavy for big tables)
            # Safer: perform a simple select of primary key
            fetch = supabase.table(table_name).select("id", count="exact").execute()
            if isinstance(fetch, dict):
                supabase_count = fetch.get("count", None)
            else:
                supabase_count = getattr(fetch, "count", None)
    except Exception as e:
        print(f"⚠️  Exception querying Supabase: {e}")
        supabase_count = None

    checks.append(("supabase_row_count_matches", supabase_count == original_count if supabase_count is not None else False, supabase_count))

    # 4. All segments exist: tenure_group, monthly_charge_segment
    for seg in ["tenure_group", "monthly_charge_segment"]:
        exists = seg in df.columns and df[seg].notna().any()
        checks.append((f"segment_{seg}_exists", exists, None if exists else f"{seg} missing or all NaN"))

    # 5. Contract codes only in {0,1,2}
    if "contract_type_code" in df.columns:
        unique_codes = set(df["contract_type_code"].dropna().unique().astype(int))
        allowed = {0,1,2}
        ok = unique_codes.issubset(allowed)
        checks.append(("contract_codes_valid", ok, unique_codes))
    else:
        checks.append(("contract_codes_valid", False, "contract_type_code column not found"))

    # Print summary
    print("\n=== VALIDATION SUMMARY ===")
    for name, ok, info in checks:
        status = "OK" if ok else "FAIL"
        print(f"- {name}: {status} -> {info}")
    print("==========================")

if __name__ == "__main__":
    staged_csv_path = os.path.join("..", "data", "staged", "telco_customer_transformed.csv")
    validate(staged_csv_path)





