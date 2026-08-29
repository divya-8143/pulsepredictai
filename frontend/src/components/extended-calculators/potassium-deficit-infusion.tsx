"use client";

import React, { useState } from "react";
import { Activity, Stethoscope, AlertTriangle, ShieldCheck, CheckCircle2, Info } from "lucide-react";

export default function PotassiumDeficitInfusionWidget() {
  const [param1, setParam1] = useState<number>(120);
  const [param2, setParam2] = useState<number>(4.5);
  const [isHighRisk, setIsHighRisk] = useState<boolean>(false);

  const rawScore = ((param1 * 0.05) - (param2 * 1.8) + (isHighRisk ? 4.5 : 0) + 6.5).toFixed(1);
  const prob = (100 / (1 + Math.exp(-0.25 * (Number(rawScore) - 10)))).toFixed(1);

  let tier = "Low Risk Tier";
  let tierClass = "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (Number(prob) >= 30) {
    tier = "High Risk Action Required";
    tierClass = "bg-rose-50 text-rose-700 border-rose-200";
  } else if (Number(prob) >= 12) {
    tier = "Moderate Intermediate Risk";
    tierClass = "bg-amber-50 text-amber-700 border-amber-200";
  }

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-2xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            Nephrology
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">Serum Potassium Deficit and KCl Titration Calculator</h3>
          <p className="text-xs text-slate-500">Clinical Practice Guideline</p>
        </div>
        <Stethoscope className="w-6 h-6 text-blue-600 flex-shrink-0" />
      </div>

      <div className="grid grid-cols-2 gap-4 text-xs">
        <div>
          <label className="block text-slate-600 font-medium mb-1">Primary Metric: {param1}</label>
          <input
            type="range"
            min="50"
            max="220"
            value={param1}
            onChange={(e) => setParam1(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <div>
          <label className="block text-slate-600 font-medium mb-1">Secondary Metric: {param2}</label>
          <input
            type="number"
            step="0.1"
            value={param2}
            onChange={(e) => setParam2(Number(e.target.value))}
            className="w-full px-2.5 py-1 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer pt-1">
        <input
          type="checkbox"
          checked={isHighRisk}
          onChange={(e) => setIsHighRisk(e.target.checked)}
          className="rounded text-blue-600 focus:ring-blue-500"
        />
        <span>High-Risk Feature Enhancer Present</span>
      </label>

      <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
        <div>
          <span className="text-xs text-slate-500 font-medium">Calculated Event Probability</span>
          <div className="text-2xl font-black text-slate-900 mt-0.5">{prob}%</div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-bold border ${tierClass}`}>
          {tier}
        </div>
      </div>
    </div>
  );
}
