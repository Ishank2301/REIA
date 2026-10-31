# 🏠 REIA — Real Estate Investment Advisor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/MLflow-Experiment%20Tracking-0194E2?logo=mlflow&logoColor=white" alt="MLflow" />
  <img src="https://img.shields.io/badge/XGBoost-Champion%20Model-0B7A75?logo=xgboost&logoColor=white" alt="XGBoost" />
</p>

A full-stack, data-driven real estate intelligence platform for evaluating Indian residential properties. REIA combines machine learning, market benchmarking, and an interactive dashboard to answer two key questions:

- Is this property a good investment?
- What is its likely value after 5 years?

Live Demo: https://reia-studio.ai.studio/

## Why REIA?

Real estate decisions involve more than just price and location. REIA brings together:

- ML-based investment classification
- 5-year valuation forecasting
- city-tier and micro-market benchmarks
- explainable rule-based scoring
- interactive property exploration
- deployment-ready Streamlit app
- end-to-end experiment tracking with MLflow

This project is designed for buyers, investors, and analysts who need a fast, practical way to assess residential opportunity in the Indian housing market.

## Key Features

### 1. Smart Investment Classification
REIA classifies each property as:

- Good Investment
- Average / Moderate
- Caution / High Risk

This decision is based on a six-rule framework combining valuation, home configuration, possession status, growth potential, infrastructure quality, and amenities.

### 2. 5-Year Price Forecasting
The system predicts likely future resale value and annualized appreciation using regression models trained on structured housing attributes.

### 3. Explainable Decision Logic
Each recommendation includes:

- rule score breakdown
- confidence score
- strengths and caution flags
- projected price range and ROI estimate

### 4. Indian City Benchmarking
The app supports real-world city-level comparisons across major Indian metros and emerging markets, including:

- Tier 1 cities like Bengaluru, Mumbai, Hyderabad, Pune, Chennai, and Delhi NCR
- Tier 2 cities like Jaipur, Kochi, Lucknow, Indore, Goa, and others
- base growth assumptions by city tier
- median price and area benchmarking

### 5. Property Explorer
Explore a sample catalog of curated properties and filter by:

- city
- BHK configuration
- verdict category
- investment risk profile

### 6. MLflow Experiment Tracking
The training pipeline logs all experiments with MLflow, including:

- classification model runs
- regression model runs
- parameter tracking
- metrics comparison
- champion model registration

### 7. Deployment-Ready Web App
The app is built in Streamlit and can be run locally or deployed to public hosting services.

## Project Overview

REIA follows a practical ML workflow:

1. Data ingestion and raw housing dataset loading
2. Data cleaning and preprocessing
3. Feature engineering and market feature generation
4. Target construction based on investment assumptions
5. Training multiple classification and regression models
6. Model comparison and champion selection
7. Logging to MLflow
8. Serving predictions through a Streamlit dashboard

## Tech Stack

- Python 3.10+
- Pandas and NumPy
- scikit-learn
- XGBoost
- Streamlit
- MLflow
- Matplotlib / Plotting utilities
- SQLite for local tracking

## Live App

Open the application here:

https://reia-studio.ai.studio/

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Ishank2301/REIA.git
cd REIA
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app/streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

## Full Pipeline Commands

The repository includes scripts for end-to-end workflow execution.

```bash
# Download full dataset (if needed)
python -m src.download_data

# Train models and generate processed dataset
python -m src.train

# Run EDA generation and report export
python -m src.eda

# Launch MLflow UI
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

You can also execute the full workflow in one shot:

```bash
./run_all.sh
```

## Model Architecture

The project currently trains and compares multiple models across two prediction tasks:

### Classification: Good Investment?
- Logistic Regression
- Random Forest
- XGBoost

### Regression: 5-Year Price Forecast
- Ridge Regression
- Random Forest
- XGBoost

The champion models are registered and tracked by MLflow.

## Evaluation Highlights

Results from the bundled sample dataset (5,957 rows, 80/20 split):

| Task | Best Model | Result |
|---|---|---|
| Good Investment Classification | XGBoost | Accuracy: 0.977, F1: 0.972, ROC-AUC: 0.998 |
| 5-Year Price Prediction | XGBoost | RMSE: 8.04 L, MAE: 5.54 L, R²: 0.998 |

In addition to raw performance, the app provides model interpretability through:

- rule-based investment scoring
- financial and valuation explanations
- ranking of key feature importance
- confidence outputs for each recommendation

## Repository Structure

```text
REIA/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── processed/
│   └── raw/
├── docs/
│   └── PROJECT_REPORT.md
├── models/
├── reports/
│   ├── eda/
│   └── eda_findings.md
├── src/
│   ├── config.py
│   ├── download_data.py
│   ├── eda.py
│   ├── features.py
│   ├── train.py
│   └── utils.py
├── app_sample.csv
├── HOW_TO_RUN.md
├── README.md
├── requirements.txt
├── run_all.sh
├── mlflow.db
└── .gitignore
```

## Data and Assumptions

Important note: this project uses a synthetic or rule-defined housing dataset for target creation rather than historical observed future prices.

The project explicitly assumes:

- investment labels are generated using heuristic rules in `src/config.py`
- future prices are derived from annual growth assumptions by city tier and feature conditions
- price trends are built from property attributes such as age, amenities, floor ratio, and urban infrastructure
- the dataset does not contain direct historical future-price outcomes

This means the system is best understood as a practical decision-support model based on structured assumptions, not a fully real-world transaction history predictor.

## App Features in Detail

### Advisor Dashboard
The home tab enables users to input:

- city
- property type
- BHK
- current price
- built-up area
- floor number
- total floors
- property age
- possession status
- infrastructure score
- transport score
- school score
- selected amenities

The app then produces:

- verdict with confidence
- cost vs median benchmarking
- 5-year future price estimation
- 90% forecast range
- investment strengths
- caution flags
- annualized growth projection

### Market Explorer
Users can browse a curated list of property samples by location and investment profile, making quick comparisons across different listings.

### EDA and Insights
The project includes exploratory analysis covering:

- price and size distribution
- city-tier growth behavior
- floor number anomalies
- amenities premium indicator
- macro city-level investment patterns

### Financial Analysis
The financial tab includes:

- EMI estimation
- mortgage calculation
- down payment model
- monthly cash flow
- rental yield estimate
- 5-year ROE simulation

## Deployment

### Local Deployment
```bash
streamlit run app/streamlit_app.py
```

### Cloud Deployment
This project is compatible with hosting platforms such as:

- Streamlit Community Cloud
- Hugging Face Spaces
- Azure App Service
- Docker-based deployment patterns

The app is structured to support fast deployment with minimal configuration.

## Contributing

Contributions are welcome. If you want to improve the model, add new market features, improve the dashboard UX, or expand city coverage:

1. Fork the repo
2. Create a feature branch
3. Implement your changes
4. Submit a pull request

## Notes

This repository is designed as both:

- a practical real-estate investment assistant
- a machine learning project example with actionable analytics and deployment-ready UI

It is useful for portfolio evaluation, neighborhood comparison, and investment screening workflows.

## Acknowledgements

This project is built for demonstrating the intersection of:

- predictive analytics
- investment decision support
- productized data science
- web-based dashboard deployment

## Contact / Project Access

Repository: https://github.com/Ishank2301/REIA

Live App: https://reia-studio.ai.studio/

---

If you want, I can also create a second version of this README tailored specifically for GitHub marketing style, making it more visually premium and startup-like, while keeping the technical depth intact.
