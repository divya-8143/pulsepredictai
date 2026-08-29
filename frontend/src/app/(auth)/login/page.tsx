'use client';

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiClient } from "@/lib/api";
import { useAuthStore } from "@/lib/auth-store";
import { Activity, Lock, Mail, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  const [email, setEmail] = useState("patient.demo@pulsepredict.ai");
  const [password, setPassword] = useState("Password123!");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await apiClient.post("/auth/login", { email, password });
      const data = res.data;
      setAuth(
        {
          id: data.user_id,
          email: data.email,
          full_name: data.full_name,
          role: data.role,
          is_active: true,
          is_verified: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
        data.access_token,
        data.refresh_token
      );

      if (data.role === "DOCTOR") {
        router.push("/doctor");
      } else if (data.role === "ADMIN") {
        router.push("/admin/models");
      } else {
        router.push("/patient");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Authentication failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const fillCredentials = (role: "PATIENT" | "DOCTOR" | "ADMIN") => {
    if (role === "PATIENT") {
      setEmail("patient.demo@pulsepredict.ai");
      setPassword("Password123!");
    } else if (role === "DOCTOR") {
      setEmail("doctor.demo@pulsepredict.ai");
      setPassword("Password123!");
    } else {
      setEmail("admin@pulsepredict.ai");
      setPassword("Password123!");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link href="/" className="inline-flex items-center gap-2.5">
          <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md">
            <Activity className="w-7 h-7" />
          </div>
        </Link>
        <h2 className="mt-4 text-3xl font-extrabold text-slate-900">Sign in to PulsePredict AI</h2>
        <p className="mt-2 text-xs text-slate-500">Access your health risk assessments and clinical records</p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-md rounded-2xl border border-slate-200 sm:px-10 space-y-6">
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700">Email Address</label>
              <div className="mt-1 relative">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3 py-2 pl-9 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="name@example.com"
                />
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Password</label>
              <div className="mt-1 relative">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 pl-9 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="••••••••"
                />
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow transition disabled:opacity-50 text-sm"
            >
              {loading ? "Authenticating..." : "Sign In"}
            </button>
          </form>

          {/* Quick Demo Logins */}
          <div className="pt-4 border-t border-slate-200 space-y-2">
            <span className="block text-[11px] font-bold text-slate-400 uppercase text-center">Quick Demo Credentials</span>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => fillCredentials("PATIENT")}
                className="px-2 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-semibold rounded-lg transition"
              >
                Patient
              </button>
              <button
                type="button"
                onClick={() => fillCredentials("DOCTOR")}
                className="px-2 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs font-semibold rounded-lg transition"
              >
                Doctor
              </button>
              <button
                type="button"
                onClick={() => fillCredentials("ADMIN")}
                className="px-2 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold rounded-lg transition"
              >
                Admin
              </button>
            </div>
          </div>

          <div className="text-center">
            <Link href="/register" className="text-xs text-blue-600 hover:underline">
              Don't have an account? Register here
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
