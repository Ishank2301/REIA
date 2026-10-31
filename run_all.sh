#!/usr/bin/env bash
set -e

echo "=== 🏠 Real Estate Investment Advisor (REIA) Pipeline ==="

echo "Step 1: Installing / verifying dependencies..."
pip install -r requirements.txt -q

echo "Step 2: Running model training and MLflow registration..."
python -m src.train "$@"

echo "Step 3: Generating EDA findings report & charts..."
python -m src.eda

echo "=== Pipeline Finished Successfully ==="
echo "To launch the web dashboard: streamlit run app/streamlit_app.py"
echo "To explore MLflow experiments: mlflow ui --backend-store-uri sqlite:///mlflow.db"
