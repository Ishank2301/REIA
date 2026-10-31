# 🚀 How to Run & Deploy REIA (Real Estate Investment Advisor)

This guide explains all methods to run and deploy the REIA site and machine learning pipeline.

---

## 🌐 Method 1: Instant Live Cloud Applet (Active Now)

The interactive dashboard is compiled and running live on Google Cloud Run:
- **Development Server:** `https://ais-dev-zvuau5shqhgnvc7pcigf7l-218192041272.asia-southeast1.run.app`
- **Public Shareable Preview:** `https://ais-pre-zvuau5shqhgnvc7pcigf7l-218192041272.asia-southeast1.run.app`

---

## 💻 Method 2: Run This Web Dashboard Locally (React + Vite)

### Prerequisites:
- Node.js (v18 or v20+)
- npm (comes with Node.js)

### Commands:
```bash
# 1. Clone the repository
git clone https://github.com/Ishank2301/REIA.git
cd REIA

# 2. Install dependencies
npm install

# 3. Start local development server
npm run dev
```

Once started, open your browser and go to:
👉 **`http://localhost:3000`**

To create a static production build:
```bash
npm run build
npm run preview
```

---

## 🐍 Method 3: Run the Python Machine Learning Pipeline & Streamlit App

### Prerequisites:
- Python 3.9, 3.10, or 3.11

### Step 1: Clone and Set Up Virtual Environment
```bash
git clone https://github.com/Ishank2301/REIA.git
cd REIA

# Create and activate virtual environment
python3 -m venv venv

# On macOS / Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run Automated Pipeline
```bash
# Automated run of training + EDA:
./run_all.sh

# Or run modules individually:
python -m src.download_data   # Verifies dataset / creates sample
python -m src.train           # Trains 6 models & logs to MLflow
python -m src.eda             # Executes 20 EDA questions & generates reports/eda_findings.md
```

### Step 3: Launch Streamlit Web App
```bash
streamlit run app/streamlit_app.py
```
👉 Open **`http://localhost:8501`**

### Step 4: Launch MLflow Tracking UI
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
👉 Open **`http://localhost:5000`** to view experiment parameters, evaluation metrics, and registered champion models.

---

## ☁️ Method 4: Deploying to Free Online Hosting (24/7 Availability)

### Option A: Streamlit Community Cloud (Recommended for Python app)
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository: `Ishank2301/REIA`.
4. Branch: `main`.
5. Main file path: `app/streamlit_app.py`.
6. Click **Deploy**. Your app will be live with a permanent public link.

### Option B: Vercel (Recommended for React Web App)
1. Go to [vercel.com](https://vercel.com) and log in with GitHub.
2. Click **Add New...** -> **Project**.
3. Import `Ishank2301/REIA`.
4. Framework preset will automatically detect **Vite**.
5. Click **Deploy**. Your site will be live on `https://reia-*.vercel.app`.

---

## 📁 Repository Structure Overview

| File / Folder | Purpose |
|---|---|
| `src/` | ML pipeline modules: data download, cleaning, feature engineering, and model training |
| `app/streamlit_app.py` | Streamlit interactive web interface |
| `src/config.py` | City tiers, growth assumptions, and 6-rule investment rubric |
| `reports/eda_findings.md` | Comprehensive answers to 20 EDA housing market questions |
| `docs/PROJECT_REPORT.md` | Architectural report, benchmarks, and model registry summaries |
| `package.json` | Web application dependencies and Vite scripts |
| `requirements.txt` | Python data science and machine learning dependencies |
