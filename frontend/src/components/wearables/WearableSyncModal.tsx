"use client";

import React, { useState } from "react";
import { Watch, Smartphone, CheckCircle, UploadCloud } from "lucide-react";

export default function WearableSyncModal() {
  const [syncing, setSyncing] = useState<boolean>(false);
  const [synced, setSynced] = useState<boolean>(false);

  const handleSync = () => {
    setSyncing(true);
    setTimeout(() => {
      setSyncing(false);
      setSynced(true);
    }, 1200);
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 max-w-md mx-auto">
      <div className="flex items-center gap-3 border-b pb-3">
        <Watch className="w-6 h-6 text-blue-600" />
        <div>
          <h3 className="text-sm font-bold text-slate-900">Wearable HealthKit Sync</h3>
          <p className="text-xs text-slate-500">Apple Watch • Garmin • Google Pixel Watch</p>
        </div>
      </div>

      <div className="p-4 bg-slate-50 rounded-xl border text-xs space-y-2 text-slate-700">
        <div className="flex justify-between">
          <span className="text-slate-500">Resting Heart Rate:</span>
          <span className="font-bold text-slate-900">68 bpm</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">HRV (SDNN):</span>
          <span className="font-bold text-slate-900">54 ms</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Estimated VO2 Max:</span>
          <span className="font-bold text-slate-900">42.1 mL/kg/min</span>
        </div>
      </div>

      <button
        onClick={handleSync}
        disabled={syncing}
        className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2"
      >
        <UploadCloud className="w-4 h-4" />
        {synced ? "✓ Synchronized with HealthKit" : syncing ? "Connecting..." : "Sync Vitals from HealthKit"}
      </button>
    </div>
  );
}
