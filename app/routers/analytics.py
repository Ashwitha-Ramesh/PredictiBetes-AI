import os
import json
from fastapi import APIRouter, HTTPException
from app.services.eda_service import get_eda_data, get_plotly_figures
from app.services.ml_service import retrain_all_models
from app.ml_model import METRICS_PATH
from app.utils import logger

router = APIRouter(prefix="/api", tags=["Analytics & EDA"])

@router.get("/eda")
def get_eda_analytics():
    """Returns EDA dataset overview, statistical distributions, and Plotly chart JSON payloads."""
    try:
        data = get_eda_data()
        charts = get_plotly_figures()
        return {
            "stats": data,
            "charts": charts
        }
    except Exception as e:
        logger.error(f"Error fetching EDA analytics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate EDA analytics: {str(e)}")

@router.get("/metrics")
def get_model_comparison_metrics():
    """Returns evaluation metrics, ROC curves, PR curves, and confusion matrices for all 6 models."""
    if not os.path.exists(METRICS_PATH):
        try:
            metrics = retrain_all_models()
            return metrics
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to train models: {str(e)}")
            
    try:
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)
        return metrics
    except Exception as e:
        logger.error(f"Error reading metrics artifact: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load model metrics.")

@router.post("/retrain")
def retrain_models():
    """Triggers complete re-training of all 6 algorithms and selects best model."""
    try:
        metrics = retrain_all_models()
        return {
            "message": "Models successfully retrained!",
            "best_model_name": metrics.get("best_model_name"),
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Retraining error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")
