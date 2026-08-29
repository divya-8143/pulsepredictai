import React, { useState } from "react";
import { RiskCategory } from "@/types";
import { AlertTriangle, CheckCircle2, Flame, HeartPulse, Download, Utensils, Loader2 } from "lucide-react";
import { apiClient } from "@/lib/api";
import PersonalizedDietPlan from "@/components/PersonalizedDietPlan";

interface RiskScoreCardProps {
  score: number;
  category: RiskCategory;
  primaryModel: string;
  recommendations: string[];
  assessmentId?: string;
}

export const RiskScoreCard: React.FC<RiskScoreCardProps> = ({
  score,
  category,
  primaryModel,
  recommendations,
  assessmentId
}) => {
  const [downloading, setDownloading] = useState(false);
  const [showDietPlan, setShowDietPlan] = useState(false);
  const [dietPlanData, setDietPlanData] = useState<any>(null);
  const [loadingDiet, setLoadingDiet] = useState(false);

  const handleDownloadPdf = async () => {
    if (!assessmentId) {
      alert("Assessment ID unavailable for download.");
      return;
    }
    setDownloading(true);
    try {
      const response = await apiClient.get(`/assessments/${assessmentId}/report`, {
        responseType: "blob"
      });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `PulsePredict_Assessment_${assessmentId.slice(0, 8)}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to download PDF report", err);
      alert("Failed to download clinical PDF report. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  const handleFetchDietPlan = async () => {
    if (!assessmentId) return;
    setShowDietPlan(!showDietPlan);
    if (!dietPlanData) {
      setLoadingDiet(true);
      try {
        const res = await apiClient.get(`/assessments/${assessmentId}/diet-plan`);
        setDietPlanData(res.data);
      } catch (err) {
        console.error("Failed to load diet plan", err);
      } finally {
        setLoadingDiet(false);
      }
    }
  };

  const getCategoryStyles = (cat: RiskCategory) => {
    switch (cat) {
      case "LOW":
        return {
          bg: "bg-emerald-50 border-emerald-200 text-emerald-800",
          badge: "bg-emerald-500 text-white",
          icon: <CheckCircle2 className="w-6 h-6 text-emerald-600" />,
          label: "Low Risk (Optimal Baseline)"
        };
      case "MODERATE":
        return {
          bg: "bg-amber-50 border-amber-200 text-amber-800",
          badge: "bg-amber-500 text-white",
          icon: <AlertTriangle className="w-6 h-6 text-amber-600" />,
          label: "Moderate Risk (Preventive Alert)"
        };
      case "HIGH":
        return {
          bg: "bg-orange-50 border-orange-200 text-orange-800",
          badge: "bg-orange-500 text-white",
          icon: <Flame className="w-6 h-6 text-orange-600" />,
          label: "High Risk (Clinical Follow-Up)"
        };
      case "CRITICAL":
        return {
          bg: "bg-rose-50 border-rose-200 text-rose-800",
          badge: "bg-rose-600 text-white",
          icon: <HeartPulse className="w-6 h-6 text-rose-600" />,
          label: "Critical Risk (Urgent Care Trigger)"
        };
    }
  };

  const styles = getCategoryStyles(category);

  return (
    <div className="space-y-6">
      <div className={`p-6 rounded-2xl border ${styles.bg} shadow-sm space-y-6 transition-all`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {styles.icon}
            <div>
              <h3 className="font-bold text-lg tracking-tight">AI Health Risk Assessment</h3>
              <p className="text-xs text-slate-500">Evaluated via {primaryModel}</p>
            </div>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${styles.badge}`}>
            {category}
          </span>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-6 py-2">
          <div className="relative flex items-center justify-center">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="52"
                stroke="currentColor"
                strokeWidth="10"
                className="text-slate-200"
                fill="transparent"
              />
              <circle
                cx="64"
                cy="64"
                r="52"
                stroke="currentColor"
                strokeWidth="10"
                className={
                  category === "LOW" ? "text-emerald-500" :
                  category === "MODERATE" ? "text-amber-500" :
                  category === "HIGH" ? "text-orange-500" : "text-rose-600"
                }
                fill="transparent"
                strokeDasharray={326.7}
                strokeDashoffset={326.7 - (326.7 * score) / 100}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute text-center">
              <span className="text-3xl font-extrabold tracking-tight text-slate-900">{score}</span>
              <span className="block text-[10px] font-semibold text-slate-400 uppercase">/ 100</span>
            </div>
          </div>

          <div className="flex-1 space-y-2">
            <h4 className="font-semibold text-sm text-slate-900">{styles.label}</h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              Composite health score synthesized from blood pressure, metabolic biomarkers, lipid fractionations, BMI, and genetic predisposition factors.
            </p>
            
            {/* Patient Action Buttons */}
            {assessmentId && (
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <button
                  onClick={handleDownloadPdf}
                  disabled={downloading}
                  className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm flex items-center gap-1.5 transition disabled:opacity-50"
                >
                  {downloading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                  Download Clinical PDF Report
                </button>

                <button
                  onClick={handleFetchDietPlan}
                  className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-sm flex items-center gap-1.5 transition"
                >
                  <Utensils className="w-4 h-4" />
                  {showDietPlan ? "Hide Diet Plan" : "View Personalized Balanced Diet"}
                </button>
              </div>
            )}
          </div>
        </div>

        {recommendations.length > 0 && (
          <div className="bg-white/80 backdrop-blur rounded-xl p-4 border border-slate-200/80 space-y-2">
            <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Clinical Action Guidance</h5>
            <ul className="space-y-1.5 text-xs text-slate-600">
              {recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Render Diet Plan if opened */}
      {showDietPlan && (
        <div className="transition-all animate-fadeIn">
          {loadingDiet ? (
            <div className="p-8 bg-white rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
              <Loader2 className="w-6 h-6 animate-spin mx-auto text-emerald-600 mb-2" />
              Generating personalized balanced diet blueprint...
            </div>
          ) : (
            <PersonalizedDietPlan plan={dietPlanData} assessmentId={assessmentId} />
          )}
        </div>
      )}
    </div>
  );
};
