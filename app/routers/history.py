import csv
import io
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PredictionRecord
from app.schemas import PredictionRecordSchema
from app.utils import logger

router = APIRouter(prefix="/api", tags=["Prediction History"])

@router.get("/history", response_model=List[PredictionRecordSchema])
def get_prediction_history(
    search: Optional[str] = Query(None, description="Search term across risk level or result"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(PredictionRecord)
    
    if risk_level:
        query = query.filter(PredictionRecord.risk_level == risk_level)
        
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (PredictionRecord.risk_level.ilike(search_fmt)) |
            (PredictionRecord.bmi_category.ilike(search_fmt)) |
            (PredictionRecord.model_used.ilike(search_fmt))
        )
        
    records = query.order_by(PredictionRecord.created_at.desc()).limit(limit).all()
    return records

@router.delete("/history/{record_id}")
def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prediction record not found.")
        
    db.delete(record)
    db.commit()
    logger.info(f"Deleted prediction record ID {record_id}")
    return {"message": f"Record {record_id} successfully deleted."}

@router.delete("/history")
def clear_all_history(db: Session = Depends(get_db)):
    count = db.query(PredictionRecord).delete()
    db.commit()
    logger.info(f"Cleared all {count} history records.")
    return {"message": f"Cleared {count} prediction records from history."}

@router.get("/history/download")
def download_history_csv(db: Session = Depends(get_db)):
    records = db.query(PredictionRecord).order_by(PredictionRecord.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Timestamp", "Pregnancies", "Glucose", "BloodPressure",
        "SkinThickness", "Insulin", "BMI", "DPF", "Age",
        "Prediction", "Probability", "Confidence%", "RiskLevel", "BMICategory", "ModelUsed"
    ])
    
    for r in records:
        writer.writerow([
            r.id, r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            r.pregnancies, r.glucose, r.blood_pressure,
            r.skin_thickness, r.insulin, r.bmi, r.dpf, r.age,
            "Diabetic" if r.prediction == 1 else "Non-Diabetic",
            r.probability, r.confidence_percent, r.risk_level, r.bmi_category, r.model_used
        ])
        
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=diabetes_prediction_history.csv"}
    )
