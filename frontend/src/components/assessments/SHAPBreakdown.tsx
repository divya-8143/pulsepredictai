import React from "react";
import { SHAPContribution } from "@/types";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface SHAPBreakdownProps {
  contributions: SHAPContribution[];
}

export const SHAPBreakdown: React.FC<SHAPBreakdownProps> = ({ contributions }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
      <div>
        <h3 className="font-bold text-base text-slate-900">Explainable AI (SHAP Feature Attribution)</h3>
        <p className="text-xs text-slate-500">
          Shows how each individual biomarker pushed your predicted risk score higher or lower relative to population baselines.
        </p>
      </div>

      <div className="divide-y divide-slate-100">
        {contributions.slice(0, 8).map((item, idx) => (
          <div key={idx} className="py-3 flex items-center justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-xs text-slate-900 truncate">{item.display_name}</span>
                <span className="text-[11px] text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded font-mono">
                  {String(item.feature_value)}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-0.5 truncate">{item.clinical_note}</p>
            </div>

            <div className="flex items-center gap-2">
              <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded-full ${
                item.impact === "INCREASES_RISK" ? "bg-rose-50 text-rose-700" :
                item.impact === "DECREASES_RISK" ? "bg-emerald-50 text-emerald-700" :
                "bg-slate-50 text-slate-600"
              }`}>
                {item.impact === "INCREASES_RISK" && <TrendingUp className="w-3 h-3 text-rose-600" />}
                {item.impact === "DECREASES_RISK" && <TrendingDown className="w-3 h-3 text-emerald-600" />}
                {item.impact === "NEUTRAL" && <Minus className="w-3 h-3 text-slate-400" />}
                {item.shap_value > 0 ? `+${item.shap_value.toFixed(3)}` : item.shap_value.toFixed(3)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
