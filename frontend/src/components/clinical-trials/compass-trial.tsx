"use client";

import React from "react";
import { BookOpen, CheckCircle, Award, ArrowUpRight } from "lucide-react";

export default function CompassTrialCard() {
  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            Vascular Landmark Trial
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">COMPASS: Rivaroxaban with or without Aspirin in Stable Cardiovascular Disease</h3>
          <p className="text-xs text-slate-500">Eikelboom et al. N Engl J Med 2017</p>
        </div>
        <Award className="w-6 h-6 text-emerald-600 flex-shrink-0" />
      </div>

      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs flex justify-between items-center">
        <span className="text-slate-600 font-medium">Primary Outcome Effect:</span>
        <span className="font-extrabold text-slate-900 bg-white px-2.5 py-1 rounded border border-slate-200">
          0.76 (0.66-0.86)
        </span>
      </div>
    </div>
  );
}
