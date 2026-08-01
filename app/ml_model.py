import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

FEATURE_COLUMNS = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]
TARGET_COLUMN = 'Outcome'

ZERO_INVALID_COLS = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.pkl')
METRICS_PATH = os.path.join(MODEL_DIR, 'metrics.json')
DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset', 'diabetes.csv'))

class DiabetesMLPipeline:
    def __init__(self, data_path: str = DATASET_PATH):
        self.data_path = data_path
        self.scaler = None
        self.best_model = None
        self.best_model_name = None
        self.feature_medians = {}
        self.metrics_history = {}

    def load_and_preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Loads data, imputes zero values with feature medians, scales features."""
        df = pd.read_csv(self.data_path)
        
        # Calculate medians for zero-imputation
        for col in ZERO_INVALID_COLS:
            non_zero_median = df[df[col] > 0][col].median()
            if pd.isna(non_zero_median):
                non_zero_median = df[col].median()
            self.feature_medians[col] = float(non_zero_median)
            df[col] = df[col].replace(0, self.feature_medians[col])

        X = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        X_train_df = pd.DataFrame(X_train_scaled, columns=FEATURE_COLUMNS)
        X_test_df = pd.DataFrame(X_test_scaled, columns=FEATURE_COLUMNS)

        return X_train_df, X_test_df, y_train, y_test

    def get_classifiers(self) -> Dict[str, Any]:
        return {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
            'Support Vector Machine': SVC(probability=True, random_state=42),
            'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
            'Gaussian Naive Bayes': GaussianNB()
        }

    def train_and_evaluate(self) -> Dict[str, Any]:
        """Trains all 6 classifiers, evaluates performance metrics, and saves the best model."""
        os.makedirs(MODEL_DIR, exist_ok=True)
        X_train, X_test, y_train, y_test = self.load_and_preprocess()

        classifiers = self.get_classifiers()
        results = {}
        best_score = -1.0
        best_clf = None
        best_name = ""

        for name, clf in classifiers.items():
            # Training time
            start_train = time.time()
            clf.fit(X_train, y_train)
            train_time = round((time.time() - start_train) * 1000, 2) # in ms

            # Inference time
            start_inf = time.time()
            y_pred = clf.predict(X_test)
            inf_time = round((time.time() - start_inf) * 1000, 2)

            y_proba = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else [0.5]*len(y_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y_test, y_proba)

            cm = confusion_matrix(y_test, y_pred).tolist()
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            precision_pts, recall_pts, _ = precision_recall_curve(y_test, y_proba)

            # Feature importance if available
            feature_importance = []
            if hasattr(clf, 'feature_importances_'):
                feature_importance = clf.feature_importances_.tolist()
            elif hasattr(clf, 'coef_'):
                feature_importance = np.abs(clf.coef_[0]).tolist()
            else:
                feature_importance = [1.0 / len(FEATURE_COLUMNS)] * len(FEATURE_COLUMNS)

            results[name] = {
                'accuracy': round(float(acc), 4),
                'precision': round(float(prec), 4),
                'recall': round(float(rec), 4),
                'f1_score': round(float(f1), 4),
                'roc_auc': round(float(roc_auc), 4),
                'train_time_ms': train_time,
                'inference_time_ms': inf_time,
                'confusion_matrix': cm,
                'roc_curve': {
                    'fpr': [round(x, 4) for x in fpr.tolist()],
                    'tpr': [round(x, 4) for x in tpr.tolist()]
                },
                'pr_curve': {
                    'precision': [round(x, 4) for x in precision_pts.tolist()],
                    'recall': [round(x, 4) for x in recall_pts.tolist()]
                },
                'feature_importance': dict(zip(FEATURE_COLUMNS, [round(x, 4) for x in feature_importance]))
            }

            # Best model selection based on ROC-AUC + F1 score
            score = (roc_auc * 0.6) + (f1 * 0.4)
            if score > best_score:
                best_score = score
                best_clf = clf
                best_name = name

        self.best_model = best_clf
        self.best_model_name = best_name
        self.metrics_history = results

        # Save artifacts
        model_artifact = {
            'model': self.best_model,
            'scaler': self.scaler,
            'best_model_name': self.best_model_name,
            'feature_medians': self.feature_medians,
            'feature_names': FEATURE_COLUMNS
        }
        joblib.dump(model_artifact, MODEL_PATH)

        summary_metrics = {
            'best_model_name': self.best_model_name,
            'models': results,
            'trained_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(METRICS_PATH, 'w') as f:
            json.dump(summary_metrics, f, indent=2)

        return summary_metrics

    def load_model(self) -> bool:
        """Loads saved best model from disk."""
        if not os.path.exists(MODEL_PATH):
            return False
        artifact = joblib.load(MODEL_PATH)
        self.best_model = artifact['model']
        self.scaler = artifact['scaler']
        self.best_model_name = artifact['best_model_name']
        self.feature_medians = artifact['feature_medians']
        return True

    def predict_single(self, input_data: Dict[str, float]) -> Dict[str, Any]:
        """Preprocesses input dict and returns prediction, probability, and risk indicators."""
        if self.best_model is None or self.scaler is None:
            if not self.load_model():
                self.train_and_evaluate()

        # Format input vector
        row = []
        for col in FEATURE_COLUMNS:
            val = float(input_data.get(col, 0))
            if col in ZERO_INVALID_COLS and val <= 0:
                val = self.feature_medians.get(col, 0)
            row.append(val)

        X_df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
        X_scaled = self.scaler.transform(X_df)

        pred = int(self.best_model.predict(X_scaled)[0])
        if hasattr(self.best_model, 'predict_proba'):
            proba = float(self.best_model.predict_proba(X_scaled)[0][1])
        else:
            proba = 1.0 if pred == 1 else 0.0

        # Feature contribution explainability (scaled value * importance weight)
        feature_contributions = {}
        if hasattr(self.best_model, 'coef_'):
            weights = self.best_model.coef_[0]
            for idx, col in enumerate(FEATURE_COLUMNS):
                feature_contributions[col] = round(float(X_scaled[0][idx] * weights[idx]), 4)
        elif hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            for idx, col in enumerate(FEATURE_COLUMNS):
                val_diff = X_scaled[0][idx]
                feature_contributions[col] = round(float(val_diff * importances[idx]), 4)
        else:
            for idx, col in enumerate(FEATURE_COLUMNS):
                feature_contributions[col] = round(float(X_scaled[0][idx]), 4)

        # Sort top positive risk factors and protective factors
        top_positive_factors = [
            {"feature": k, "score": v} for k, v in sorted(feature_contributions.items(), key=lambda item: item[1], reverse=True) if v > 0
        ]
        top_negative_factors = [
            {"feature": k, "score": v} for k, v in sorted(feature_contributions.items(), key=lambda item: item[1]) if v <= 0
        ]

        return {
            'prediction': pred,
            'probability': round(proba, 4),
            'confidence_percent': round(proba * 100 if pred == 1 else (1 - proba) * 100, 2),
            'model_used': self.best_model_name,
            'feature_contributions': feature_contributions,
            'top_positive_factors': top_positive_factors,
            'top_negative_factors': top_negative_factors
        }
