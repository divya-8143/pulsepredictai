"use client";

import React, { useState, useEffect } from "react";
import { Activity, Heart, Zap, AlertTriangle, ShieldCheck, Wifi, RefreshCw } from "lucide-react";

export default function LiveVitalsTelemetry() {
  const [hr, setHr] = useState<number>(74);
  const [spo2, setSpo2] = useState<number>(98.5);
  const [sbp, setSbp] = useState<number>(122);
  const [dbp, setDbp] = useState<number>(78);
  const [isStreaming, setIsStreaming] = useState<boolean>(true);

  useEffect(() => {
    if (!isStreaming) return;
    const interval = setInterval(() => {
      setHr((prev) => Math.min(130, Math.max(55, Math.round(prev + (Math.random() * 6 - 3)))));
      setSpo2((prev) => Math.min(100, Math.max(92, Number((prev + (Math.random() * 0.4 - 0.2)).toFixed(1)))));
      setSbp((prev) => Math.min(160, Math.max(105, Math.round(prev + (Math.random() * 4 - 2)))));
      setDbp((prev) => Math.min(95, Math.max(65, Math.round(prev + (Math.random() * 3 - 1.5)))));
    }, 1500);
    return () => clearInterval(interval);
  }, [isStreaming]);

  const map = ((2 * dbp + sbp) / 3).toFixed(1);
  const rpp = Math.round((hr * sbp) / 100);

  return (
    <div className="bg-slate-900 text-white rounded-2xl p-6 border border-slate-800 shadow-xl space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
          <div>
            <h3 className="text-base font-bold flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              Live Telemetry Stream
            </h3>
            <span className="text-xs text-slate-400">Continuous Wearable & Bedside Monitor Integration</span>
          </div>
        </div>
        <button
          onClick={() => setIsStreaming(!isStreaming)}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
            isStreaming ? "bg-rose-500/20 text-rose-300 border border-rose-500/40" : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
          }`}
        >
          <Wifi className="w-3.5 h-3.5" />
          {isStreaming ? "Pause Live Stream" : "Resume Stream"}
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700">
          <span className="text-[10px] uppercase font-bold text-slate-400 flex items-center gap-1">
            <Heart className="w-3 h-3 text-rose-400 animate-pulse" />
            Heart Rate
          </span>
          <div className="text-3xl font-black text-white mt-1">{hr}</div>
          <span className="text-[10px] text-emerald-400 font-semibold">BPM (Normal Sinus)</span>
        </div>

        <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700">
          <span className="text-[10px] uppercase font-bold text-slate-400">Oxygen Saturation</span>
          <div className="text-3xl font-black text-white mt-1">{spo2}%</div>
          <span className="text-[10px] text-emerald-400 font-semibold">SpO2 Optimal</span>
        </div>

        <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700">
          <span className="text-[10px] uppercase font-bold text-slate-400">Blood Pressure</span>
          <div className="text-3xl font-black text-white mt-1">{sbp}/{dbp}</div>
          <span className="text-[10px] text-slate-400 font-semibold">mmHg</span>
        </div>

        <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700">
          <span className="text-[10px] uppercase font-bold text-slate-400">Mean Arterial Press.</span>
          <div className="text-3xl font-black text-indigo-400 mt-1">{map}</div>
          <span className="text-[10px] text-indigo-300 font-semibold">mmHg (MAP)</span>
        </div>
      </div>
    </div>
  );
}
