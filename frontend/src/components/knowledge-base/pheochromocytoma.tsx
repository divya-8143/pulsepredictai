"use client";

import React, { useState } from "react";
import { BookOpen, ShieldAlert, CheckCircle2, Stethoscope, Tag, ArrowUpRight } from "lucide-react";

export default function PheochromocytomaEncyclopediaView() {
  const [severityGrade, setSeverityGrade] = useState<number>(2);

  const calculatedRisk = (severityGrade * 22.5 + 25).toFixed(1);

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-3xl mx-auto">
      <div className="flex items-start justify-between border-b pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">
              ICD-10: C74.10
            </span>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">
              SNOMED: 7718002
            </span>
          </div>
          <h3 className="text-lg font-bold text-slate-900 mt-1.5">Adrenal Medullary Pheochromocytoma</h3>
          <span className="text-xs text-slate-500 font-medium">Endocrinology</span>
        </div>
        <BookOpen className="w-6 h-6 text-blue-600 flex-shrink-0" />
      </div>

      <div className="grid grid-cols-2 gap-4 text-xs">
        <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
          <span className="text-slate-500 font-medium">Cardiovascular Risk Multiplier</span>
          <div className="text-lg font-extrabold text-slate-900 mt-0.5">1.85x Baseline</div>
        </div>

        <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
          <span className="text-slate-500 font-medium">Computed Progression Index</span>
          <div className="text-lg font-extrabold text-indigo-600 mt-0.5">{calculatedRisk} / 100</div>
        </div>
      </div>

      <div className="space-y-2 pt-1 text-xs">
        <span className="font-bold text-slate-700 uppercase tracking-wider block">Clinical Action Directives</span>
        <ul className="space-y-1.5 text-slate-600">
          <li className="flex items-center gap-2">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
            <span>Implement guideline-directed organ protection pharmacotherapy.</span>
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
            <span>Annual surveillance of renal, metabolic, and hemodynamic parameters.</span>
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
            <span>Target LDL-C reduction &gt; 50% and strict blood pressure control &lt; 130/80 mmHg.</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
