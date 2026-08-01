from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base

class PredictionRecord(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Input Clinical Features
    pregnancies = Column(Integer, nullable=False)
    glucose = Column(Float, nullable=False)
    blood_pressure = Column(Float, nullable=False)
    skin_thickness = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    dpf = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    
    # Output Predictions
    prediction = Column(Integer, nullable=False) # 0 or 1
    probability = Column(Float, nullable=False)
    confidence_percent = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False) # Low, Moderate, High, Very High
    bmi_category = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
