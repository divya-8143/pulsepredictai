'use client';

import React from "react";
import Link from "next/link";
import { Activity, ShieldCheck, HeartPulse, Brain, BarChart3, Stethoscope, ChevronRight } from "lucide-react";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { Navbar } from "@/components/shared/Navbar";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <DisclaimerBanner />
      <Navbar />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-16 pb-24 lg:pt-28 lg:pb-36 bg-gradient-to-b from-white to-slate-50 border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
              <Brain className="w-4 h-4 text-blue-600" />
              <span>Multi-Model AI (Logistic Regression, Random Forest, XGBoost)</span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight">
              Predictive Clinical Health Risk Intelligence for <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Proactive Healthcare</span>
            </h1>

            <p className="text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
              Integrate multidimensional vitals, lipid profiles, and metabolic biomarkers to compute calibrated risk assessments with explainable SHAP feature attribution and physician collaboration.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                href="/register"
                className="w-full sm:w-auto px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/25 transition flex items-center justify-center gap-2"
              >
                <span>Get Started as Patient</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-8 py-3.5 bg-white hover:bg-slate-100 text-slate-800 font-semibold rounded-xl border border-slate-300 shadow-sm transition"
              >
                Sign In to Dashboard
              </Link>
            </div>
          </div>
        </section>

        {/* Feature Cards Grid */}
        <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
            <h2 className="text-3xl font-bold text-slate-900">Enterprise AI Health Architecture</h2>
            <p className="text-slate-600 text-sm">
              Engineered with rigorous mathematical validation, low-latency inference, and HIPAA-ready role access.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center">
                <HeartPulse className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Multi-Model Ensemble</h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                Evaluates patient vitals across Regularized Logistic Regression, Random Forest, and XGBoost with soft-voting probability aggregation.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div className="w-12 h-12 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center">
                <Brain className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">SHAP Explainability</h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                Clear feature attribution showing how each biomarker (blood pressure, glucose, lipids) drives risk elevation or protection.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div className="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center">
                <Stethoscope className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Physician Review Flow</h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                Dedicated doctor dashboards for clinical annotation, risk tier filtering (Low to Critical), and automated PDF clinical summaries.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-white border-t border-slate-200 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-xs text-slate-500 space-y-2">
          <p>© 2026 PulsePredict AI Platform. All rights reserved.</p>
          <p>For preventive health risk estimation & research monitoring only. Not a medical diagnosis.</p>
        </div>
      </footer>
    </div>
  );
}
