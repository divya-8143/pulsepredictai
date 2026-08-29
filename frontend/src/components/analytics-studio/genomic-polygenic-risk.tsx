"use client";

import React, { useState } from "react";
import { Activity, BarChart2, ShieldAlert, Users, Layers, TrendingUp, Sparkles, CheckCircle } from "lucide-react";

export default function GenomicPolygenicRiskAnalyticsStudio() {
  const [activeTab, setActiveTab] = useState<string>("overview");

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
            Genomics Studio
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-1">Polygenic Risk Score (PRS) Multi-Locus Imputation & Blending Engine</h2>
        </div>
        <BarChart2 className="w-8 h-8 text-indigo-600" />
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <span className="text-xs text-slate-500 font-medium">Cohort Monitored</span>
          <div className="text-2xl font-black text-slate-900 mt-1">12,480</div>
          <span className="text-[10px] text-emerald-600 font-bold">+4.2% this month</span>
        </div>

        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <span className="text-xs text-slate-500 font-medium">Mean Risk Score</span>
          <div className="text-2xl font-black text-slate-900 mt-1">48.2</div>
          <span className="text-[10px] text-slate-500 font-medium">Standardized scale</span>
        </div>

        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <span className="text-xs text-slate-500 font-medium">GDMT Compliance</span>
          <div className="text-2xl font-black text-emerald-600 mt-1">87.4%</div>
          <span className="text-[10px] text-emerald-600 font-bold">Optimal Target</span>
        </div>

        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <span className="text-xs text-slate-500 font-medium">Predicted Event Drop</span>
          <div className="text-2xl font-black text-indigo-600 mt-1">-28%</div>
          <span className="text-[10px] text-indigo-600 font-bold">5-Year Horizon</span>
        </div>
      </div>

      <div className="p-4 bg-indigo-50 border border-indigo-100 rounded-xl text-xs text-indigo-900 space-y-1">
        <p className="font-bold flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-indigo-600" />
          Automated Clinical Decision Support Insight
        </p>
        <p className="text-indigo-800">
          Stochastic population modeling demonstrates significant risk divergence across glycemic and blood pressure sub-cohorts. Early implementation of combination organ-protective therapy provides maximum risk mitigation.
        </p>
      </div>
    </div>
  );
}
