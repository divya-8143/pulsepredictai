import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
RAW_DATA_PATH = os.path.join(DATASETS_DIR, "raw", "clinical_health_risk_dataset.csv")

RANDOM_SEED = 42

NUMERICAL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "resting_heart_rate",
    "total_cholesterol",
    "hdl_cholesterol",
    "ldl_cholesterol",
    "triglycerides",
    "bmi",
    "fasting_glucose",
    "hba1c",
    "physical_activity_hours_week",
]

CATEGORICAL_FEATURES = [
    "smoking_status",
    "alcohol_consumption",
]

BINARY_FEATURES = [
    "family_history_cad",
    "family_history_diabetes",
    "family_history_hypertension",
]

ALL_INPUT_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES

TARGET_COLUMN = "risk_category_encoded"
TARGET_CONTINUOUS = "risk_score"

FEATURE_DISPLAY_NAMES = {
    "age": "Patient Age",
    "systolic_bp": "Systolic Blood Pressure",
    "diastolic_bp": "Diastolic Blood Pressure",
    "resting_heart_rate": "Resting Heart Rate",
    "total_cholesterol": "Total Serum Cholesterol",
    "hdl_cholesterol": "High-Density Lipoprotein (HDL)",
    "ldl_cholesterol": "Low-Density Lipoprotein (LDL)",
    "triglycerides": "Serum Triglycerides",
    "bmi": "Body Mass Index (BMI)",
    "fasting_glucose": "Fasting Blood Glucose",
    "hba1c": "Glycated Hemoglobin (HbA1c)",
    "physical_activity_hours_week": "Physical Activity (Hours/Week)",
    "smoking_status": "Tobacco Smoking Habit",
    "alcohol_consumption": "Alcohol Intake Frequency",
    "family_history_cad": "Family History of CAD",
    "family_history_diabetes": "Family History of Diabetes",
    "family_history_hypertension": "Family History of Hypertension",
    "pulse_pressure": "Pulse Pressure (SBP - DBP)",
    "cholesterol_ratio": "Cholesterol Ratio (Total / HDL)",
}
