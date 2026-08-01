import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from typing import Dict, Any, List
from app.ml_model import DATASET_PATH, FEATURE_COLUMNS, TARGET_COLUMN

def get_eda_data() -> Dict[str, Any]:
    df = pd.read_csv(DATASET_PATH)
    
    # Dataset Summary Statistics
    summary_stats = df.describe().round(3).to_dict()
    skewness = df.skew().round(3).to_dict()
    kurtosis = df.kurtosis().round(3).to_dict()
    
    zero_counts = {}
    for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
        zero_counts[col] = int((df[col] == 0).sum())
        
    outcome_counts = df['Outcome'].value_counts().to_dict()
    total_records = len(df)
    diabetic_count = int(outcome_counts.get(1, 0))
    non_diabetic_count = int(outcome_counts.get(0, 0))
    
    # Correlation Matrix
    corr_matrix = df.corr().round(3)
    
    # Extract top positive & negative correlations with Outcome
    outcome_corr = corr_matrix['Outcome'].drop('Outcome').sort_values(ascending=False)
    top_positive = [{"feature": k, "correlation": float(v)} for k, v in outcome_corr.items() if v > 0]
    top_negative = [{"feature": k, "correlation": float(v)} for k, v in outcome_corr.items() if v < 0]
    
    # Explanations in plain English
    explanations = [
        f"Glucose shows the highest positive correlation ({outcome_corr.get('Glucose', 0):.3f}) with diabetes. Higher blood sugar levels strongly indicate diabetic risk.",
        f"BMI exhibits a significant correlation ({outcome_corr.get('BMI', 0):.3f}) with Outcome, reinforcing obesity as a key contributor.",
        f"Age is positively associated ({outcome_corr.get('Age', 0):.3f}) with diabetes risk, as metabolic function changes over time.",
        f"Insulin and SkinThickness contain missing values (represented as 0s in standard clinical raw data) which require median imputation for optimal ML performance."
    ]
    
    return {
        "total_records": total_records,
        "diabetic_count": diabetic_count,
        "non_diabetic_count": non_diabetic_count,
        "diabetic_percent": round((diabetic_count / total_records) * 100, 2),
        "zero_counts": zero_counts,
        "summary_stats": summary_stats,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "correlation_matrix": corr_matrix.to_dict(),
        "top_positive": top_positive,
        "top_negative": top_negative,
        "explanations": explanations
    }

def get_plotly_figures() -> Dict[str, str]:
    """Generates Plotly interactive chart JSON objects for frontend rendering."""
    df = pd.read_csv(DATASET_PATH)
    
    # 1. Outcome Donut Chart
    fig_outcome = px.pie(
        df, 
        names=df['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'}),
        title='Class Distribution (Outcome)',
        hole=0.4,
        color_discrete_sequence=['#10B981', '#EF4444']
    )
    fig_outcome.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter, sans-serif')
    )
    
    # 2. Correlation Heatmap
    corr = df.corr().round(2)
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Feature Correlation Heatmap"
    )
    fig_corr.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter, sans-serif')
    )
    
    # 3. Glucose vs BMI Scatter Plot
    fig_scatter = px.scatter(
        df,
        x='Glucose',
        y='BMI',
        color=df['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'}),
        size='Age',
        hover_data=['Pregnancies', 'Insulin'],
        title='Glucose vs. BMI by Outcome (Size = Age)',
        color_discrete_map={'Non-Diabetic': '#10B981', 'Diabetic': '#EF4444'}
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter, sans-serif')
    )
    
    # 4. Feature Histograms
    fig_hist = px.histogram(
        df,
        x='Glucose',
        color=df['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'}),
        barmode='overlay',
        title='Glucose Concentration Distribution by Class',
        color_discrete_map={'Non-Diabetic': '#10B981', 'Diabetic': '#EF4444'}
    )
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter, sans-serif')
    )

    return {
        "outcome_chart": pio.to_json(fig_outcome),
        "heatmap_chart": pio.to_json(fig_corr),
        "scatter_chart": pio.to_json(fig_scatter),
        "histogram_chart": pio.to_json(fig_hist)
    }
