"use client";

import React from "react";
import { ShieldCheck, AlertCircle, HelpCircle } from "lucide-react";

interface UncertaintyProps {
  confidenceInterval?: {
    lower_bound: number;
    upper_bound: number;
    formatted: string;
  };
  uncertaintyTier?: string;
  confidenceGrade?: string;
  isOOD?: boolean;
}

export default function UncertaintyBadge({
  confidenceInterval,
  confidenceGrade = "High (Models Unanimously Agree)",
  isOOD = false
}: UncertaintyProps) {
  return (
    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-2">
      <div className="flex items-center justify-between">
        <span className="font-semibold text-slate-700 flex items-center gap-1.5">
          {isOOD ? (
            <AlertCircle className="w-4 h-4 text-amber-600" />
          ) : (
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          )}
          Bayesian Confidence & Uncertainty
        </span>
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
          isOOD ? "bg-amber-100 text-amber-800" : "bg-emerald-100 text-emerald-800"
        }`}>
          {isOOD ? "Out-of-Distribution" : "95% Credible Interval"}
        </span>
      </div>

      {confidenceInterval && (
        <div className="flex justify-between items-center bg-white p-2.5 rounded-lg border border-slate-200">
          <span className="text-slate-500 font-medium">Risk Score Uncertainty Range:</span>
          <span className="font-bold text-slate-900">{confidenceInterval.formatted}</span>
        </div>
      )}

      <p className="text-[11px] text-slate-500">
        Statistical Reliability: <span className="font-medium text-slate-700">{confidenceGrade}</span>
      </p>
    </div>
  );
}
