"""Feature engineering, cleaning, and preprocessing pipeline for REIA."""

import logging
import numpy as np
import pandas as pd
from src.config import CITY_TIERS, GOOD_INVESTMENT_RULES

logger = logging.getLogger(__name__)

AMENITY_COLS = [
    "Gym", "Swimming_Pool", "Clubhouse", "Security_24x7", 
    "Power_Backup", "Covered_Parking", "Children_Play_Area", "Garden"
]

def get_city_tier(city_name: str) -> str:
    for tier, data in CITY_TIERS.items():
        if city_name in data["cities"]:
            return tier
    return "Tier 2"

def get_city_base_growth(city_name: str) -> float:
    for tier, data in CITY_TIERS.items():
        if city_name in data["cities"]:
            return data["base_growth"]
    return 0.070

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess raw listing data: deduplicate, clean anomalies, and impute."""
    df = df.copy()

    # Strip strings
    str_cols = df.select_dtypes(include=["object"]).columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()

    # Drop duplicate listings
    if "Property_ID" in df.columns:
        df = df.drop_duplicates(subset=["Property_ID"])
    df = df.drop_duplicates()

    # Drop impossible price or area rows
    df = df[df["Price_in_Lakhs"] > 0]
    df = df[df["Size_in_SqFt"] > 50]

    # Floor anomaly remediation: flag & cap Floor_No > Total_Floors
    df["Floor_Anomaly"] = (df["Floor_No"] > df["Total_Floors"]).astype(int)
    df["Total_Floors"] = df["Total_Floors"].replace(0, 1)
    df["Floor_No_Capped"] = np.minimum(df["Floor_No"], df["Total_Floors"])

    # Age bounds
    if "Property_Age" in df.columns:
        df["Property_Age"] = df["Property_Age"].clip(lower=0, upper=80)

    # Impute missing numeric columns with median, categorical with mode
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived ratios, amenity counts, growth rates, and targets."""
    df = df.copy()

    # Recompute price per sq ft in Rupees
    df["Price_Per_SqFt_Rs"] = ((df["Price_in_Lakhs"] * 100000.0) / df["Size_in_SqFt"]).round(2)

    # Winsorise price per sq ft to clip extreme noise
    lower_p = df["Price_Per_SqFt_Rs"].quantile(0.01)
    upper_p = df["Price_Per_SqFt_Rs"].quantile(0.99)
    df["Winsorised_Price_Per_SqFt"] = df["Price_Per_SqFt_Rs"].clip(lower=lower_p, upper=upper_p)

    # Amenities count
    present_amenities = [c for c in AMENITY_COLS if c in df.columns]
    if present_amenities:
        df["Amenities_Count"] = df[present_amenities].sum(axis=1)
    else:
        df["Amenities_Count"] = 4

    # Floor ratio (capped between 0.0 and 1.0)
    df["Floor_Ratio"] = (df["Floor_No_Capped"] / df["Total_Floors"].clip(lower=1)).clip(0.0, 1.0).round(2)

    # City medians and price ratio
    city_medians = df.groupby("City")["Price_in_Lakhs"].transform("median")
    df["City_Median_Price"] = city_medians
    df["Price_vs_City_Median_Ratio"] = (df["Price_in_Lakhs"] / df["City_Median_Price"].clip(lower=1.0)).round(2)

    # City Tier
    df["City_Tier"] = df["City"].apply(get_city_tier)

    # Target Computation (Assumption-based annual growth r)
    base_growth = df["City"].apply(get_city_base_growth)
    transport_adj = ((df.get("Transport_Score", 5) - 5) * 0.0035)
    infra_adj = ((df.get("Infrastructure_Score", 5) - 5) * 0.0040)
    status_adj = df["Possession_Status"].map({"Ready to Move": 0.005, "Resale": 0.0, "Under Construction": -0.003}).fillna(0)
    type_adj = df["Property_Type"].map({"Villa": 0.004, "Penthouse": 0.002, "Independent House": 0.003, "Apartment": 0.0}).fillna(0)
    
    age_col = df.get("Property_Age", 2)
    age_adj = np.where(age_col <= 3, 0.005, np.where(age_col > 15, -0.006, 0.0))

    annual_r = (base_growth + transport_adj + infra_adj + status_adj + type_adj + age_adj).clip(0.04, 0.145)
    df["Annual_Growth_Rate"] = annual_r.round(4)

    # Regression Target: 5-Year Future Price in Lakhs
    df["Future_Price_5Yr"] = (df["Price_in_Lakhs"] * ((1.0 + df["Annual_Growth_Rate"]) ** 5)).round(2)

    # Classification Target: Multi-Factor Good Investment Rule (>= 4/6 criteria)
    r1 = (df["Price_vs_City_Median_Ratio"] <= GOOD_INVESTMENT_RULES["price_vs_median_threshold"]).astype(int)
    r2 = (df["BHK"] >= GOOD_INVESTMENT_RULES["min_bhk"]).astype(int)
    r3 = (df["Possession_Status"] == "Ready to Move").astype(int)
    r4 = (df["Annual_Growth_Rate"] >= GOOD_INVESTMENT_RULES["min_annual_growth"]).astype(int)
    r5 = ((df["Infrastructure_Score"] >= GOOD_INVESTMENT_RULES["min_infra_score"]) & 
          (df["Transport_Score"] >= GOOD_INVESTMENT_RULES["min_transport_score"])).astype(int)
    r6 = ((df["Amenities_Count"] >= GOOD_INVESTMENT_RULES["min_amenities_count"]) & 
          (df["Floor_Ratio"] <= GOOD_INVESTMENT_RULES["max_floor_ratio"])).astype(int)

    df["Rule_Score"] = r1 + r2 + r3 + r4 + r5 + r6
    df["Is_Good_Investment"] = (df["Rule_Score"] >= GOOD_INVESTMENT_RULES["passing_score_threshold"]).astype(int)

    return df
