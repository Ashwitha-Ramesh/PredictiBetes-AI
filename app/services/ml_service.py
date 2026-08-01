import os
import pandas as pd
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.ml_model import DiabetesMLPipeline, DATASET_PATH
from app.models import PredictionRecord
from app.utils import determine_risk_level, get_bmi_category, generate_health_tips, logger

# Singleton instance of ML pipeline
pipeline_instance = DiabetesMLPipeline()

def ensure_model_loaded():
    if pipeline_instance.best_model is None:
        if not pipeline_instance.load_model():
            logger.info("No saved model found. Training initial models...")
            pipeline_instance.train_and_evaluate()

def predict_and_save(input_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    ensure_model_loaded()
    
    # Run prediction
    res = pipeline_instance.predict_single(input_data)
    
    prediction = res['prediction']
    probability = res['probability']
    confidence_percent = res['confidence_percent']
    model_used = res['model_used']
    
    glucose = float(input_data.get('Glucose', input_data.get('glucose', 0)))
    bmi = float(input_data.get('BMI', input_data.get('bmi', 0)))
    bp = float(input_data.get('BloodPressure', input_data.get('blood_pressure', 0)))
    age = int(input_data.get('Age', input_data.get('age', 0)))
    
    risk_level = determine_risk_level(probability, glucose, bmi)
    bmi_category = get_bmi_category(bmi)
    health_tips = generate_health_tips(glucose, bmi, bp, age, probability)
    
    result_label = "Diabetic" if prediction == 1 else "Non-Diabetic"
    
    # Save record to SQLite database
    db_record = PredictionRecord(
        pregnancies=int(input_data.get('Pregnancies', input_data.get('pregnancies', 0))),
        glucose=glucose,
        blood_pressure=bp,
        skin_thickness=float(input_data.get('SkinThickness', input_data.get('skin_thickness', 0))),
        insulin=float(input_data.get('Insulin', input_data.get('insulin', 0))),
        bmi=bmi,
        dpf=float(input_data.get('DiabetesPedigreeFunction', input_data.get('dpf', 0))),
        age=age,
        prediction=prediction,
        probability=probability,
        confidence_percent=confidence_percent,
        risk_level=risk_level,
        bmi_category=bmi_category,
        model_used=model_used
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    logger.info(f"Saved prediction ID {db_record.id}: Result={result_label}, Prob={probability}")
    
    return {
        "id": db_record.id,
        "prediction": prediction,
        "result_label": result_label,
        "probability": probability,
        "confidence_percent": confidence_percent,
        "risk_level": risk_level,
        "bmi_category": bmi_category,
        "model_used": model_used,
        "health_tips": health_tips,
        "top_positive_factors": res.get('top_positive_factors', []),
        "top_negative_factors": res.get('top_negative_factors', [])
    }

def process_batch_csv(df: pd.DataFrame) -> List[Dict[str, Any]]:
    ensure_model_loaded()
    
    required_cols = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]
    
    # Standardize column names if lowercase
    col_map = {c.lower(): c for c in required_cols}
    col_map['dpf'] = 'DiabetesPedigreeFunction'
    
    df_renamed = df.rename(columns=lambda c: col_map.get(c.lower(), c))
    
    missing_cols = [c for c in required_cols if c not in df_renamed.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing_cols)}")
        
    results = []
    for idx, row in df_renamed.iterrows():
        input_dict = {c: float(row[c]) for c in required_cols}
        res = pipeline_instance.predict_single(input_dict)
        
        glucose = input_dict['Glucose']
        bmi = input_dict['BMI']
        prob = res['probability']
        risk_level = determine_risk_level(prob, glucose, bmi)
        
        results.append({
            "row_index": idx + 1,
            "prediction": res['prediction'],
            "result_label": "Diabetic" if res['prediction'] == 1 else "Non-Diabetic",
            "probability": prob,
            "risk_level": risk_level
        })
        
    return results

def retrain_all_models() -> Dict[str, Any]:
    logger.info("Triggering online model retraining...")
    metrics = pipeline_instance.train_and_evaluate()
    return metrics
