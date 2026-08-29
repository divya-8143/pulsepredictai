'use client';

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { RiskScoreCard } from "@/components/assessments/RiskScoreCard";
import { BiomarkerTrendChart } from "@/components/charts/BiomarkerTrendChart";
import { apiClient } from "@/lib/api";
import { useAuthStore } from "@/lib/auth-store";
import { PlusCircle, History, Activity, Calendar, ShieldCheck } from "lucide-react";

export default function PatientDashboard() {
  const { user, initialize } = useAuthStore();
  const [trends, setTrends] = useState([]);
  const [latestAssessment, setLatestAssessment] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initialize();
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [trendRes, histRes] = await Promise.all([
        apiClient.get("/assessments/trends"),
        apiClient.get("/assessments/history?page=1&page_size=1")
      ]);
      setTrends(trendRes.data);
      if (histRes.data.items && histRes.data.items.length > 0) {
        // Fetch detailed assessment
        const latestId = histRes.data.items[0].id;
        const detailRes = await apiClient.get(`/assessments/${latestId}`);
        setLatestAssessment(detailRes.data);
      }
    } catch (e) {
      console.error("Failed to load patient dashboard", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 w-full">
        {/* Welcome Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Welcome, {user?.full_name || "Patient"}</h1>
            <p className="text-xs text-slate-500 mt-1">
              Your personalized longitudinal cardiovascular & metabolic risk command center.
            </p>
          </div>
          <Link
            href="/patient/assess"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-xl shadow transition"
          >
            <PlusCircle className="w-4 h-4" />
            New Assessment
          </Link>
        </div>

        {latestAssessment ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <RiskScoreCard
                score={latestAssessment.overall_risk_score}
                category={latestAssessment.risk_category}
                primaryModel={latestAssessment.primary_model_name}
                recommendations={latestAssessment.clinical_recommendations}
              />
            </div>
            <div className="lg:col-span-2">
              <BiomarkerTrendChart data={trends} />
            </div>
          </div>
        ) : (
          <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900">No Health Assessments Recorded Yet</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Submit your baseline blood pressure, cholesterol panel, BMI, and lifestyle biomarkers to generate your first ML risk score.
            </p>
            <Link
              href="/patient/assess"
              className="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow transition"
            >
              Start First Assessment
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
