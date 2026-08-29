'use client';

import React, { useEffect, useState } from "react";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { ReviewModal } from "@/components/doctor/ReviewModal";
import { apiClient } from "@/lib/api";
import { Search, Filter, Stethoscope, ChevronLeft, ChevronRight } from "lucide-react";

export default function DoctorPatientsPage() {
  const [patients, setPatients] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeReviewPatient, setActiveReviewPatient] = useState<any | null>(null);

  useEffect(() => {
    loadPatients();
  }, [riskFilter]);

  const loadPatients = async () => {
    setLoading(true);
    try {
      let url = "/doctor/patients";
      const params = new URLSearchParams();
      if (riskFilter) params.append("risk_category", riskFilter);
      if (search) params.append("search", search);
      
      const res = await apiClient.get(`${url}?${params.toString()}`);
      setPatients(res.data);
    } catch (e) {
      console.error("Failed to load patient roster", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadPatients();
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 w-full">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Patient Risk Roster</h1>
          <p className="text-xs text-slate-500 mt-1">
            Search, filter by risk severity, and provide physician clinical annotations.
          </p>
        </div>

        {/* Filter and Search Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-80">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by patient name or email..."
              className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-purple-500 focus:outline-none"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          </form>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-purple-500 focus:outline-none"
            >
              <option value="">All Risk Categories</option>
              <option value="CRITICAL">Critical Risk (>= 75)</option>
              <option value="HIGH">High Risk (50 - 74)</option>
              <option value="MODERATE">Moderate Risk (25 - 49)</option>
              <option value="LOW">Low Risk (&lt; 25)</option>
            </select>
          </div>
        </div>

        {/* Patient Table */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase font-semibold">
                <tr>
                  <th className="px-6 py-3">Patient</th>
                  <th className="px-6 py-3">Demographics</th>
                  <th className="px-6 py-3">Risk Level</th>
                  <th className="px-6 py-3">Risk Score</th>
                  <th className="px-6 py-3">Last Evaluated</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {patients.length > 0 ? (
                  patients.map((p) => (
                    <tr key={p.patient_id} className="hover:bg-slate-50/80 transition">
                      <td className="px-6 py-4">
                        <div className="font-bold text-slate-900">{p.full_name}</div>
                        <div className="text-slate-400 text-[11px]">{p.email}</div>
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {p.gender || "OTHER"} • {p.age ? `${p.age} yrs` : "N/A"}
                      </td>
                      <td className="px-6 py-4">
                        {p.latest_risk_category ? (
                          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase ${
                            p.latest_risk_category === "CRITICAL" ? "bg-rose-100 text-rose-800" :
                            p.latest_risk_category === "HIGH" ? "bg-orange-100 text-orange-800" :
                            p.latest_risk_category === "MODERATE" ? "bg-amber-100 text-amber-800" :
                            "bg-emerald-100 text-emerald-800"
                          }`}>
                            {p.latest_risk_category}
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[11px]">No assessment</span>
                        )}
                      </td>
                      <td className="px-6 py-4 font-mono font-bold text-slate-800">
                        {p.latest_risk_score !== null ? `${p.latest_risk_score} / 100` : "-"}
                      </td>
                      <td className="px-6 py-4 text-slate-500">
                        {p.latest_assessed_at ? new Date(p.latest_assessed_at).toLocaleDateString() : "Never"}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => setActiveReviewPatient(p)}
                          className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold shadow transition"
                        >
                          Review Case
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="px-6 py-8 text-center text-slate-400">
                      No patients matching criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Review Modal */}
        {activeReviewPatient && (
          <ReviewModal
            assessmentId={activeReviewPatient.patient_id}
            patientName={activeReviewPatient.full_name}
            onClose={() => setActiveReviewPatient(null)}
            onSuccess={() => {
              setActiveReviewPatient(null);
              loadPatients();
            }}
          />
        )}
      </main>
    </div>
  );
}
