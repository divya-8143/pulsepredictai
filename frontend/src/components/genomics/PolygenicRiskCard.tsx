"use client";

import React, { useState } from "react";
import { Dna, ShieldCheck, TrendingUp } from "lucide-react";

export default function PolygenicRiskCard() {
  const [prs, setPrs] = useState<number>(1.6);
  const baseline = 24.5;
  const integrated = (baseline * 1.85).toFixed(1);

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-md mx-auto">
      <div className="flex items-center gap-3 border-b pb-3">
        <Dna className="w-6 h-6 text-purple-600" />
        <div>
          <h3 className="text-sm font-bold text-slate-900">Polygenic Risk Score (PRS)</h3>
          <p className="text-xs text-slate-500">Genome-Wide CAD Risk Blending</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="p-3 bg-purple-50 rounded-xl border border-purple-200">
          <span className="text-purple-700 font-medium">Genetic Multiplier</span>
          <div className="text-xl font-extrabold text-purple-900 mt-1">1.85x Baseline</div>
        </div>
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
          <span className="text-slate-500 font-medium">Integrated 10Y Risk</span>
          <div className="text-xl font-extrabold text-slate-900 mt-1">{integrated}%</div>
        </div>
      </div>
    </div>
  );
}
