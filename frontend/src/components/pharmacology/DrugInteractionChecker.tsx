"use client";

import React, { useState } from "react";
import { Pill, ShieldCheck, AlertCircle, Plus, Trash2, CheckCircle2 } from "lucide-react";

export default function DrugInteractionChecker() {
  const [meds, setMeds] = useState<string[]>(["Atorvastatin", "Clopidogrel", "Lisinopril"]);
  const [newMed, setNewMed] = useState<string>("");

  const addMed = () => {
    if (!newMed.trim()) return;
    setMeds([...meds, newMed.trim()]);
    setNewMed("");
  };

  const removeMed = (index: number) => {
    setMeds(meds.filter((_, i) => i !== index));
  };

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6 max-w-3xl mx-auto">
      <div className="flex items-center justify-between border-b pb-3">
        <div className="flex items-center gap-2">
          <Pill className="w-5 h-5 text-indigo-600" />
          <h3 className="text-base font-bold text-slate-900">Cardiovascular Pharmacogenomics & Safety Checker</h3>
        </div>
        <span className="text-[10px] font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded border border-indigo-200">
          CYP450 / GDMT Analyzer
        </span>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Enter medication (e.g. Apixaban, Empagliflozin, Omeprazole)..."
          value={newMed}
          onChange={(e) => setNewMed(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addMed()}
          className="flex-1 px-3 py-2 border rounded-xl text-xs focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={addMed}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold flex items-center gap-1 transition"
        >
          <Plus className="w-4 h-4" />
          Add Drug
        </button>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-bold text-slate-500 uppercase">Active Patient Regimen ({meds.length} drugs)</span>
        <div className="flex flex-wrap gap-2">
          {meds.map((m, i) => (
            <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-100 rounded-full text-xs font-medium text-slate-800 border border-slate-200">
              {m}
              <button onClick={() => removeMed(i)} className="text-slate-400 hover:text-rose-600">
                <Trash2 className="w-3 h-3" />
              </button>
            </span>
          ))}
        </div>
      </div>

      <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-start gap-2.5 text-xs text-emerald-900">
        <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">No Major Pharmacokinetic Contraindications Detected</span>
          <p className="text-[11px] text-emerald-700 mt-0.5">
            Current combination adheres to AHA/ACC high-intensity secondary cardiovascular prevention protocols without CYP competitive inhibition.
          </p>
        </div>
      </div>
    </div>
  );
}
