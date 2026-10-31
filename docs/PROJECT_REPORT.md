# 📑 Real Estate Investment Advisor (REIA) - Project Report

## Executive Summary
REIA provides machine learning driven decision support for Indian residential property acquisitions. It evaluates current market listings, flags profitability via multi-factor classification, and forecasts continuous 5-year future valuation.

## System Architecture
- **Data Pipeline**: Automated ingestion, imputation, outlier winsorization, and feature engineering.
- **Classification Pipeline**: Predicts binary *Good Investment* outcome using XGBoost (champion), Random Forest, and Logistic Regression.
- **Regression Pipeline**: Estimates 5-year asset price using XGBoost Regressor (champion), Random Forest, and Ridge.
- **Experiment Tracking**: Managed via MLflow model registry (`mlflow.db`) with model artifacts logged in `./mlruns`.
- **User Interface**: Available via Streamlit (`app/streamlit_app.py`) and Web SPA.

## Model Benchmarks (Bundled Sample, 80/20 Train-Test Split)
| Task | Champion Model | Score | Baseline |
|---|---|---|---|
| Good Investment Classifier | XGBoost | Accuracy 0.977, F1 0.972, AUC 0.998 | Majority class: 0.587 |
| 5-Year Price Regressor | XGBoost | RMSE 8.04 Lakhs, MAE 5.54 Lakhs, R² 0.998 | Flat 8% growth: 25.8 L |
