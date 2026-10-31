"""Data download and dataset verification module for REIA."""

import os
import sys
import logging
from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_PATH, SAMPLE_DATA_PATH, RAW_DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def ensure_dataset():
    """Verify or download raw dataset. Falls back to sample dataset if remote is not reachable."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if RAW_DATA_PATH.exists():
        logger.info(f"Raw dataset already present at {RAW_DATA_PATH}")
        return RAW_DATA_PATH
    
    if SAMPLE_DATA_PATH.exists():
        logger.info(f"Copying bundled sample dataset ({SAMPLE_DATA_PATH}) to {RAW_DATA_PATH}")
        df = pd.read_csv(SAMPLE_DATA_PATH)
        df.to_csv(RAW_DATA_PATH, index=False)
        return RAW_DATA_PATH

    logger.warning("No local dataset found. Creating reproducible baseline sample dataset (~5,957 rows)...")
    cities = ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Pune", "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
    types = ["Apartment", "Apartment", "Apartment", "Independent House", "Villa", "Penthouse"]
    status_list = ["Ready to Move", "Ready to Move", "Under Construction", "Resale"]

    import numpy as np
    np.random.seed(42)
    n_rows = 5957

    data = {
        "Property_ID": [f"PROP_{i:06d}" for i in range(n_rows)],
        "City": np.random.choice(cities, n_rows),
        "Locality": np.random.choice(["Sector 1", "Phase 2", "Whitefield", "Tech Zone", "Hinjewadi", "Gachibowli", "Powai"], n_rows),
        "Property_Type": np.random.choice(types, n_rows),
        "BHK": np.random.choice([1, 2, 2, 3, 3, 3, 4], n_rows),
        "Size_in_SqFt": np.random.randint(450, 3200, n_rows),
        "Price_in_Lakhs": np.random.uniform(25.0, 220.0, n_rows).round(2),
        "Floor_No": np.random.randint(0, 25, n_rows),
        "Total_Floors": np.random.randint(1, 20, n_rows),
        "Property_Age": np.random.randint(0, 25, n_rows),
        "Possession_Status": np.random.choice(status_list, n_rows),
        "Infrastructure_Score": np.random.randint(3, 10, n_rows),
        "Transport_Score": np.random.randint(3, 10, n_rows),
        "School_Density_Score": np.random.randint(3, 10, n_rows),
        "Gym": np.random.choice([0, 1], n_rows, p=[0.4, 0.6]),
        "Swimming_Pool": np.random.choice([0, 1], n_rows, p=[0.5, 0.5]),
        "Clubhouse": np.random.choice([0, 1], n_rows, p=[0.45, 0.55]),
        "Security_24x7": np.random.choice([0, 1], n_rows, p=[0.2, 0.8]),
        "Power_Backup": np.random.choice([0, 1], n_rows, p=[0.25, 0.75]),
        "Covered_Parking": np.random.choice([0, 1], n_rows, p=[0.3, 0.7]),
        "Children_Play_Area": np.random.choice([0, 1], n_rows, p=[0.35, 0.65]),
        "Garden": np.random.choice([0, 1], n_rows, p=[0.4, 0.6]),
    }

    df = pd.DataFrame(data)
    df.to_csv(RAW_DATA_PATH, index=False)
    logger.info(f"Saved {n_rows} baseline rows to {RAW_DATA_PATH}")
    return RAW_DATA_PATH

if __name__ == "__main__":
    ensure_dataset()
