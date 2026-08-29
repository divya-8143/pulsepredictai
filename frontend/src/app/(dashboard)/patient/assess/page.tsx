'use client';

import React, { useState } from "react";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { HealthDataForm } from "@/components/assessments/HealthDataForm";
import { RiskScoreCard } from "@/components/assessments/RiskScoreCard";
import { SHAPBreakdown } from "@/components/assessments/SHAPBreakdown";
import { RiskAssessment } from "@/types";
import Link from "next/link";
import { ArrowLeft, RotateCcw } from "lucide-react";

export default function AssessPage() {
  const [result, setResult] = useState<RiskAssessment | null>(null);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 w-full">
        <div className="flex items-center justify-between">
          <Link href="/patient" className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-blue-600 transition">
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Link>
          {result && (
            <button
              onClick={() => setResult(null)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:underline"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Retake Assessment
            </button>
          )}
        </div>

        {!result ? (
          <div className="space-y-4">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Multi-Model AI Health Assessment</h1>
              <p className="text-xs text-slate-500 mt-1">
                Enter your physiological biomarkers below for real-time risk stratification.
              </p>
            </div>
            <HealthDataForm onSuccess={(res) => setResult(res)} />
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Your Health Risk Assessment Result</h1>
              <p className="text-xs text-slate-500 mt-1">
                Generated via Logistic Regression, Random Forest & XGBoost with SHAP attribution.
              </p>
            </div>

            <RiskScoreCard
              score={result.overall_risk_score}
              category={result.risk_category}
              primaryModel={result.primary_model_name}
              recommendations={result.clinical_recommendations}
            />

            <SHAPBreakdown contributions={result.feature_importance_shap} />
          </div>
        )}
      </main>
    </div>
  );
}
