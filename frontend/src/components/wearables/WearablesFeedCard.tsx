"use client";
import React from "react";
import { Watch, Heart, Flame } from "lucide-react";

export default function WearablesFeedCard() {
  return (
    <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
      <h4 className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
        <Watch className="w-4 h-4 text-blue-600" />
        Wearables Live Biometrics Stream
      </h4>
      <p className="text-[11px] text-slate-500">Apple HealthKit & Google Health Connect sync active.</p>
    </div>
  );
}
