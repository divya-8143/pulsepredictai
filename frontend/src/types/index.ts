export type UserRole = "PATIENT" | "DOCTOR" | "ADMIN";

export type RiskCategory = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

export type SmokingStatus = "NEVER" | "FORMER" | "CURRENT";

export type AlcoholConsumption = "NONE" | "MODERATE" | "HEAVY";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  patient_profile_id?: string;
  doctor_profile_id?: string;
}

export interface HealthDataInput {
  age: number;
  systolic_bp: number;
  diastolic_bp: number;
  resting_heart_rate: number;
  total_cholesterol: number;
  hdl_cholesterol: number;
  ldl_cholesterol: number;
  triglycerides: number;
  bmi: number;
  fasting_glucose: number;
  hba1c: number;
  smoking_status: SmokingStatus;
  alcohol_consumption: AlcoholConsumption;
  physical_activity_hours_week: number;
  family_history_cad: boolean;
  family_history_diabetes: boolean;
  family_history_hypertension: boolean;
}

export interface SHAPContribution {
  feature_name: string;
  display_name: string;
  feature_value: any;
  shap_value: number;
  impact: "INCREASES_RISK" | "DECREASES_RISK" | "NEUTRAL";
  clinical_note: string;
}

export interface RiskAssessment {
  id: string;
  patient_id: string;
  overall_risk_score: number;
  risk_category: RiskCategory;
  primary_model_name: string;
  ensemble_predictions: Record<string, {
    risk_score: number;
    risk_category: RiskCategory;
    confidence_probability: number;
    weight_in_ensemble: number;
  }>;
  feature_importance_shap: SHAPContribution[];
  clinical_recommendations: string[];
  input_biomarkers: HealthDataInput;
  assessed_at: string;
  disclaimer: string;
}

export interface AssessmentHistoryItem {
  id: string;
  patient_id: string;
  patient_name?: string;
  age: number;
  systolic_bp: number;
  diastolic_bp: number;
  bmi: number;
  fasting_glucose: number;
  total_cholesterol: number;
  overall_risk_score: number;
  risk_category: RiskCategory;
  assessed_at: string;
  has_doctor_review?: boolean;
}

export interface PaginatedHistory {
  items: AssessmentHistoryItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
