# 🏠 Real Estate Investment Advisor
Predicting property profitability (**Good Investment?** classification) and **price after 5 years** (regression) for Indian housing listings, with MLflow experiment tracking and a Streamlit app.

## Quick start
```bash
pip install -r requirements.txt
python -m src.download_data      # full dataset (~250k rows) from the brief's Drive link; skip to use the bundled 5,957-row sample
python -m src.train              # clean -> features -> targets -> train 6 models -> log to MLflow -> register champions
python -m src.eda                # 20 EDA questions -> reports/eda_findings.md + reports/eda/*.png
streamlit run app/streamlit_app.py
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Or run everything: `./run_all.sh`. For a faster run on the full file: `python -m src.train --max-rows 100000`.

The repo ships with models trained on the **bundled sample** so the app works immediately. **Retrain on the full CSV for final numbers.**

## What's in the box (matches the brief's deliverables)
| Deliverable | Where |
|---|---|
| Cleaned & processed dataset | `data/processed/housing_processed.csv` (created by `src.train`), `app_sample.csv` |
| Python scripts: EDA, training, evaluation | `src/eda.py`, `src/train.py`, `src/features.py` |
| MLflow experiment logs + registered models | created by `src.train` (`mlflow.db`, `mlruns/`); models `RealEstate_GoodInvestment_Classifier`, `RealEstate_Future_Price_Regressor` (alias `champion`) |
| Streamlit app (prediction + insights) | `app/streamlit_app.py` |
| Documentation | this README, `docs/PROJECT_REPORT.md`, `reports/eda_findings.md` |

## Pipeline
1. **Preprocessing** (`features.clean`): strip names/strings, drop duplicates, impute (median / mode), drop impossible rows, recompute age, flag + cap `Floor_No > Total_Floors`.
2. **Features** (`features.add_features`): price/sq ft recomputed in Rs (the dataset column is rounded to 0.01 lakh), amenity flags + count, infrastructure score, school density score, transport score, floor ratio, price-vs-city/type-median ratio, winsorised price/sq ft. Scaling (`StandardScaler`) and one-hot encoding happen inside the sklearn pipeline.
3. **Targets** (assumption-based, all in `src/config.py`): annual growth = city-tier base (8/7/6%) + adjustments (transport, infrastructure, availability, type, age) + small noise; `Future = Current × (1+r)^5`. *Good Investment* = multi-factor score ≥ 4/6 (the brief's "price vs median + BHK ≥ 3 + ready-to-move + appreciation" idea).
4. **Models**: Logistic Regression / Random Forest / XGBoost (classification: accuracy, precision, recall, F1, ROC-AUC, confusion matrix); Ridge / Random Forest / XGBoost (regression: RMSE, MAE, R²). Best of each is registered in the MLflow model registry and saved to `models/`.
5. **App**: input form → verdict + probability + rule-score breakdown, 5-year price with 90% range and growth chart, filterable property explorer with model ranking, market insight charts, model-performance page.

## Results on the bundled sample (5,957 rows, 80/20 split)
| Task | Best model | Result | Baseline |
|---|---|---|---|
| Good Investment | XGBoost | acc 0.977, F1 0.972, AUC 0.998 | majority class 0.587 acc; "price below median" rule alone 0.814 acc |
| 5-year price | XGBoost | RMSE 8.04 L, MAE 5.54 L, R² 0.998 | flat 8% growth: RMSE 25.8 L; noise floor: 7.7 L |

## ⚠️ Read before you present this
- **The labels are assumptions, not observed outcomes.** The dataset has no historical or future prices, so "price after 5 years" and "Good Investment" are *defined by rules* in `config.py`. The models learn to reproduce those rules, so high accuracy/R² show the pipeline works, **not** that it forecasts the real market. Say this in your viva/report; the baselines in the table are the honest comparison.
- **The data behaves like synthetic data**: price vs size correlation ≈ 0, flat (uniform) distributions, nearly identical average prices across 42 cities, ~47% of rows with floor number above total floors. EDA answers say so rather than inventing patterns.
- **Not in the dataset** (but named in the brief): crime rate, RERA status. They are not used.
- "Price trends" use construction year, since there are no listing dates.
- Results above come from the 5,957-row sample; the full-file run was not executed here.
