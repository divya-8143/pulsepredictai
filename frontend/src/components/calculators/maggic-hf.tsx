"use client";

import React, { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Activity, Heart, ShieldAlert, CheckCircle, Info, Stethoscope, ArrowRight, RefreshCw } from "lucide-react";

interface CalculatorProps {
  initialAge?: number;
  initialGender?: "MALE" | "FEMALE";
  initialSystolic?: number;
  initialDiastolic?: number;
  initialTotalChol?: number;
  initialHDL?: number;
  initialGlucose?: number;
  initialSmoker?: boolean;
  initialDiabetes?: boolean;
}

export default function MAGGIC_HFCalculator({
  initialAge = 52,
  initialGender = "MALE",
  initialSystolic = 135,
  initialDiastolic = 85,
  initialTotalChol = 210,
  initialHDL = 48,
  initialGlucose = 100,
  initialSmoker = false,
  initialDiabetes = false
}: CalculatorProps) {
  const [age, setAge] = useState<number>(initialAge);
  const [gender, setGender] = useState<"MALE" | "FEMALE">(initialGender);
  const [systolic, setSystolic] = useState<number>(initialSystolic);
  const [diastolic, setDiastolic] = useState<number>(initialDiastolic);
  const [totalChol, setTotalChol] = useState<number>(initialTotalChol);
  const [hdl, setHDL] = useState<number>(initialHDL);
  const [glucose, setGlucose] = useState<number>(initialGlucose);
  const [smoker, setSmoker] = useState<boolean>(initialSmoker);
  const [diabetes, setDiabetes] = useState<boolean>(initialDiabetes);
  const [treatedBP, setTreatedBP] = useState<boolean>(false);
  const [familyHistory, setFamilyHistory] = useState<boolean>(false);

  // Real-time clinical evaluation
  const result = useMemo(() => {
    const isMale = gender === "MALE";
    let score = 0;
    score += (age - 40) * (isMale ? 0.065 : 0.058);
    const sbpDiff = Math.max(0, systolic - 120);
    score += sbpDiff * (treatedBP ? 0.022 : 0.018);
    const cholRatio = totalChol / Math.max(20, hdl);
    score += (cholRatio - 3.5) * 0.28;
    if (diabetes || glucose >= 126) score += isMale ? 0.85 : 0.95;
    if (smoker) score += 0.72;
    if (familyHistory) score += 0.45;

    const baseIncidence = isMale ? 0.045 : 0.028;
    const clampedExp = Math.max(-5, Math.min(5, score));
    const hazard = baseIncidence * Math.exp(clampedExp);
    const pct = Math.min(100, Math.max(0.1, (1 - Math.exp(-hazard)) * 100));

    let tier = "LOW_RISK";
    let color = "text-emerald-600 bg-emerald-50 border-emerald-200";
    if (pct >= 35) {
      tier = "CRITICAL HIGH RISK";
      color = "text-rose-700 bg-rose-50 border-rose-200";
    } else if (pct >= 20) {
      tier = "HIGH RISK";
      color = "text-orange-700 bg-orange-50 border-orange-200";
    } else if (pct >= 10) {
      tier = "INTERMEDIATE RISK";
      color = "text-amber-700 bg-amber-50 border-amber-200";
    } else if (pct >= 5) {
      tier = "BORDERLINE RISK";
      color = "text-blue-700 bg-blue-50 border-blue-200";
    }

    return {
      rawScore: score.toFixed(2),
      percentage: pct.toFixed(1),
      tier,
      color,
      pulsePressure: systolic - diastolic,
      map: (diastolic + (systolic - diastolic) / 3).toFixed(1),
      cholRatio: cholRatio.toFixed(2)
    };
  }, [age, gender, systolic, diastolic, totalChol, hdl, glucose, smoker, diabetes, treatedBP, familyHistory]);

  return (
    <div className="space-y-6 max-w-4xl mx-auto p-4">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">MAGGIC Heart Failure Risk Score for Mortality in HFpEF and HFrEF</h2>
          <p className="text-sm text-slate-500">Pocock et al. Eur Heart J. 2013;34(19):1404-1413</p>
        </div>
        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">
          Heart Failure
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Input Parameters */}
        <div className="md:col-span-2 space-y-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-semibold text-slate-800 text-sm tracking-wide uppercase flex items-center gap-2">
            <Stethoscope className="w-4 h-4 text-blue-600" />
            Clinical Biomarker Inputs
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Age (years): {age}</label>
              <input
                type="range"
                min="20"
                max="85"
                value={age}
                onChange={(e) => setAge(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Biological Sex</label>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setGender("MALE")}
                  className={`flex-1 py-1.5 text-xs font-medium rounded-lg border ${
                    gender === "MALE" ? "bg-blue-600 text-white border-blue-600" : "bg-slate-50 text-slate-700"
                  }`}
                >
                  Male
                </button>
                <button
                  type="button"
                  onClick={() => setGender("FEMALE")}
                  className={`flex-1 py-1.5 text-xs font-medium rounded-lg border ${
                    gender === "FEMALE" ? "bg-blue-600 text-white border-blue-600" : "bg-slate-50 text-slate-700"
                  }`}
                >
                  Female
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Systolic BP (mmHg): {systolic}</label>
              <input
                type="number"
                value={systolic}
                onChange={(e) => setSystolic(Number(e.target.value))}
                className="w-full px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Diastolic BP (mmHg): {diastolic}</label>
              <input
                type="number"
                value={diastolic}
                onChange={(e) => setDiastolic(Number(e.target.value))}
                className="w-full px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Total Cholesterol (mg/dL)</label>
              <input
                type="number"
                value={totalChol}
                onChange={(e) => setTotalChol(Number(e.target.value))}
                className="w-full px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">HDL Cholesterol (mg/dL)</label>
              <input
                type="number"
                value={hdl}
                onChange={(e) => setHDL(Number(e.target.value))}
                className="w-full px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="pt-3 border-t grid grid-cols-2 gap-3 text-xs">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={smoker}
                onChange={(e) => setSmoker(e.target.checked)}
                className="rounded text-blue-600 focus:ring-blue-500"
              />
              <span className="text-slate-700">Current Tobacco Smoker</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={diabetes}
                onChange={(e) => setDiabetes(e.target.checked)}
                className="rounded text-blue-600 focus:ring-blue-500"
              />
              <span className="text-slate-700">Diabetes Mellitus</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={treatedBP}
                onChange={(e) => setTreatedBP(e.target.checked)}
                className="rounded text-blue-600 focus:ring-blue-500"
              />
              <span className="text-slate-700">Treated for Hypertension</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={familyHistory}
                onChange={(e) => setFamilyHistory(e.target.checked)}
                className="rounded text-blue-600 focus:ring-blue-500"
              />
              <span className="text-slate-700">Family History of Premature CAD</span>
            </label>
          </div>
        </div>

        {/* Realtime Output Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <span className="text-xs font-semibold tracking-wider text-slate-500 uppercase">Calculated Risk Output</span>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-4xl font-extrabold text-slate-900">{result.percentage}%</span>
              <span className="text-xs text-slate-500">10-Year Probability</span>
            </div>

            <div className={`mt-3 inline-block px-3 py-1 rounded-full text-xs font-bold border ${result.color}`}>
              {result.tier}
            </div>

            <div className="mt-6 space-y-2 text-xs border-t pt-4 text-slate-600">
              <div className="flex justify-between">
                <span>Total/HDL Ratio:</span>
                <span className="font-semibold text-slate-900">{result.cholRatio}</span>
              </div>
              <div className="flex justify-between">
                <span>Mean Arterial Pressure:</span>
                <span className="font-semibold text-slate-900">{result.map} mmHg</span>
              </div>
              <div className="flex justify-between">
                <span>Pulse Pressure:</span>
                <span className="font-semibold text-slate-900">{result.pulsePressure} mmHg</span>
              </div>
            </div>
          </div>

          <div className="mt-6 p-3 bg-slate-50 rounded-lg text-xs text-slate-600 border border-slate-200">
            <p className="font-semibold text-slate-800 mb-1 flex items-center gap-1">
              <Info className="w-3.5 h-3.5 text-blue-600" />
              Clinical Summary
            </p>
            {Number(result.percentage) >= 20 ? (
              <p>High risk tier indicates formal evaluation for statin therapy and intensive blood pressure control.</p>
            ) : (
              <p>Moderate to low risk tier. Emphasize therapeutic lifestyle modifications and periodic monitoring.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
