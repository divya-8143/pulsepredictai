"use client";

import React, { useState } from "react";
import { Activity, HeartPulse, ShieldCheck } from "lucide-react";

export default function KlothoProteinPanel() {
  const [val, setVal] = useState<number>(10);

  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
      <div className="flex items-center justify-between border-b pb-2">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            Nephrology
          </span>
          <h3 className="text-sm font-bold text-slate-900 mt-1">Soluble Alpha-Klotho Anti-Aging Renal Hormone</h3>
        </div>
        <HeartPulse className="w-5 h-5 text-blue-600" />
      </div>

      <div className="text-xs space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-500">Reference Interval:</span>
          <span className="font-semibold text-slate-800">> 500 pg/mL</span>
        </div>
      </div>
    </div>
  );
}
