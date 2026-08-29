"use client";
import React from "react";
import { Compass, ShieldCheck } from "lucide-react";

export default function CardioRadarWidget() {
  return (
    <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
      <h4 className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
        <Compass className="w-4 h-4 text-indigo-600" />
        Cardiovascular Multi-Axis Radar Visualizer
      </h4>
    </div>
  );
}
