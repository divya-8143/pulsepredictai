import React from "react";
import { RiskCategory } from "@/types";
import { AlertTriangle, CheckCircle2, Flame, HeartPulse } from "lucide-react";

interface RiskScoreCardProps {
  score: number;
  category: RiskCategory;
  primaryModel: string;
  recommendations: string[];
}

export const RiskScoreCard: React.FC<RiskScoreCardProps> = ({
  score,
  category,
  primaryModel,
  recommendations
}) => {
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
  );
};
