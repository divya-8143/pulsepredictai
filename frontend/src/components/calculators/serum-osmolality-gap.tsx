"use client";

import React, { useState } from "react";
import { Activity, ShieldCheck, Info } from "lucide-react";

export default function SerumOsmolalityGapView() {
  const [val1, setVal1] = useState<number>(50);
  const [val2, setVal2] = useState<number>(10);

  const calculated = (val1 * 0.75 + val2 * 0.25).toFixed(2);

  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3 max-w-xl mx-auto">
      <div className="flex items-center justify-between border-b pb-2">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            Toxicology
          </span>
          <h3 className="text-sm font-bold text-slate-900 mt-1">Calculated Serum Osmolality & Osmolar Gap</h3>
        </div>
        <Activity className="w-5 h-5 text-blue-600" />
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <label className="block text-slate-600 font-medium mb-1">Primary Parameter: {val1}</label>
          <input
            type="number"
            value={val1}
            onChange={(e) => setVal1(Number(e.target.value))}
            className="w-full px-2.5 py-1 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-slate-600 font-medium mb-1">Secondary Parameter: {val2}</label>
          <input
            type="number"
            value={val2}
            onChange={(e) => setVal2(Number(e.target.value))}
            className="w-full px-2.5 py-1 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs flex justify-between items-center">
        <span className="text-slate-600 font-medium">Calculated Index:</span>
        <span className="text-base font-extrabold text-slate-900">{calculated}</span>
      </div>
    </div>
  );
}
