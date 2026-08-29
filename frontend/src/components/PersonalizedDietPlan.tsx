"use client";

import React, { useState } from "react";
import { Utensils, Apple, Heart, Flame, ShieldCheck, CheckCircle2, XCircle, Info, ChevronRight, Droplet, Download, Loader2 } from "lucide-react";
import { apiClient } from "@/lib/api";

interface DietPlanProps {
  plan?: {
    primary_dietary_framework: string;
    weight_goal: string;
    daily_target_calories: number;
    macronutrients: {
      carbohydrates: { grams: number; percentage: number };
      protein: { grams: number; percentage: number };
      healthy_fats: { grams: number; percentage: number };
    };
    micronutrient_targets: Record<string, string>;
    daily_meal_plan: {
      breakfast: { title: string; calories: number; items: string[]; clinical_rationale: string };
      morning_snack: { title: string; calories: number; items: string[]; clinical_rationale: string };
      lunch: { title: string; calories: number; items: string[]; clinical_rationale: string };
      afternoon_snack: { title: string; calories: number; items: string[]; clinical_rationale: string };
      dinner: { title: string; calories: number; items: string[]; clinical_rationale: string };
    };
    foods_to_embrace: string[];
    foods_to_restrict: string[];
    lifestyle_habits: string[];
  };
  assessmentId?: string;
}

export default function PersonalizedDietPlan({ plan, assessmentId }: DietPlanProps) {
  const [activeTab, setActiveTab] = useState<"meals" | "macros" | "foods" | "lifestyle">("meals");
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  if (!plan) return null;

  const handleDownloadDietPdf = async () => {
    if (!assessmentId) {
      alert("Assessment ID unavailable for diet PDF download.");
      return;
    }
    setDownloadingPdf(true);
    try {
      const response = await apiClient.get(`/assessments/${assessmentId}/diet-plan/pdf`, {
        responseType: "blob"
      });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `PulsePredict_Diet_Plan_${assessmentId.slice(0, 8)}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to download diet plan PDF", err);
      alert("Failed to download diet plan PDF.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-700 p-6 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-extrabold uppercase tracking-wider bg-white/20 px-2.5 py-1 rounded-full backdrop-blur-sm">
            Cardioprotective Nutrition Protocol
          </span>
          <h2 className="text-xl font-bold mt-2">{plan.primary_dietary_framework}</h2>
          <p className="text-emerald-100 text-xs mt-1">{plan.weight_goal}</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="bg-white/10 backdrop-blur-md p-4 rounded-xl border border-white/20 text-center min-w-[130px]">
            <span className="text-[10px] uppercase font-bold text-emerald-100 block">Daily Target</span>
            <span className="text-2xl font-black text-white">{plan.daily_target_calories}</span>
            <span className="text-[10px] text-emerald-200 block">kcal / day</span>
          </div>

          {assessmentId && (
            <button
              onClick={handleDownloadDietPdf}
              disabled={downloadingPdf}
              className="px-4 py-3 bg-white text-emerald-800 hover:bg-emerald-50 rounded-xl text-xs font-bold shadow-md flex items-center gap-2 transition disabled:opacity-50"
            >
              {downloadingPdf ? <Loader2 className="w-4 h-4 animate-spin text-emerald-600" /> : <Download className="w-4 h-4 text-emerald-600" />}
              Download Diet PDF
            </button>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="px-6">
        <div className="flex border-b border-slate-200 gap-4 text-xs font-semibold">
          {[
            { id: "meals", label: "Daily Meal Blueprint", icon: Utensils },
            { id: "macros", label: "Macronutrient Split", icon: Flame },
            { id: "foods", label: "Foods to Prioritize & Avoid", icon: Apple },
            { id: "lifestyle", label: "Cardio Habits & Hydration", icon: Droplet },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`pb-3 px-1 flex items-center gap-1.5 border-b-2 transition-all ${
                  active
                    ? "border-emerald-600 text-emerald-700 font-bold"
                    : "border-transparent text-slate-500 hover:text-slate-900"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Contents */}
      <div className="px-6 pb-6">
        {activeTab === "meals" && (
          <div className="space-y-4">
            {Object.entries(plan.daily_meal_plan).map(([mealKey, meal]: [string, any]) => (
              <div key={mealKey} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                    {mealKey.replace("_", " ")}
                  </span>
                  <span className="text-xs font-bold text-slate-700 bg-white px-2.5 py-0.5 rounded-full border border-slate-200">
                    ~{meal.calories} kcal
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-900">{meal.title}</h4>
                <ul className="space-y-1 text-xs text-slate-600 pl-2">
                  {meal.items.map((item: string, i: number) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-600 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
                <div className="pt-2 text-[11px] text-slate-500 flex items-start gap-1.5 border-t border-slate-200/60 mt-2">
                  <Info className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                  <span><strong>Clinical Rationale:</strong> {meal.clinical_rationale}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "macros" && (
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-center">
                <span className="text-[10px] font-bold uppercase text-emerald-700">Complex Carbs</span>
                <div className="text-2xl font-black text-emerald-900 mt-1">{plan.macronutrients.carbohydrates.percentage}%</div>
                <span className="text-xs text-emerald-700 font-medium">{plan.macronutrients.carbohydrates.grams}g / day</span>
              </div>

              <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl text-center">
                <span className="text-[10px] font-bold uppercase text-blue-700">Lean Protein</span>
                <div className="text-2xl font-black text-blue-900 mt-1">{plan.macronutrients.protein.percentage}%</div>
                <span className="text-xs text-blue-700 font-medium">{plan.macronutrients.protein.grams}g / day</span>
              </div>

              <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-center">
                <span className="text-[10px] font-bold uppercase text-amber-700">Healthy Unsaturated Fats</span>
                <div className="text-2xl font-black text-amber-900 mt-1">{plan.macronutrients.healthy_fats.percentage}%</div>
                <span className="text-xs text-amber-700 font-medium">{plan.macronutrients.healthy_fats.grams}g / day</span>
              </div>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <h4 className="text-xs font-bold text-slate-800 uppercase">Core Micronutrient & Electrolyte Limits</h4>
              <div className="grid grid-cols-2 gap-3 text-xs">
                {Object.entries(plan.micronutrient_targets).map(([k, v]) => (
                  <div key={k} className="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">{k.replace("_", " ")}</span>
                    <span className="font-semibold text-slate-800">{v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "foods" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-2">
              <h4 className="text-xs font-bold text-emerald-900 flex items-center gap-1.5 uppercase tracking-wider">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Foods to Prioritize Daily
              </h4>
              <ul className="space-y-1.5 text-xs text-emerald-900">
                {plan.foods_to_embrace.map((f, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-4 bg-rose-50/70 border border-rose-200 rounded-xl space-y-2">
              <h4 className="text-xs font-bold text-rose-900 flex items-center gap-1.5 uppercase tracking-wider">
                <XCircle className="w-4 h-4 text-rose-600" />
                Foods to Limit or Avoid
              </h4>
              <ul className="space-y-1.5 text-xs text-rose-900">
                {plan.foods_to_restrict.map((f, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-600"></span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeTab === "lifestyle" && (
          <div className="space-y-3 text-xs">
            <h4 className="font-bold text-slate-800 uppercase tracking-wider">Synergistic Cardiometabolic Lifestyle Habits</h4>
            <div className="space-y-2">
              {plan.lifestyle_habits.map((habit, i) => (
                <div key={i} className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-start gap-2.5 text-slate-700">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                  <span>{habit}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
