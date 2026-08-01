import logging
import os
from typing import Dict, Any, List

# Logger configuration
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.log"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DiabetesMLApp")

def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    elif 30.0 <= bmi < 35.0:
        return "Class I Obesity"
    elif 35.0 <= bmi < 40.0:
        return "Class II Obesity"
    else:
        return "Class III Severe Obesity"

def determine_risk_level(probability: float, glucose: float, bmi: float) -> str:
    """Combines ML probability score with clinical risk factors."""
    if probability >= 0.70 or glucose >= 180:
        return "Very High"
    elif probability >= 0.45 or glucose >= 140 or bmi >= 35:
        return "High"
    elif probability >= 0.25 or glucose >= 115 or bmi >= 27:
        return "Moderate"
    else:
        return "Low"

def generate_health_tips(glucose: float, bmi: float, bp: float, age: int, probability: float) -> Dict[str, List[str]]:
    diet_tips = []
    exercise_tips = []
    monitoring_tips = []
    general_tips = []

    # Diet tips
    if glucose >= 140:
        diet_tips.append("Reduce refined carbohydrate and simple sugar intake significantly.")
        diet_tips.append("Focus on low glycemic index (GI) whole foods like legumes, oats, and green leafy vegetables.")
    elif glucose >= 100:
        diet_tips.append("Monitor portion sizes of high-carbohydrate meals.")
        diet_tips.append("Incorporate more dietary fiber (aim for 25-30g daily).")
    else:
        diet_tips.append("Maintain a balanced diet rich in vegetables, lean protein, and whole grains.")

    # BMI / Weight tips
    if bmi >= 30:
        diet_tips.append("Consult a registered dietitian to establish a mild caloric deficit.")
        exercise_tips.append("Aim for at least 150 minutes of moderate aerobic exercise (walking, swimming, cycling) per week.")
        exercise_tips.append("Include light resistance training 2-3 times per week to build lean muscle mass.")
    elif bmi >= 25:
        exercise_tips.append("Engage in brisk walking for 30 minutes daily.")
        exercise_tips.append("Limit high-calorie sugary beverages and processed snacks.")

    # BP tips
    if bp >= 80:
        monitoring_tips.append("Monitor blood pressure regularly twice a week.")
        diet_tips.append("Limit daily sodium intake to less than 2,000 mg.")
    else:
        monitoring_tips.append("Include annual cardiovascular and blood pressure checkups.")

    # General / Medical tips
    if probability >= 0.5:
        monitoring_tips.append("Schedule an HbA1c blood test with your healthcare provider.")
        general_tips.append("Consult an endocrinologist or primary physician for a comprehensive clinical assessment.")
    else:
        general_tips.append("Maintain routine annual health checkups and blood screenings.")

    general_tips.append("Ensure 7-8 hours of quality restful sleep each night.")
    general_tips.append("Practice stress reduction techniques like deep breathing, yoga, or meditation.")

    return {
        "diet": diet_tips,
        "exercise": exercise_tips,
        "monitoring": monitoring_tips,
        "general": general_tips
    }
