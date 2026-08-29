"use client";

import React from "react";
import { AlertTriangle, CheckCircle2, Info } from "lucide-react";

interface AnomalyProps {
  coherenceReport?: {
    is_physiologically_coherent: boolean;
    discrepancy_count: number;
    discrepancies: Array<{
      type: string;
      severity: string;
      parameter: string;
      message: string;
    }>;
  };
}

export default function BiomarkerAnomalyAlert({ coherenceReport }: AnomalyProps) {
  if (!coherenceReport || coherenceReport.is_physiologically_coherent) {
    return null;
  }

  return (
    <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 space-y-2 text-xs">
      <div className="flex items-center gap-2 text-rose-800 font-bold">
        <AlertTriangle className="w-4 h-4 text-rose-600" />
        Physiological Discrepancy Warning ({coherenceReport.discrepancy_count} detected)
      </div>

      <p className="text-rose-700 text-[11px]">
        The entered laboratory values exhibit physiological inconsistencies that may distort ML risk scoring:
      </p>

      <ul className="space-y-1 mt-2">
        {coherenceReport.discrepancies.map((d, i) => (
          <li key={i} className="bg-white p-2 rounded border border-rose-200 text-rose-900 font-medium flex items-start gap-1.5">
            <span className="text-rose-600 font-bold">•</span>
            <span>{d.message}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
