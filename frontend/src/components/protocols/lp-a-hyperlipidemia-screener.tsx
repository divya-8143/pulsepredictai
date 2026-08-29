"use client";

import React, { useState } from "react";
import { Stethoscope, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Clock } from "lucide-react";

export default function LpAHyperlipidemiaScreenerProtocolWidget() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [biomarker, setBiomarker] = useState<number>(135);

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4 max-w-3xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
            Lipidology Protocol
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">Lipoprotein(a) [Lp(a)] Elevated Cardiovascular Residual Risk Engine</h3>
        </div>
        <Stethoscope className="w-6 h-6 text-indigo-600" />
      </div>

      <div className="flex gap-2 border-b pb-4">
        {[1, 2, 3].map((step) => (
          <button
            key={step}
            onClick={() => setCurrentStep(step)}
            className={`flex-1 py-2 px-3 rounded-lg text-xs font-semibold border text-center transition-all ${
              currentStep === step
                ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
            }`}
          >
            Step {step}: {step === 1 ? "Initiation" : step === 2 ? "Dual Titration" : "Triple / Refractory"}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        <h4 className="text-xs font-bold text-slate-600 uppercase tracking-wider">Protocol Directives for Step {currentStep}</h4>
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 text-xs text-slate-700">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span className="font-semibold text-slate-900">
              {currentStep === 1 ? "First-Line Guideline Directed Monotherapy (Standard Dose)" : currentStep === 2 ? "Combination Dual Pharmacotherapy (High-Potency)" : "Triple Pathway GDMT + Specialty Multi-Disciplinary Care"}
            </span>
          </div>
          <p className="text-slate-600 pl-6">
            {currentStep === 1
              ? "Establish baseline laboratory panel (renal function, transaminases, electrolytes). Emphasize dietary sodium restriction and lifestyle."
              : currentStep === 2
              ? "Re-assess primary therapeutic biomarker target at 6 weeks. If non-responsive or tolerated, uptitrate to maximal labeled dose."
              : "Evaluate secondary causes, medication adherence, and consider specialized interventional or novel biological therapies."}
          </p>
        </div>

        <div className="grid grid-cols-3 gap-3 pt-2">
          <div className="p-3 bg-white border border-slate-200 rounded-lg text-xs">
            <span className="text-slate-500 block mb-1 flex items-center gap-1 font-medium">
              <Clock className="w-3 h-3 text-indigo-600" />
              Week 2 Check
            </span>
            <span className="font-semibold text-slate-800">Safety labs & tolerability</span>
          </div>

          <div className="p-3 bg-white border border-slate-200 rounded-lg text-xs">
            <span className="text-slate-500 block mb-1 flex items-center gap-1 font-medium">
              <Clock className="w-3 h-3 text-indigo-600" />
              Week 6-8 Check
            </span>
            <span className="font-semibold text-slate-800">Biomarker target review</span>
          </div>

          <div className="p-3 bg-white border border-slate-200 rounded-lg text-xs">
            <span className="text-slate-500 block mb-1 flex items-center gap-1 font-medium">
              <Clock className="w-3 h-3 text-indigo-600" />
              Month 6 Check
            </span>
            <span className="font-semibold text-slate-800">Longitudinal surveillance</span>
          </div>
        </div>
      </div>
    </div>
  );
}
