'use client';

import React, { useEffect, useState } from "react";
import { Navbar } from "@/components/shared/Navbar";
import { DisclaimerBanner } from "@/components/shared/DisclaimerBanner";
import { apiClient } from "@/lib/api";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import { Brain, Cpu, BarChart2, CheckCircle2 } from "lucide-react";

export default function ModelPerformanceDashboard() {
  const [selectedModel, setSelectedModel] = useState("CalibratedEnsemble");
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const modelOptions = [
    { id: "CalibratedEnsemble", name: "Calibrated Ensemble (LR + RF + XGBoost)", type: "Production Primary" },
    { id: "XGBoost", name: "XGBoost Classifier (Optuna Tuned)", type: "Gradient Boosted Trees" },
    { id: "RandomForest", name: "Random Forest Classifier", type: "Bagging Ensemble" },
    { id: "LogisticRegression", name: "Logistic Regression (Regularized)", type: "Linear Odds Baseline" },
  ];

  useEffect(() => {
    loadModelMetrics(selectedModel);
  }, [selectedModel]);

  const loadModelMetrics = async (modelName: string) => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/ml/models/${modelName}/metrics`);
      setMetrics(res.data);
    } catch (e) {
      console.error("Failed to load model metrics", e);
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
            <span className="px-2.5 py-0.5 rounded-md bg-blue-100 text-blue-700 font-mono text-[11px] font-bold">MODEL REGISTRY & PERFORMANCE</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Machine Learning Evaluation Dashboard</h1>
          <p className="text-xs text-slate-500 mt-1">
            Compare multi-class accuracy, precision, recall, F1, ROC-AUC, and confusion matrices across registered models.
          </p>
        </div>

        {/* Model Selector Tabs */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          {modelOptions.map((opt) => (
            <button
              key={opt.id}
              onClick={() => setSelectedModel(opt.id)}
              className={`p-4 rounded-xl border text-left transition shadow-sm ${
                selectedModel === opt.id
                  ? "bg-white border-blue-600 ring-2 ring-blue-500/20"
                  : "bg-white/60 border-slate-200 hover:bg-white"
              }`}
            >
              <span className="block text-xs font-bold text-slate-900">{opt.name}</span>
              <span className="block text-[11px] text-slate-400 mt-1">{opt.type}</span>
            </button>
          ))}
        </div>

        {/* Performance Metric Scorecards */}
        {metrics && (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
              <span className="text-[11px] font-bold text-slate-400 uppercase">Accuracy</span>
              <p className="text-2xl font-extrabold text-blue-600 mt-1">{(metrics.accuracy * 100).toFixed(2)}%</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
              <span className="text-[11px] font-bold text-slate-400 uppercase">Precision (W)</span>
              <p className="text-2xl font-extrabold text-indigo-600 mt-1">{(metrics.precision * 100).toFixed(2)}%</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
              <span className="text-[11px] font-bold text-slate-400 uppercase">Recall (W)</span>
              <p className="text-2xl font-extrabold text-purple-600 mt-1">{(metrics.recall * 100).toFixed(2)}%</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
              <span className="text-[11px] font-bold text-slate-400 uppercase">F1-Score</span>
              <p className="text-2xl font-extrabold text-emerald-600 mt-1">{(metrics.f1_score * 100).toFixed(2)}%</p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center col-span-2 sm:col-span-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase">ROC-AUC OvR</span>
              <p className="text-2xl font-extrabold text-amber-600 mt-1">{metrics.roc_auc.toFixed(4)}</p>
            </div>
          </div>
        )}

        {/* Charts & Confusion Matrix */}
        {metrics && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* ROC Curve Chart */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div>
                <h3 className="font-bold text-base text-slate-900">Multi-Class ROC Curve (OvR)</h3>
                <p className="text-xs text-slate-500">True Positive Rate vs False Positive Rate per risk category.</p>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="fpr" type="number" domain={[0, 1]} tick={{ fontSize: 11 }} label={{ value: "False Positive Rate", position: "insideBottom", offset: -5, fontSize: 10 }} />
                    <YAxis dataKey="tpr" type="number" domain={[0, 1]} tick={{ fontSize: 11 }} label={{ value: "True Positive Rate", angle: -90, position: "insideLeft", fontSize: 10 }} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
                    <Line data={metrics.roc_curve["LOW"]} dataKey="tpr" stroke="#10b981" strokeWidth={2} name="Low Risk" dot={false} />
                    <Line data={metrics.roc_curve["MODERATE"]} dataKey="tpr" stroke="#f59e0b" strokeWidth={2} name="Moderate" dot={false} />
                    <Line data={metrics.roc_curve["HIGH"]} dataKey="tpr" stroke="#f97316" strokeWidth={2} name="High" dot={false} />
                    <Line data={metrics.roc_curve["CRITICAL"]} dataKey="tpr" stroke="#ef4444" strokeWidth={2} name="Critical" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Confusion Matrix Heatmap Table */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div>
                <h3 className="font-bold text-base text-slate-900">Confusion Matrix (Validation Split)</h3>
                <p className="text-xs text-slate-500">Actual vs Predicted clinical class assignments across 2,400 test cases.</p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-center text-xs border border-slate-200">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="p-2 border border-slate-200 text-slate-400">Actual \ Pred</th>
                      {metrics.class_labels.map((cl: string) => (
                        <th key={cl} className="p-2 border border-slate-200 font-bold text-slate-700">{cl}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {metrics.confusion_matrix.map((row: number[], rowIdx: number) => (
                      <tr key={rowIdx}>
                        <td className="p-2 border border-slate-200 font-bold bg-slate-50 text-slate-700">
                          {metrics.class_labels[rowIdx]}
                        </td>
                        {row.map((val: number, colIdx: number) => (
                          <td
                            key={colIdx}
                            className={`p-3 border border-slate-200 font-mono font-bold ${
                              rowIdx === colIdx ? "bg-blue-50 text-blue-800" : "text-slate-400"
                            }`}
                          >
                            {val}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
