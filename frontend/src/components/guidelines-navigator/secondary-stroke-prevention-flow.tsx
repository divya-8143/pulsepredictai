"use client";

import React, { useState } from "react";
import { GitMerge, CheckCircle2, ArrowRight, ShieldCheck, HelpCircle } from "lucide-react";

export default function SecondaryStrokePreventionFlowVisualizer() {
  const [activeStep, setActiveStep] = useState<number>(1);

  const steps = [
    { step: 1, title: "Diagnostic Criteria & Inclusion Gate", desc: "Confirm formal clinical indications, rule out secondary reversible etiologies." },
    { step: 2, title: "Biomarker Risk Stratification", desc: "Evaluate quantitative threshold cutoffs (Lipids, Blood Pressure, eGFR, Glycemia)." },
    { step: 3, title: "First-Line GDMT Allocation", desc: "Initiate evidence-backed class I therapeutic regimen at guideline starting doses." },
    { step: 4, title: "6-Week Titration & Safety Re-Evaluation", desc: "Check renal parameters, electrolytes, drug tolerance, and achieve target goal." }
  ];

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
            Neurology Decision Tree
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">AHA/ASA 2021 TIA / Ischemic Stroke Secondary Neuroprotection Flow</h3>
        </div>
        <GitMerge className="w-6 h-6 text-indigo-600" />
      </div>

      <div className="space-y-3 pt-2">
        {steps.map((s) => (
          <div
            key={s.step}
            onClick={() => setActiveStep(s.step)}
            className={`p-4 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
              activeStep === s.step
                ? "bg-indigo-50 border-indigo-300 shadow-sm"
                : "bg-slate-50 border-slate-200 hover:bg-slate-100"
            }`}
          >
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
              activeStep === s.step ? "bg-indigo-600 text-white" : "bg-slate-200 text-slate-700"
            }`}>
              {s.step}
            </div>
            <div className="flex-1">
              <h4 className="text-xs font-bold text-slate-900">{s.title}</h4>
              <p className="text-xs text-slate-600 mt-0.5">{s.desc}</p>
            </div>
            {activeStep === s.step && (
              <CheckCircle2 className="w-5 h-5 text-indigo-600 flex-shrink-0" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
