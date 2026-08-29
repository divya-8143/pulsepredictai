"use client";
import React from "react";
import { Watch, Heart } from "lucide-react";

export default function WearableLiveWidget() {
  return (
    <div className="p-4 bg-white rounded-xl border border-slate-200">
      <h4 className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
        <Watch className="w-4 h-4 text-blue-600" />
        Wearable Biometrics Live Feed
      </h4>
    </div>
  );
}
