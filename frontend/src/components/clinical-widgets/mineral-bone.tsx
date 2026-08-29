"use client";

import React, { useState, useMemo } from "react";
import { Activity, Heart, Shield, AlertCircle, TrendingUp, Sparkles, Check } from "lucide-react";

export default function MineralBoneWidget() {
  const [baseline, setBaseline] = useState<number>(45);
  const [biomarker, setBiomarker] = useState<number>(2.4);
  const [accelerated, setAccelerated] = useState<boolean>(false);

  const analysis = useMemo(() => {
    let raw = baseline * 0.4 + biomarker * 15;
    if (accelerated) raw *= 1.35;
    const score = Math.min(100, Math.max(0, 100 / (1 + Math.exp(-0.05 * (raw - 50)))));
    
    let tier = "Normal Baseline";
    let badgeClass = "bg-emerald-50 text-emerald-700 border-emerald-200";
    if (score >= 75) {
      tier = "Severe Pathology";
      badgeClass = "bg-rose-50 text-rose-700 border-rose-200";
    } else if (score >= 50) {
      tier = "Moderate Strain";
      badgeClass = "bg-amber-50 text-amber-700 border-amber-200";
    } else if (score >= 25) {
      tier = "Mild Alteration";
      badgeClass = "bg-blue-50 text-blue-700 border-blue-200";
    }

    return {
      score: score.toFixed(1),
      tier,
      badgeClass,
      fiveYear: (score * (accelerated ? 1.25 : 1.1)).toFixed(1)
    };
  }, [baseline, biomarker, accelerated]);

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-2xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            Nephrology
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">Chronic Kidney Disease-Mineral and Bone Disorder (CKD-MBD)</h3>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-bold border ${analysis.badgeClass}`}>
          {analysis.tier}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Baseline Index: {baseline}</label>
          <input
            type="range"
            min="10"
            max="100"
            value={baseline}
            onChange={(e) => setBaseline(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Biomarker Level: {biomarker}</label>
          <input
            type="number"
            step="0.1"
            value={biomarker}
            onChange={(e) => setBiomarker(Number(e.target.value))}
            className="w-full px-2.5 py-1 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer pt-2">
        <input
          type="checkbox"
          checked={accelerated}
          onChange={(e) => setAccelerated(e.target.checked)}
          className="rounded text-blue-600 focus:ring-blue-500"
        />
        <span>Accelerated Disease Progression Modifier</span>
      </label>

      <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-center justify-between">
        <div>
          <span className="text-xs text-slate-500 font-medium">Computed Subsystem Score</span>
          <div className="text-2xl font-black text-slate-900">{analysis.score} / 100</div>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-500 font-medium">5-Year Projection</span>
          <div className="text-sm font-bold text-slate-800 flex items-center gap-1 justify-end">
            <TrendingUp className="w-4 h-4 text-blue-600" />
            {analysis.fiveYear}
          </div>
        </div>
      </div>
    </div>
  );
}
