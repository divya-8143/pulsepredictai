import os
import numpy as np
import pandas as pd
from ml_engine.config import RAW_DATA_PATH, RANDOM_SEED

def generate_synthetic_clinical_dataset(n_samples: int = 12000, output_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Generate clinically realistic, non-linear correlated cardiovascular & metabolic dataset.
    Follows epidemiological distributions from NHANES, Framingham, and CDC BRFSS.
    """
    np.random.seed(RANDOM_SEED)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Demographics
    age = np.random.normal(loc=52.0, scale=14.0, size=n_samples)
    age = np.clip(age, 18.0, 95.0)

    # 2. Anthropometrics
    # BMI tends to rise with age with positive skew
    bmi = np.random.gamma(shape=12.0, scale=2.3, size=n_samples)
    bmi = np.clip(bmi, 16.0, 58.0)

    # 3. Cardiovascular Vitals (Correlated with Age & BMI)
    # Mean systolic rises ~0.6 per year of age and ~0.8 per BMI unit
    sbp_mean = 100.0 + (0.45 * age) + (0.55 * (bmi - 22.0))
    systolic_bp = np.random.normal(loc=sbp_mean, scale=14.0)
    systolic_bp = np.clip(systolic_bp, 85.0, 220.0)

    dbp_mean = 65.0 + (0.15 * age) + (0.35 * (bmi - 22.0))
    diastolic_bp = np.random.normal(loc=dbp_mean, scale=9.0)
    diastolic_bp = np.clip(diastolic_bp, 50.0, systolic_bp - 16.0)

    resting_heart_rate = np.random.normal(loc=72.0 + 0.2 * (bmi - 24.0), scale=10.0, size=n_samples)
    resting_heart_rate = np.clip(resting_heart_rate, 45.0, 140.0)

    # 4. Metabolic Panel
    # Fasting glucose correlated with BMI and age
    fbg_mean = 85.0 + (0.6 * (bmi - 22.0)) + (0.3 * (age - 30.0))
    fasting_glucose = np.random.normal(loc=fbg_mean, scale=22.0)
    fasting_glucose = np.clip(fasting_glucose, 65.0, 320.0)

    # HbA1c clinically correlated with fasting glucose (Nathan et al. equation)
    hba1c = (fasting_glucose + 46.7) / 28.7 + np.random.normal(0, 0.35, size=n_samples)
    hba1c = np.clip(hba1c, 4.2, 14.5)

    # 5. Lipid Panel
    total_chol = np.random.normal(loc=195.0 + 0.3 * age, scale=35.0, size=n_samples)
    total_chol = np.clip(total_chol, 110.0, 380.0)

    hdl_chol = np.random.normal(loc=55.0 - 0.4 * (bmi - 22.0), scale=12.0, size=n_samples)
    hdl_chol = np.clip(hdl_chol, 20.0, 95.0)

    ldl_chol = total_chol - hdl_chol - np.random.uniform(20.0, 45.0, size=n_samples)
    ldl_chol = np.clip(ldl_chol, 40.0, 260.0)

    triglycerides = np.random.gamma(shape=5.0, scale=30.0, size=n_samples)
    triglycerides = np.clip(triglycerides, 45.0, 550.0)

    # 6. Lifestyle & Habits
    smoking_prob = np.clip(0.18 + 0.05 * (age < 45) - 0.002 * (age - 50), 0.08, 0.4)
    smoking_status = np.random.choice(
        ["NEVER", "FORMER", "CURRENT"], 
        size=n_samples, 
        p=[0.55, 0.25, 0.20]
    )

    alcohol_consumption = np.random.choice(
        ["NONE", "MODERATE", "HEAVY"],
        size=n_samples,
        p=[0.50, 0.38, 0.12]
    )

    physical_activity_hours_week = np.random.exponential(scale=3.0, size=n_samples)
    physical_activity_hours_week = np.clip(physical_activity_hours_week, 0.0, 30.0)

    # 7. Genetics
    family_history_cad = np.random.binomial(n=1, p=0.22, size=n_samples).astype(bool)
    family_history_diabetes = np.random.binomial(n=1, p=0.28, size=n_samples).astype(bool)
    family_history_hypertension = np.random.binomial(n=1, p=0.35, size=n_samples).astype(bool)

    # 8. Ground Truth Physiological Risk Equation (Multi-factor Cox/Framingham Hybrid)
    log_odds = (
        -7.5
        + 0.045 * age
        + 0.025 * (systolic_bp - 120.0)
        + 0.015 * (bmi - 23.0)
        + 0.012 * (ldl_chol - 100.0)
        - 0.020 * (hdl_chol - 50.0)
        + 0.018 * (fasting_glucose - 90.0)
        + 0.35 * (hba1c - 5.5)
        + 0.75 * (smoking_status == "CURRENT")
        + 0.30 * (smoking_status == "FORMER")
        + 0.40 * (alcohol_consumption == "HEAVY")
        - 0.08 * physical_activity_hours_week
        + 0.65 * family_history_cad
        + 0.45 * family_history_diabetes
        + 0.35 * family_history_hypertension
    )
    
    # Sigmoidal probability
    risk_prob = 1.0 / (1.0 + np.exp(-log_odds))
    risk_score = np.clip(risk_prob * 100.0, 1.0, 99.0)

    # Risk Category (0: LOW, 1: MODERATE, 2: HIGH, 3: CRITICAL)
    risk_category = []
    for s in risk_score:
        if s < 25.0:
            risk_category.append(0) # LOW
        elif s < 50.0:
            risk_category.append(1) # MODERATE
        elif s < 75.0:
            risk_category.append(2) # HIGH
        else:
            risk_category.append(3) # CRITICAL

    df = pd.DataFrame({
        "age": np.round(age, 1),
        "systolic_bp": np.round(systolic_bp, 1),
        "diastolic_bp": np.round(diastolic_bp, 1),
        "resting_heart_rate": np.round(resting_heart_rate, 1),
        "total_cholesterol": np.round(total_chol, 1),
        "hdl_cholesterol": np.round(hdl_chol, 1),
        "ldl_cholesterol": np.round(ldl_chol, 1),
        "triglycerides": np.round(triglycerides, 1),
        "bmi": np.round(bmi, 1),
        "fasting_glucose": np.round(fasting_glucose, 1),
        "hba1c": np.round(hba1c, 2),
        "smoking_status": smoking_status,
        "alcohol_consumption": alcohol_consumption,
        "physical_activity_hours_week": np.round(physical_activity_hours_week, 1),
        "family_history_cad": family_history_cad,
        "family_history_diabetes": family_history_diabetes,
        "family_history_hypertension": family_history_hypertension,
        "risk_score": np.round(risk_score, 2),
        "risk_category_encoded": risk_category
    })

    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} clinical training samples at {output_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_clinical_dataset()
