"use client";

import React, { useState } from "react";
import { Eye, Activity, ShieldCheck, FileText } from "lucide-react";

export default function CtFractionalFlowReserveView() {
  const [val, setVal] = useState<number>(45);
  const [bsa, setBsa] = useState<number>(1.95);

  const indexed = (val / Math.max(1, bsa)).toFixed(2);
  let grade = "Normal Baseline";
  let gradeColor = "bg-emerald-50 text-emerald-700 border-emerald-200";
  if (Number(indexed) >= 40) {
    grade = "Severe Remodeling";
    gradeColor = "bg-rose-50 text-rose-700 border-rose-200";
  } else if (Number(indexed) >= 32) {
    grade = "Moderate Alteration";
    gradeColor = "bg-amber-50 text-amber-700 border-amber-200";
  } else if (Number(indexed) >= 28) {
    grade = "Mild Alteration";
    gradeColor = "bg-blue-50 text-blue-700 border-blue-200";
  }

  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-2xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
            Radiology
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">CT-Derived Fractional Flow Reserve (FFR-CT) Hemodynamic Lesion</h3>
        </div>
        <Eye className="w-6 h-6 text-indigo-600" />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Measured Parameter: {val} mm</label>
          <input
            type="range"
            min="10"
            max="80"
            value={val}
            onChange={(e) => setVal(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Body Surface Area (BSA): {bsa} m²</label>
          <input
            type="number"
            step="0.05"
            value={bsa}
            onChange={(e) => setBsa(Number(e.target.value))}
            className="w-full px-2.5 py-1 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
        <div>
          <span className="text-xs text-slate-500 font-medium">Indexed Value (BSA-Normalized)</span>
          <div className="text-2xl font-black text-slate-900 mt-0.5">{indexed}</div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-bold border ${gradeColor}`}>
          {grade}
        </div>
      </div>
    </div>
  );
}
