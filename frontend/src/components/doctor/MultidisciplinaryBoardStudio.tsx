"use client";

import React, { useState } from "react";
import { Users, FileCheck, Stethoscope, MessageSquare, CheckCircle2, Award } from "lucide-react";

export default function MultidisciplinaryBoardStudio() {
  const [notes, setNotes] = useState<string>("Patient presents with complex cardiorenal metabolic syndrome. Recommend dual SGLT2i + high-intensity statin titration.");
  const [signed, setSigned] = useState<boolean>(false);

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
            Cardiology • Nephrology • Endocrinology
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-1">Multidisciplinary Clinical Board Studio</h2>
        </div>
        <Users className="w-7 h-7 text-indigo-600" />
      </div>

      <div className="grid grid-cols-3 gap-3 text-xs">
        <div className="p-3 bg-slate-50 border rounded-xl">
          <span className="text-slate-500 font-medium">Attending Cardiologist</span>
          <div className="font-bold text-slate-800 mt-0.5">Dr. Sarah Jenkins, MD, FACC</div>
          <span className="text-[10px] text-emerald-600 font-semibold">✓ Signed Off</span>
        </div>

        <div className="p-3 bg-slate-50 border rounded-xl">
          <span className="text-slate-500 font-medium">Consulting Nephrologist</span>
          <div className="font-bold text-slate-800 mt-0.5">Dr. Marcus Vance, MD, FASN</div>
          <span className="text-[10px] text-emerald-600 font-semibold">✓ Signed Off</span>
        </div>

        <div className="p-3 bg-slate-50 border rounded-xl">
          <span className="text-slate-500 font-medium">Lead Endocrinologist</span>
          <div className="font-bold text-slate-800 mt-0.5">Dr. Elena Rostova, MD</div>
          <span className="text-[10px] text-amber-600 font-semibold">Pending Review</span>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <label className="font-bold text-slate-700 uppercase">Board Consensus Clinical Directives</label>
        <textarea
          rows={3}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="w-full p-3 border rounded-xl focus:ring-2 focus:ring-indigo-500 text-slate-800"
        />
      </div>

      <div className="flex items-center justify-between pt-2">
        <span className="text-xs text-slate-500 flex items-center gap-1">
          <Award className="w-4 h-4 text-indigo-600" />
          Quorum Met (2/3 Specialists Confirmed)
        </span>

        <button
          onClick={() => setSigned(true)}
          className={`px-5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
            signed ? "bg-emerald-600 text-white" : "bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
          }`}
        >
          <FileCheck className="w-4 h-4" />
          {signed ? "Consensus Digitally Signed" : "Digitally Sign Board Consensus"}
        </button>
      </div>
    </div>
  );
}
