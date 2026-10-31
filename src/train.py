"""Model training pipeline: trains 6 models, tracks in MLflow, and registers champions."""

import argparse
import logging
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score
)

import mlflow
import mlflow.sklearn

from src.config import (
    RAW_DATA_PATH, PROCESSED_DATA_PATH, PROCESSED_DATA_DIR, MODELS_DIR,
    MLFLOW_TRACKING_URI, EXPERIMENT_NAME, MODEL_CLASSIFIER_NAME,
    MODEL_REGRESSOR_NAME, CHAMPION_ALIAS
)
from src.download_data import ensure_dataset
from src.features import clean, add_features

try:
    from xgboost import XGBClassifier, XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

NUMERIC_FEATURES = [
    "BHK", "Size_in_SqFt", "Price_in_Lakhs", "Floor_Ratio", "Amenities_Count",
    "Infrastructure_Score", "Transport_Score", "School_Density_Score",
    "Price_vs_City_Median_Ratio"
]
CATEGORICAL_FEATURES = ["City", "Property_Type", "Possession_Status", "City_Tier"]

def run_training(max_rows=None):
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    data_file = ensure_dataset()
    logger.info(f"Loading raw data from {data_file}")
    df = pd.read_csv(data_file)
    if max_rows and len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=42)

    logger.info("Running preprocessing (features.clean)...")
    cleaned_df = clean(df)
    
    logger.info("Computing engineered features & targets (features.add_features)...")
    processed_df = add_features(cleaned_df)
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)
    logger.info(f"Saved processed dataset to {PROCESSED_DATA_PATH}")

    # Prepare features and targets
    X = processed_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_clf = processed_df["Is_Good_Investment"]
    y_reg = processed_df["Future_Price_5Yr"]

    X_train, X_test, y_clf_train, y_clf_test, y_reg_train, y_reg_test = train_test_split(
        X, y_clf, y_reg, test_size=0.20, random_state=42, stratify=y_clf
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )

    # Classification Models
    clf_models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
    }
    if HAS_XGB:
        clf_models["XGBoostClassifier"] = XGBClassifier(
            n_estimators=120, max_depth=5, learning_rate=0.08, eval_metric="logloss", random_state=42
        )

    # Regression Models
    reg_models = {
        "Ridge": Ridge(alpha=1.0, random_state=42),
        "RandomForestRegressor": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
    }
    if HAS_XGB:
        reg_models["XGBoostRegressor"] = XGBRegressor(
            n_estimators=120, max_depth=5, learning_rate=0.08, random_state=42
        )

    best_clf_f1 = -1
    best_clf_name = None
    best_clf_pipe = None

    best_reg_r2 = -1
    best_reg_name = None
    best_reg_pipe = None

    # Train Classifiers
    logger.info("--- Training Classification Models ---")
    for name, model in clf_models.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])
        pipe.fit(X_train, y_clf_train)
        y_pred = pipe.predict(X_test)
        
        acc = accuracy_score(y_clf_test, y_pred)
        f1 = f1_score(y_clf_test, y_pred)
        auc = roc_auc_score(y_clf_test, pipe.predict_proba(X_test)[:, 1])
        logger.info(f"[{name}] Acc: {acc:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

        if f1 > best_clf_f1:
            best_clf_f1 = f1
            best_clf_name = name
            best_clf_pipe = pipe

    # Train Regressors
    logger.info("--- Training Regression Models ---")
    for name, model in reg_models.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])
        pipe.fit(X_train, y_reg_train)
        y_pred = pipe.predict(X_test)
        
        rmse = np.sqrt(mean_squared_error(y_reg_test, y_pred))
        mae = mean_absolute_error(y_reg_test, y_pred)
        r2 = r2_score(y_reg_test, y_pred)
        logger.info(f"[{name}] RMSE: {rmse:.2f}L | MAE: {mae:.2f}L | R2: {r2:.4f}")

        if r2 > best_reg_r2:
            best_reg_r2 = r2
            best_reg_name = name
            best_reg_pipe = pipe

    # Save Best Models
    logger.info(f"Registering Champion Classifier: {best_clf_name} (F1: {best_clf_f1:.4f})")
    joblib.dump(best_clf_pipe, MODELS_DIR / f"{MODEL_CLASSIFIER_NAME}.joblib")

    logger.info(f"Registering Champion Regressor: {best_reg_name} (R2: {best_reg_r2:.4f})")
    joblib.dump(best_reg_pipe, MODELS_DIR / f"{MODEL_REGRESSOR_NAME}.joblib")

    logger.info("Models saved to models/ directory successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=None, help="Max rows to train on")
    args = parser.parse_args()
    run_training(max_rows=args.max_rows)
