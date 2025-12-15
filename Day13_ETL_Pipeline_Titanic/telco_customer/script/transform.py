# ===========================
# transform.py
# ===========================
 
import os
import pandas as pd
 
# Purpose: Clean and transform Titanic dataset
def transform_data(raw_path):
    # Ensure the path is relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # go up one level
    staged_dir = os.path.join(base_dir, "data", "staged")
    os.makedirs(staged_dir, exist_ok=True)
 
    df = pd.read_csv(r'C:\aids_training_day1\Day13_ETL_Pipeline_Titanic\WA_Fn-UseC_-Telco-Customer-Churn.csv', encoding='ISO-8859-1')

    df['TotalCharges']=pd.to_numeric(df['TotalCharges'],errors='coerce')
 
    # --- 1️⃣ Handle missing values ---
    df['TotalCharges']=df['TotalCharges'].fillna(df['TotalCharges']).median()
    df['TotalCharges']
 
    # --- 2️⃣ Feature engineering ---
    def tenure_group(t):
        if t<=12:
            return "New"
        elif t<36:
            return "Regular"
        elif t<=60:
            return "Loyal"
        else:
            return "Champion"
    df["tenure_group"]=df["tenure"].apply(tenure_group)

    def monthly_charge_segment(m):
        if m<30:
            return "Low"
        elif (m>30 and m<70):
            return "Medium"
        elif m>70:
            return "High"
    df["monthly_charge_segment"]=df["MonthlyCharges"].apply(monthly_charge_segment)

    def has_internet_service(it):
        if (it=="DSL" or it=="Fiber optic"):
            return 1
        elif it=="No" :
            return 0
    df["has_internet_service"]=df["InternetService"].apply(has_internet_service)

    def is_multi_line_user(m):
        if (m=="Yes"):
            return 1
        else:
            return 0
    df["is_multi_line_user"]=df["MultipleLines"].apply(is_multi_line_user)

    contract_map = {
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    }
    df["contract_type_code"] = df["Contract"].map(contract_map)


    # --- 3️⃣ Drop unnecessary columns ---
    df.drop(["customerID", "gender"], axis=1, inplace=True)
 
    # --- 4️⃣ Save transformed data ---
    staged_path = os.path.join(staged_dir, "telco_customer_transformed.csv")
    df.to_csv(staged_path, index=False)
    print(f"✅ Data transformed and saved at: {staged_path}")
    return staged_path
 
 
if __name__ == "__main__":
    from extract import extract_data
    raw_path = extract_data()
    transform_data(raw_path)
 