from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class DiabetesInput(BaseModel):
    pregnancies: int = Field(..., ge=0, le=20, description="Number of times pregnant")
    glucose: float = Field(..., ge=0, le=300, description="Plasma glucose concentration (mg/dL)")
    blood_pressure: float = Field(..., ge=0, le=200, description="Diastolic blood pressure (mm Hg)")
    skin_thickness: float = Field(..., ge=0, le=100, description="Triceps skin fold thickness (mm)")
    insulin: float = Field(..., ge=0, le=900, description="2-Hour serum insulin (mu U/ml)")
    bmi: float = Field(..., ge=0.0, le=80.0, description="Body Mass Index (weight in kg/(height in m)^2)")
    dpf: float = Field(..., ge=0.0, le=3.0, description="Diabetes Pedigree Function")
    age: int = Field(..., ge=1, le=120, description="Age in years")

    @field_validator('glucose', 'blood_pressure', 'bmi')
    @classmethod
    def validate_clinical_ranges(cls, v, info):
        # Soft warning range check if needed
        return v

class HealthTips(BaseModel):
    diet: List[str]
    exercise: List[str]
    monitoring: List[str]
    general: List[str]

class PredictionResponse(BaseModel):
    prediction: int
    result_label: str
    probability: float
    confidence_percent: float
    risk_level: str
    bmi_category: str
    model_used: str
    health_tips: HealthTips
    top_positive_factors: Optional[List[Dict[str, Any]]] = None
    top_negative_factors: Optional[List[Dict[str, Any]]] = None
    model_config = {"protected_namespaces": ()}

class PredictionRecordSchema(BaseModel):
    id: int
    created_at: datetime
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    dpf: float
    age: int
    prediction: int
    probability: float
    confidence_percent: float
    risk_level: str
    bmi_category: str
    model_used: str

    model_config = {
        "from_attributes": True,
        "protected_namespaces": ()
    }

class ModelMetricsResponse(BaseModel):
    best_model_name: str
    trained_at: str
    models: Dict[str, Any]

class BatchPredictionItem(BaseModel):
    row_index: int
    prediction: int
    result_label: str
    probability: float
    risk_level: str
