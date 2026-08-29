'use client';

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { apiClient } from "@/lib/api";
import { useAuthStore } from "@/lib/auth-store";
import { Users, AlertTriangle, Flame, CheckCircle2, Stethoscope, ChevronRight, Search } from "lucide-react";

export default function DoctorDashboard() {
  const { user, initialize } = useAuthStore();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initialize();
    loadDoctorStats();
  }, []);

  const loadDoctorStats = async () => {
    try {
      const res = await apiClient.get("/doctor/dashboard");
      setStats(res.data);
    } catch (e) {
      console.error("Failed to load doctor dashboard", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 w-full">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-md bg-purple-100 text-purple-700 font-mono text-[11px] font-bold">PHYSICIAN CONSOLE</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">Welcome, Dr. {user?.full_name || "Physician"}</h1>
            <p className="text-xs text-slate-500 mt-1">Clinical decision support and risk stratification overview across your patient panel.</p>
          </div>

          <Link
            href="/doctor/patients"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs rounded-xl shadow transition"
          >
            <Users className="w-4 h-4" />
            View Patient Roster
          </Link>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-rose-600">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Critical Risk</span>
              <Flame className="w-5 h-5" />
            </div>
            <p className="text-3xl font-extrabold text-slate-900">{stats?.critical_risk_count || 0}</p>
            <span className="text-[11px] text-rose-600 font-semibold">Immediate clinical attention required</span>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-orange-600">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">High Risk</span>
              <AlertTriangle className="w-5 h-5" />
            </div>
            <p className="text-3xl font-extrabold text-slate-900">{stats?.high_risk_count || 0}</p>
            <span className="text-[11px] text-orange-600 font-semibold">Flagged for preventive review</span>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-amber-600">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Moderate Risk</span>
              <AlertTriangle className="w-5 h-5" />
            </div>
            <p className="text-3xl font-extrabold text-slate-900">{stats?.moderate_risk_count || 0}</p>
            <span className="text-[11px] text-amber-600 font-semibold">Lifestyle intervention recommended</span>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-emerald-600">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Low Risk</span>
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <p className="text-3xl font-extrabold text-slate-900">{stats?.low_risk_count || 0}</p>
            <span className="text-[11px] text-emerald-600 font-semibold">Physiological baseline optimal</span>
          </div>
        </div>

        {/* Priority Case Review Queue */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900">Priority Clinical Review Queue</h3>
              <p className="text-xs text-slate-500">Patients presenting with high or critical multi-factor cardiovascular/metabolic risks.</p>
            </div>
            <Link href="/doctor/patients" className="text-xs font-semibold text-purple-600 hover:underline flex items-center gap-1">
              All Patients <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="divide-y divide-slate-100">
            {stats?.recent_critical_patients && stats.recent_critical_patients.length > 0 ? (
              stats.recent_critical_patients.map((p: any) => (
                <div key={p.patient_id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-sm text-slate-900">{p.full_name}</span>
                      <span className="text-xs text-slate-400">({p.gender}, Age {p.age})</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">{p.email}</p>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                      p.latest_risk_category === "CRITICAL" ? "bg-rose-100 text-rose-800" : "bg-orange-100 text-orange-800"
                    }`}>
                      {p.latest_risk_category}: {p.latest_risk_score} / 100
                    </span>

                    <Link
                      href="/doctor/patients"
                      className="px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs font-semibold rounded-lg transition"
                    >
                      Review Case
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              <p className="py-8 text-center text-slate-400 text-xs">No pending critical risk cases in queue.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
