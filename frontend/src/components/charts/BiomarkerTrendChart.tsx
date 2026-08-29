import React from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";

interface TrendDataPoint {
  date: string;
  risk_score: number;
  systolic_bp: number;
  fasting_glucose: number;
  total_cholesterol: number;
}

interface BiomarkerTrendChartProps {
  data: TrendDataPoint[];
}

export const BiomarkerTrendChart: React.FC<BiomarkerTrendChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center bg-slate-50 rounded-2xl border border-dashed border-slate-200 text-slate-400 text-xs">
        No longitudinal biomarker records available yet. Complete your first assessment to initialize trend tracking.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
      <div>
        <h3 className="font-bold text-base text-slate-900">Longitudinal Health Trajectory</h3>
        <p className="text-xs text-slate-500">Historical trend lines for blood pressure, glucose, and overall risk score.</p>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#64748b" }} />
            <YAxis tick={{ fontSize: 11, fill: "#64748b" }} />
            <Tooltip
              contentStyle={{ backgroundColor: "#ffffff", borderRadius: "12px", border: "1px solid #e2e8f0", fontSize: "12px" }}
            />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
            <Line type="monotone" dataKey="risk_score" stroke="#ef4444" strokeWidth={2.5} name="Risk Score (0-100)" dot={{ r: 4 }} />
            <Line type="monotone" dataKey="systolic_bp" stroke="#3b82f6" strokeWidth={2} name="Systolic BP (mmHg)" dot={{ r: 3 }} />
            <Line type="monotone" dataKey="fasting_glucose" stroke="#8b5cf6" strokeWidth={2} name="Glucose (mg/dL)" dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
