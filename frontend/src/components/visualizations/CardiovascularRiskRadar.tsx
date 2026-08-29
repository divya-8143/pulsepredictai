"use client";
import React from "react";
import { Compass, Shield } from "lucide-react";

export default function CardiovascularRiskRadar() {
  return (
    <div className="p-4 bg-white rounded-xl border border-slate-200">
      <h4 className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
        <Compass className="w-4 h-4 text-indigo-600" />
        Multi-Axis Cardiovascular Risk Radar
      </h4>
    </div>
  );
}
