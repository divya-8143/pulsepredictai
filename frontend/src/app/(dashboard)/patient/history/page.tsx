'use client';

import React, { useEffect, useState } from "react";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { apiClient } from "@/lib/api";
import { AssessmentHistoryItem } from "@/types";
import Link from "next/link";
import { ArrowLeft, Calendar, FileText, ChevronLeft, ChevronRight, Download, Utensils, Loader2 } from "lucide-react";
import PersonalizedDietPlan from "@/components/PersonalizedDietPlan";

export default function HistoryPage() {
  const [items, setItems] = useState<AssessmentHistoryItem[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);
  const [selectedDietId, setSelectedDietId] = useState<string | null>(null);
  const [dietPlanData, setDietPlanData] = useState<any>(null);
  const [loadingDiet, setLoadingDiet] = useState(false);

  useEffect(() => {
    fetchHistory(page);
  }, [page]);

  const fetchHistory = async (p: number) => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/assessments/history?page=${p}&page_size=8`);
      setItems(res.data.items);
      setTotalPages(res.data.total_pages);
    } catch (e) {
      console.error("Failed to fetch history", e);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async (id: string) => {
    setDownloadingId(id);
    try {
      const response = await apiClient.get(`/assessments/${id}/report`, {
        responseType: "blob"
      });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `PulsePredict_Assessment_${id.slice(0, 8)}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to download PDF report", err);
      alert("Failed to download clinical PDF report.");
    } finally {
      setDownloadingId(null);
    }
  };

  const handleOpenDietPlan = async (id: string) => {
    if (selectedDietId === id) {
      setSelectedDietId(null);
      return;
    }
    setSelectedDietId(id);
    setLoadingDiet(true);
    try {
      const res = await apiClient.get(`/assessments/${id}/diet-plan`);
      setDietPlanData(res.data);
    } catch (err) {
      console.error("Failed to fetch diet plan", err);
    } finally {
      setLoadingDiet(false);
    }
  };

  const getRiskBadge = (cat: string) => {
    switch (cat) {
      case "LOW":
        return "bg-emerald-100 text-emerald-800";
      case "MODERATE":
        return "bg-amber-100 text-amber-800";
      case "HIGH":
        return "bg-orange-100 text-orange-800";
      case "CRITICAL":
        return "bg-rose-100 text-rose-800";
      default:
        return "bg-slate-100 text-slate-800";
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 w-full">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Assessment & Diet History</h1>
            <p className="text-xs text-slate-500 mt-1">Download past clinical reports and review your customized nutrition plans.</p>
          </div>
          <Link href="/patient" className="text-xs font-semibold text-slate-600 hover:text-blue-600 flex items-center gap-1">
            <ArrowLeft className="w-4 h-4" />
            Dashboard
          </Link>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase font-semibold">
                <tr>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3">Risk Category</th>
                  <th className="px-6 py-3">Risk Score</th>
                  <th className="px-6 py-3">Blood Pressure</th>
                  <th className="px-6 py-3">Glucose</th>
                  <th className="px-6 py-3">BMI</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.length > 0 ? (
                  items.map((it) => (
                    <React.Fragment key={it.id}>
                      <tr className="hover:bg-slate-50/80 transition">
                        <td className="px-6 py-4 text-slate-900 font-medium">{new Date(it.assessed_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2.5 py-1 rounded-full font-bold text-[10px] uppercase ${getRiskBadge(it.risk_category)}`}>
                            {it.risk_category}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-mono font-bold text-slate-800">{it.overall_risk_score.toFixed(1)} / 100</td>
                        <td className="px-6 py-4 text-slate-600">{it.systolic_bp} / {it.diastolic_bp} mmHg</td>
                        <td className="px-6 py-4 text-slate-600">{it.fasting_glucose} mg/dL</td>
                        <td className="px-6 py-4 text-slate-600">{it.bmi} kg/m²</td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => handleDownloadPdf(it.id)}
                              disabled={downloadingId === it.id}
                              title="Download PDF Report"
                              className="p-2 text-blue-600 hover:bg-blue-50 border border-blue-200 rounded-lg transition disabled:opacity-40"
                            >
                              {downloadingId === it.id ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              ) : (
                                <Download className="w-3.5 h-3.5" />
                              )}
                            </button>

                            <button
                              onClick={() => handleOpenDietPlan(it.id)}
                              title="View Balanced Diet Plan"
                              className={`p-2 rounded-lg border transition ${
                                selectedDietId === it.id
                                  ? "bg-emerald-600 text-white border-emerald-600"
                                  : "text-emerald-700 hover:bg-emerald-50 border-emerald-200"
                              }`}
                            >
                              <Utensils className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                      {selectedDietId === it.id && (
                        <tr>
                          <td colSpan={7} className="p-4 bg-slate-50 border-b border-slate-200">
                            {loadingDiet ? (
                              <div className="py-6 text-center text-xs text-slate-500">
                                <Loader2 className="w-5 h-5 animate-spin mx-auto text-emerald-600 mb-1" />
                                Loading personalized diet plan...
                              </div>
                            ) : (
                              <PersonalizedDietPlan plan={dietPlanData} assessmentId={selectedDietId || undefined} />
                            )}
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  ))
                ) : (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-slate-400">
                      No assessment history found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-6 py-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
              <span>Page {page} of {totalPages}</span>
              <div className="flex items-center gap-2">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="p-1 rounded border border-slate-200 disabled:opacity-40"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  className="p-1 rounded border border-slate-200 disabled:opacity-40"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
