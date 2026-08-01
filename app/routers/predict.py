import io
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DiabetesInput, PredictionResponse
from app.services.ml_service import predict_and_save, process_batch_csv
from app.utils import logger

router = APIRouter(prefix="/api", tags=["Prediction"])

@router.post("/predict", response_model=PredictionResponse)
def predict_diabetes(data: DiabetesInput, db: Session = Depends(get_db)):
    """Accepts clinical inputs, computes ML diabetes prediction, and stores history."""
    try:
        input_dict = data.model_dump()
        result = predict_and_save(input_dict, db)
        return result
    except Exception as e:
        logger.error(f"Prediction Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction service failed: {str(e)}")

@router.post("/predict/batch")
async def batch_predict_csv(file: UploadFile = File(...)):
    """Upload CSV file containing feature columns to run batch predictions."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")
            
        results = process_batch_csv(df)
        return {
            "total_rows": len(results),
            "diabetic_count": sum(1 for r in results if r['prediction'] == 1),
            "non_diabetic_count": sum(1 for r in results if r['prediction'] == 0),
            "results": results
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process CSV file: {str(e)}")
