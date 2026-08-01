# 🩺 PredictiBetes — AI-Powered Diabetes Prediction & Clinical Analytics Platform

> **Developer Credit**: Developed with ❤️ by **Ashwitha Ramesh**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.0-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.19.0-3F4F75.svg?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**PredictiBetes** is a full-stack, recruiter-ready Machine Learning web application designed to assess clinical diabetes risk, benchmark multiple classification algorithms, and deliver explainable AI insights.

---

## 🌟 Key Highlights

- **6 Machine Learning Algorithms**: Evaluates Logistic Regression, Random Forest, Decision Tree, Support Vector Machine (SVM), K-Nearest Neighbors (KNN), and Gaussian Naive Bayes.
- **Model Explainability (XAI)**: Identifies top risk-driving metrics (e.g., Glucose, BMI) and protective factors for every single patient assessment.
- **Multi-Step Animated Assessment**: Interactive progress loading experience (*Data Analysis ➔ Feature Evaluation ➔ ML Benchmarking ➔ Clinical Insights*).
- **Interactive Plotly Visualizations**: Heatmaps, class distributions, box plots, and scatter plots with 1-click chart download capabilities.
- **Persistent SQLite Prediction Log**: Search, filter, delete, and download prediction history as CSV.
- **CSV Batch Upload**: Upload multi-patient CSV files for instant batch prediction results.
- **Cloud Deployment Ready**: Optimized for 1-click deployment on Render, Railway, Koyeb, and Heroku without Docker or Celery complexity.

---

## 📐 Architecture & Modular Structure

```
diabetes-prediction/
├── app/
│   ├── main.py              # FastAPI application & template routing
│   ├── database.py          # SQLAlchemy SQLite connection & session management
│   ├── models.py            # PredictionRecord ORM database schema
│   ├── schemas.py           # Pydantic request/response validation schemas
│   ├── ml_model.py          # Scikit-learn ML pipeline & 6 classifier trainers
│   ├── train_model.py       # ML training script to generate best_model.pkl
│   ├── utils.py             # Logger, risk indicators & health recommendations
│   ├── routers/
│   │   ├── predict.py       # Single & batch prediction API endpoints
│   │   ├── history.py       # Prediction history CRUD & CSV download endpoints
│   │   └── analytics.py     # EDA, metrics & online retraining endpoints
│   ├── services/
│   │   ├── ml_service.py    # Business logic & DB persistence
│   │   └── eda_service.py   # Statistical analysis & Plotly figure builder
│   ├── templates/
│   │   ├── base.html        # Master glassmorphic layout wrapper
│   │   ├── index.html       # Landing page (hero, counters & workflow)
│   │   ├── predict.html     # Single prediction form & CSV batch upload
│   │   ├── dashboard.html   # Plotly interactive analytics dashboard
│   │   ├── eda.html         # Correlation matrix & data quality report
│   │   ├── models.html      # 6 Model comparison matrix & ROC/PR curves
│   │   └── history.html     # SQLite prediction history table
│   └── static/
│       ├── css/custom.css   # Custom Glassmorphism CSS design system
│       └── js/              # Modular Vanilla JS scripts
├── dataset/diabetes.csv     # Benchmark Pima Indians Diabetes Dataset
├── model/                   # Serialized best model & metrics JSON
├── screenshots/             # Application visual previews
├── requirements.txt         # Production dependencies
├── LICENSE                  # MIT License (Ashwitha Ramesh)
├── CONTRIBUTING.md          # Open-source contribution guide
├── CHANGELOG.md             # Version release notes
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12, Uvicorn, Pydantic, SQLAlchemy, Joblib
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Frontend**: HTML5, Jinja2 Templates, Bootstrap 5, Vanilla JavaScript, Plotly.js
- **Database**: SQLite
- **Styling**: Glassmorphism CSS, Bootstrap Icons

---

## 🚀 Quickstart & Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/PredictiBetes.git
cd PredictiBetes
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Train Models
```bash
python app/train_model.py
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```
Open **`http://127.0.0.1:8000`** in your browser.

---

## 🌐 Cloud Deployment Guide (Render / Railway / Koyeb)

PredictiBetes is pre-configured for cloud platforms:

- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- **Environment Variable**: Set `PORT` (automatically assigned by cloud provider).

---

## 👨‍💻 Developer & Contact

Developed by **Ashwitha Ramesh**

- **GitHub**: [github.com](https://github.com/Ashwitha-Ramesh)
- **LinkedIn**: [linkedin.com](https://www.linkedin.com/in/ashwitha-ramesh-0123ab315/)
- **Email**: [ashwiramesh2005@gmail.com](mailto:ashwiramesh2005@gmail.com)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
