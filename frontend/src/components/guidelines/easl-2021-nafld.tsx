"use client";

import React, { useState } from "react";
import { BookOpen, CheckCircle2, AlertTriangle, ShieldCheck, HeartPulse, ChevronRight, Sparkles } from "lucide-react";

export default function EASL_2021_NAFLDGuidelineExplorer() {
  const [selectedPillar, setSelectedPillar] = useState<string>("Lipid Management");

  const pillars = [
    {
      title: "Lipid Management",
      grade: "Class I, Level A",
      action: "Moderate-to-High Intensity Statin Therapy for High-Risk & Diabetic Cohorts",
      target: "LDL-C < 70 mg/dL (or < 55 mg/dL if multi-vessel disease)",
      firstLine: ["Atorvastatin 40-80mg", "Rosuvastatin 20-40mg", "Ezetimibe 10mg addon"]
    },
    {
      title: "Hypertension Protocol",
      grade: "Class I, Level A",
      action: "Dual First-Line Therapy for SBP >= 140 or DBP >= 90 mmHg",
      target: "Standardized Office BP < 130/80 mmHg",
      firstLine: ["ACEi/ARB + Dihydro-CCB", "Thiazide-like Diuretic (Chlorthalidone/Indapamide)"]
    },
    {
      title: "Cardiometabolic & Glycemic Protection",
      grade: "Class I, Level A",
      action: "SGLT2 Inhibitor & GLP-1 Receptor Agonist Organ Protection",
      target: "HbA1c < 7.0% with proven MACE & HF reduction",
      firstLine: ["Empagliflozin 10-25mg", "Dapagliflozin 10mg", "Semaglutide 0.5-1.0mg weekly"]
    },
    {
      title: "Antiplatelet Allocation",
      grade: "Class I / Class III",
      action: "Lifelong Aspirin 81mg for Secondary Prevention; Restrict Primary Routine Use in Elderly",
      target: "Thrombosis suppression with minimal gastrointestinal bleeding",
      firstLine: ["Aspirin 81mg enteric-coated", "Clopidogrel 75mg daily"]
    }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto p-4">
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex items-start justify-between">
          <div>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">
              Hepatology Guideline Core
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-2">EASL Clinical Practice Guidelines on the Management of Metabolic Dysfunction-Associated Steatotic Liver Disease (MASLD)</h2>
            <p className="text-xs text-slate-500 mt-1">European Association for the Study of the Liver. J Hepatol. 2021;75(3):659-689</p>
          </div>
          <BookOpen className="w-8 h-8 text-indigo-600 flex-shrink-0" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {pillars.map((p) => (
          <button
            key={p.title}
            onClick={() => setSelectedPillar(p.title)}
            className={`p-4 rounded-xl text-left border transition-all ${
              selectedPillar === p.title
                ? "bg-indigo-600 text-white border-indigo-600 shadow-md"
                : "bg-white text-slate-700 border-slate-200 hover:border-indigo-300"
            }`}
          >
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
              selectedPillar === p.title ? "bg-indigo-500 text-white" : "bg-slate-100 text-slate-600"
            }`}>
              {p.grade}
            </span>
            <h3 className="font-semibold text-sm mt-2 line-clamp-1">{p.title}</h3>
          </button>
        ))}
      </div>

      {/* Detail View */}
      {pillars.filter(p => p.title === selectedPillar).map(p => (
        <div key={p.title} className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b pb-3">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              {p.title} — Decision Pathway
            </h3>
            <span className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold border border-indigo-200">
              {p.grade}
            </span>
          </div>

          <div className="space-y-3">
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Clinical Directive</span>
              <p className="text-sm text-slate-800 font-medium mt-0.5">{p.action}</p>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Therapeutic Target</span>
              <p className="text-sm text-slate-800 font-medium mt-0.5">{p.target}</p>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Guideline-Directed Medical Therapy (GDMT)</span>
              <ul className="mt-1 space-y-1">
                {p.firstLine.map((drug, i) => (
                  <li key={i} className="text-xs text-slate-700 flex items-center gap-2 bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
                    <span className="font-medium">{drug}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
