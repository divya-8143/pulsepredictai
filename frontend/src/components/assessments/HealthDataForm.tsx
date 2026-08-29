import React, { useState } from "react";
import { HealthDataInput, RiskAssessment } from "@/types";
import { apiClient } from "@/lib/api";
import { Activity, Heart, Droplet, User, Flame, ArrowRight, ArrowLeft, CheckCircle2, AlertCircle } from "lucide-react";

interface HealthDataFormProps {
  onSuccess: (assessment: RiskAssessment) => void;
}

export const HealthDataForm: React.FC<HealthDataFormProps> = ({ onSuccess }) => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<HealthDataInput>({
    age: 48,
    systolic_bp: 138,
    diastolic_bp: 88,
    resting_heart_rate: 74,
    total_cholesterol: 215,
    hdl_cholesterol: 45,
    ldl_cholesterol: 135,
    triglycerides: 165,
    bmi: 27.8,
    fasting_glucose: 108,
    hba1c: 5.9,
    smoking_status: "NEVER",
    alcohol_consumption: "MODERATE",
    physical_activity_hours_week: 2.5,
    family_history_cad: false,
    family_history_diabetes: true,
    family_history_hypertension: true,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else if (type === "number") {
      setFormData((prev) => ({ ...prev, [name]: parseFloat(value) || 0 }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await apiClient.post("/assessments/predict", formData);
      onSuccess(res.data);
    } catch (err: any) {
      const msg = err.response?.data?.message || err.response?.data?.extra?.clinical_errors?.join(", ") || "Failed to submit assessment.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
      {/* Step Indicator */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${step === 1 ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-600"}`}>1</span>
          <span className="text-xs font-semibold text-slate-700">Vitals & Vitals</span>
        </div>
        <div className="w-8 h-0.5 bg-slate-200" />
        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${step === 2 ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-600"}`}>2</span>
          <span className="text-xs font-semibold text-slate-700">Lipid & Metabolic</span>
        </div>
        <div className="w-8 h-0.5 bg-slate-200" />
        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${step === 3 ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-600"}`}>3</span>
          <span className="text-xs font-semibold text-slate-700">Lifestyle & Genetics</span>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {step === 1 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700">Patient Age (years)</label>
              <input
                type="number"
                name="age"
                min="18"
                max="105"
                value={formData.age}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Body Mass Index (BMI kg/m²)</label>
              <input
                type="number"
                step="0.1"
                name="bmi"
                min="12"
                max="65"
                value={formData.bmi}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Systolic Blood Pressure (mmHg)</label>
              <input
                type="number"
                name="systolic_bp"
                min="70"
                max="240"
                value={formData.systolic_bp}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Diastolic Blood Pressure (mmHg)</label>
              <input
                type="number"
                name="diastolic_bp"
                min="40"
                max="140"
                value={formData.diastolic_bp}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-xs font-semibold text-slate-700">Resting Heart Rate (bpm)</label>
              <input
                type="number"
                name="resting_heart_rate"
                min="35"
                max="200"
                value={formData.resting_heart_rate}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700">Total Cholesterol (mg/dL)</label>
              <input
                type="number"
                name="total_cholesterol"
                min="90"
                max="450"
                value={formData.total_cholesterol}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">HDL Cholesterol (mg/dL)</label>
              <input
                type="number"
                name="hdl_cholesterol"
                min="15"
                max="120"
                value={formData.hdl_cholesterol}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">LDL Cholesterol (mg/dL)</label>
              <input
                type="number"
                name="ldl_cholesterol"
                min="30"
                max="300"
                value={formData.ldl_cholesterol}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Serum Triglycerides (mg/dL)</label>
              <input
                type="number"
                name="triglycerides"
                min="40"
                max="600"
                value={formData.triglycerides}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Fasting Blood Glucose (mg/dL)</label>
              <input
                type="number"
                name="fasting_glucose"
                min="50"
                max="350"
                value={formData.fasting_glucose}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Glycated Hemoglobin (HbA1c %)</label>
              <input
                type="number"
                step="0.1"
                name="hba1c"
                min="3.5"
                max="16.0"
                value={formData.hba1c}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Tobacco Smoking Habit</label>
                <select
                  name="smoking_status"
                  value={formData.smoking_status}
                  onChange={handleChange}
                  className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                  <option value="NEVER">Never Smoked</option>
                  <option value="FORMER">Former Smoker (Quit)</option>
                  <option value="CURRENT">Current Active Smoker</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Alcohol Intake Frequency</label>
                <select
                  name="alcohol_consumption"
                  value={formData.alcohol_consumption}
                  onChange={handleChange}
                  className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                  <option value="NONE">None / Rarely</option>
                  <option value="MODERATE">Moderate Consumption</option>
                  <option value="HEAVY">Heavy Consumption</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Physical Activity (Hours/Week)</label>
              <input
                type="number"
                step="0.5"
                name="physical_activity_hours_week"
                min="0"
                max="40"
                value={formData.physical_activity_hours_week}
                onChange={handleChange}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div className="pt-2 space-y-2">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">Family Health History</label>
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-xs text-slate-700">
                  <input
                    type="checkbox"
                    name="family_history_cad"
                    checked={formData.family_history_cad}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span>Family History of Premature Coronary Artery Disease (CAD)</span>
                </label>
                <label className="flex items-center gap-2 text-xs text-slate-700">
                  <input
                    type="checkbox"
                    name="family_history_diabetes"
                    checked={formData.family_history_diabetes}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span>Family History of Type 2 Diabetes Mellitus</span>
                </label>
                <label className="flex items-center gap-2 text-xs text-slate-700">
                  <input
                    type="checkbox"
                    name="family_history_hypertension"
                    checked={formData.family_history_hypertension}
                    onChange={handleChange}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span>Family History of Chronic Hypertension</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Buttons */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          {step > 1 ? (
            <button
              type="button"
              onClick={() => setStep((s) => s - 1)}
              className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 transition"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Back
            </button>
          ) : <div />}

          {step < 3 ? (
            <button
              type="button"
              onClick={() => setStep((s) => s + 1)}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition shadow"
            >
              Continue
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-lg text-xs font-bold flex items-center gap-2 transition shadow-md disabled:opacity-50"
            >
              {loading ? "Running Multi-Model Inference..." : "Compute Risk Assessment"}
              <Activity className="w-4 h-4" />
            </button>
          )}
        </div>
      </form>
    </div>
  );
};
