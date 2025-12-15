# run_pipeline.py

import time

from extract import extract_all_cities          # or your main extract fn
from transform import main as transform_main    # or transform_all(...)
from load import main as load_main              # or load_to_supabase(...)
from etl_analysis import main as analysis_main  # or run_analysis(...)


def run_full_pipeline():
    # 1) Extract
    print("Step 1: Extract...")
    extract_all_cities()        # adjust to your real function name
    time.sleep(1)               # small pause (optional)

    # 2) Transform
    print("Step 2: Transform...")
    transform_main()

    # 3) Load
    print("Step 3: Load...")
    load_main()

    # 4) Analyze
    print("Step 4: Analyze...")
    analysis_main()

    print("✅ Pipeline finished.")


if __name__ == "__main__":
    run_full_pipeline()
