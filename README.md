# 🩺 PredictiBetes — AI-Powered Diabetes Prediction & Clinical Analytics Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green?style=for-the-badge&logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blueviolet?style=for-the-badge&logo=plotly)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)

</p>

<p align="center">

🚀 **Live Demo:** https://your-render-url.onrender.com

⭐ **GitHub Repository:** https://github.com/Ashwitha-Ramesh/PredictiBetes-AI

</p>

---

# 📌 Overview

PredictiBetes is a recruiter-ready end-to-end Machine Learning web application that predicts diabetes risk using multiple supervised learning algorithms while providing clinical analytics, explainable AI insights, interactive dashboards, and prediction history management.

Unlike traditional ML notebooks, PredictiBetes demonstrates the complete production workflow—from data preprocessing and model training to deployment with FastAPI and cloud hosting.

---

# 🌟 Features

## 🧠 Machine Learning

- Logistic Regression
- Random Forest
- Decision Tree
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Gaussian Naive Bayes

---

## 📊 Interactive Analytics

- Interactive Plotly Dashboard
- Correlation Heatmaps
- Feature Distributions
- Boxplots
- Scatter Plots
- Clinical Statistics
- Dataset Exploration

---

## 🤖 Explainable AI (XAI)

Each prediction includes

- Risk Probability
- Confidence Score
- Top Positive Risk Factors
- Protective Factors
- Clinical Interpretation
- Personalized Health Recommendations

---

## 👨‍⚕️ Prediction System

✔ Single Patient Prediction

✔ Batch CSV Prediction

✔ Real-time Risk Classification

✔ Confidence Estimation

✔ Feature Scaling

✔ Missing Value Handling

---

## 🗄 Prediction History

- SQLite Database
- Search Predictions
- Filter Records
- Delete Records
- CSV Export

---

## 🎨 Modern UI

- Glassmorphism Design
- Bootstrap 5
- Responsive Layout
- Interactive Charts
- Dark Theme
- Animated Dashboard

---

## ☁ Deployment

Successfully deployed on

**Render**

Production Ready

No Docker Required

---

# 📷 Application Preview

# 📷 Application Preview

### 🏠 Home Page

<img width="1353" alt="Home Page" src="https://github.com/user-attachments/assets/a9690cb1-8465-4617-a960-508af8bb4a9d" />

---

### 🩺 Diabetes Prediction

<img width="1346" alt="Prediction Page" src="https://github.com/user-attachments/assets/dba5cd7f-b8be-469b-9bb0-6c41116dd991" />

---

### 📊 Interactive Dashboard

<img width="1352" alt="Dashboard" src="https://github.com/user-attachments/assets/c14dd499-a380-428e-bf5c-2aff490eceb7" />

---

### 📈 Exploratory Data Analysis (EDA)

<img width="1340" alt="EDA" src="https://github.com/user-attachments/assets/a1f375bf-8776-4e2e-bdaa-fa45801fbbd4" />

---

### 🤖 Machine Learning Model Comparison

<img width="1347" alt="Models Comparison" src="https://github.com/user-attachments/assets/dc1b83a4-ea27-4841-97ca-aa88e338dbd4" />

---

### 🗂 Prediction History

<img width="1350" alt="Prediction History" src="https://github.com/user-attachments/assets/dd3e5a62-b55f-4645-827a-9b4485a74bc9" />
```

---

# 🏗 Project Architecture

```
PredictiBetes-AI
│
├── app
│   ├── routers
│   │     ├── predict.py
│   │     ├── analytics.py
│   │     └── history.py
│   │
│   ├── services
│   │     ├── ml_service.py
│   │     └── eda_service.py
│   │
│   ├── static
│   │     ├── css
│   │     ├── js
│   │     └── images
│   │
│   ├── templates
│   │     ├── base.html
│   │     ├── index.html
│   │     ├── predict.html
│   │     ├── dashboard.html
│   │     ├── eda.html
│   │     ├── models.html
│   │     └── history.html
│   │
│   ├── database.py
│   ├── main.py
│   ├── ml_model.py
│   ├── models.py
│   ├── schemas.py
│   ├── train_model.py
│   └── utils.py
│
├── dataset
│     └── diabetes.csv
│
├── model
│     ├── best_model.pkl
│     └── metrics.json
│
├── notebooks
│
├── screenshots
│
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

---

# ⚙ Technology Stack

### Backend

- FastAPI
- Python
- SQLAlchemy
- Uvicorn
- Pydantic

---

### Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- Joblib

---

### Frontend

- HTML5
- Jinja2
- Bootstrap 5
- Vanilla JavaScript
- Plotly.js

---

### Database

SQLite

---

# 🚀 Local Installation

## Clone Repository

```bash
git clone https://github.com/Ashwitha-Ramesh/PredictiBetes-AI.git

cd PredictiBetes-AI
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Train Models

```bash
python app/train_model.py
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

# 🌐 Live Deployment

### Live Website

```
https://predictibetes-ai.onrender.com/
```

Hosted using

- Render
- FastAPI
- Uvicorn
- SQLite

---

# 📈 Machine Learning Workflow

```
Dataset

↓

Data Cleaning

↓

Feature Engineering

↓

Train/Test Split

↓

Model Training

↓

Model Evaluation

↓

Best Model Selection

↓

FastAPI Backend

↓

Interactive Dashboard

↓

Cloud Deployment
```

---

# 📊 Model Comparison

| Algorithm | Evaluated |
|------------|-----------|
| Logistic Regression | ✅ |
| Random Forest | ✅ |
| Decision Tree | ✅ |
| Support Vector Machine | ✅ |
| KNN | ✅ |
| Gaussian Naive Bayes | ✅ |

---

# 🔮 Future Improvements

- User Authentication
- Doctor Dashboard
- PDF Clinical Report
- REST API Versioning
- Docker Support
- PostgreSQL Integration
- SHAP Explainability
- Deep Learning Models
- CI/CD using GitHub Actions

---

# 👨‍💻 Developer

## Ashwitha Ramesh

Computer Science Engineering Student

AI • Machine Learning • Data Analytics • Open Source

---

### Connect with me

📧 Email

```
ashwiramesh2005@gmail.com
```

💼 LinkedIn

```
https://www.linkedin.com/in/ashwitha-ramesh-0123ab315/
```

🐙 GitHub

```
https://github.com/Ashwitha-Ramesh
```

---

# ⭐ Support

If you found this project useful,

⭐ Star the repository

🍴 Fork the repository

📢 Share it with others

---

# 📜 License

Licensed under the MIT License.

---

> **Disclaimer:** PredictiBetes is an educational Machine Learning project intended for demonstration, research, and portfolio purposes. It is **not** a substitute for professional medical diagnosis or treatment.
