"""Configuration, city-tier definitions, target rules, and directory paths for REIA."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
EDA_REPORTS_DIR = REPORTS_DIR / "eda"

RAW_DATA_PATH = RAW_DATA_DIR / "housing_raw.csv"
SAMPLE_DATA_PATH = BASE_DIR / "app_sample.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "housing_processed.csv"

# MLflow Tracking
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "RealEstate_Investment_Advisor"
MODEL_CLASSIFIER_NAME = "RealEstate_GoodInvestment_Classifier"
MODEL_REGRESSOR_NAME = "RealEstate_Future_Price_Regressor"
CHAMPION_ALIAS = "champion"

# City Tiers and Base Annual Capital Growth
CITY_TIERS = {
    "Tier 1": {
        "cities": ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Pune", "Chennai", "Kolkata", "Ahmedabad"],
        "base_growth": 0.080  # 8.0%
    },
    "Tier 2": {
        "cities": [
            "Jaipur", "Kochi", "Chandigarh Tri-City", "Lucknow", "Indore", "Surat", 
            "Coimbatore", "Visakhapatnam", "Nagpur", "Bhopal", "Bhubaneswar", "Patna", 
            "Ludhiana", "Agra", "Nashik", "Rajkot", "Varanasi", "Meerut", "Raipur", 
            "Guwahati", "Amritsar", "Jodhpur", "Goa"
        ],
        "base_growth": 0.070  # 7.0%
    },
    "Tier 3": {
        "cities": ["Dehradun", "Ranchi", "Mangaluru", "Mysuru", "Udaipur", "Other"],
        "base_growth": 0.060  # 6.0%
    }
}

# Rule Thresholds for Good Investment Classification
GOOD_INVESTMENT_RULES = {
    "price_vs_median_threshold": 1.05,
    "min_bhk": 3,
    "min_annual_growth": 0.075,
    "min_infra_score": 6,
    "min_transport_score": 6,
    "min_amenities_count": 4,
    "max_floor_ratio": 0.85,
    "passing_score_threshold": 4  # Score >= 4/6 criteria
}
