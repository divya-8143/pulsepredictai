'use client';

import React, { useEffect, useState } from "react";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { apiClient } from "@/lib/api";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import { Users, PieChart as PieIcon, Activity } from "lucide-react";

export default function AnalyticsDashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const res = await apiClient.get("/analytics/population-risk");
      setData(res.data);
    } catch (e) {
      console.error("Failed to load analytics", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 w-full">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-mono text-[11px] font-bold">EPIDEMIOLOGICAL ANALYTICS</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Population Risk & Biomarker Distribution</h1>
          <p className="text-xs text-slate-500 mt-1">Cross-cohort analytics across screened patient populations.</p>
        </div>

        {data && (
          <>
            {/* Population Distribution Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm text-center">
                <span className="text-xs font-bold text-slate-400 uppercase">Low Risk Cohort</span>
                <p className="text-3xl font-extrabold text-emerald-600 mt-1">{data.distribution.low_risk_percent}%</p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm text-center">
                <span className="text-xs font-bold text-slate-400 uppercase">Moderate Risk Cohort</span>
                <p className="text-3xl font-extrabold text-amber-600 mt-1">{data.distribution.moderate_risk_percent}%</p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm text-center">
                <span className="text-xs font-bold text-slate-400 uppercase">High Risk Cohort</span>
                <p className="text-3xl font-extrabold text-orange-600 mt-1">{data.distribution.high_risk_percent}%</p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm text-center">
                <span className="text-xs font-bold text-slate-400 uppercase">Critical Risk Cohort</span>
                <p className="text-3xl font-extrabold text-rose-600 mt-1">{data.distribution.critical_risk_percent}%</p>
              </div>
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Average Biomarkers by Risk Category */}
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <div>
                  <h3 className="font-bold text-base text-slate-900">Biomarker Averages Across Risk Tiers</h3>
                  <p className="text-xs text-slate-500">Mean systolic BP, glucose, and total cholesterol by category.</p>
                </div>
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.cohort_averages} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="risk_category" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
                      <Bar dataKey="avg_systolic_bp" fill="#3b82f6" name="Systolic BP (mmHg)" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="avg_fasting_glucose" fill="#8b5cf6" name="Glucose (mg/dL)" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="avg_total_cholesterol" fill="#f59e0b" name="Cholesterol (mg/dL)" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Age Cohorts Risk Prevalence */}
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <div>
                  <h3 className="font-bold text-base text-slate-900">Risk Stratification by Age Decile</h3>
                  <p className="text-xs text-slate-500">Patient count distributions across demographic age tiers.</p>
                </div>
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.age_cohorts} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="age_group" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
                      <Bar dataKey="low" stackId="a" fill="#10b981" name="Low" />
                      <Bar dataKey="moderate" stackId="a" fill="#f59e0b" name="Moderate" />
                      <Bar dataKey="high" stackId="a" fill="#f97316" name="High" />
                      <Bar dataKey="critical" stackId="a" fill="#ef4444" name="Critical" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
