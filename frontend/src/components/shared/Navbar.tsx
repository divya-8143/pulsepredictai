import React from "react";
import Link from "next/link";
import { useAuthStore } from "@/lib/auth-store";
import { Activity, User as UserIcon, LogOut, ShieldCheck, Stethoscope } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <span className="font-bold text-lg text-slate-900 tracking-tight">PulsePredict <span className="text-blue-600">AI</span></span>
            <span className="block text-[10px] uppercase font-semibold text-slate-400 -mt-1 tracking-wider">Clinical Risk Engine</span>
          </div>
        </Link>

        <nav className="flex items-center gap-6">
          {isAuthenticated && user ? (
            <>
              {user.role === "PATIENT" && (
                <div className="flex items-center gap-4 text-sm font-medium">
                  <Link href="/patient" className="text-slate-600 hover:text-blue-600 transition">Dashboard</Link>
                  <Link href="/patient/assess" className="text-slate-600 hover:text-blue-600 transition">New Assessment</Link>
                  <Link href="/patient/history" className="text-slate-600 hover:text-blue-600 transition">History</Link>
                </div>
              )}

              {user.role === "DOCTOR" && (
                <div className="flex items-center gap-4 text-sm font-medium">
                  <Link href="/doctor" className="text-slate-600 hover:text-blue-600 transition">Doctor Dashboard</Link>
                  <Link href="/doctor/patients" className="text-slate-600 hover:text-blue-600 transition">Patient Roster</Link>
                  <Link href="/admin/models" className="text-slate-600 hover:text-blue-600 transition">ML Models</Link>
                </div>
              )}

              {user.role === "ADMIN" && (
                <div className="flex items-center gap-4 text-sm font-medium">
                  <Link href="/admin/analytics" className="text-slate-600 hover:text-blue-600 transition">Analytics</Link>
                  <Link href="/admin/models" className="text-slate-600 hover:text-blue-600 transition">ML Registry</Link>
                  <Link href="/admin/audit" className="text-slate-600 hover:text-blue-600 transition">Audit Logs</Link>
                </div>
              )}

              <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
                <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold ${
                  user.role === "DOCTOR" ? "bg-purple-100 text-purple-700" :
                  user.role === "ADMIN" ? "bg-amber-100 text-amber-800" :
                  "bg-blue-100 text-blue-700"
                }`}>
                  {user.role === "DOCTOR" ? <Stethoscope className="w-3 h-3" /> : <ShieldCheck className="w-3 h-3" />}
                  {user.role}
                </span>

                <span className="text-sm font-medium text-slate-700">{user.full_name}</span>

                <button
                  onClick={logout}
                  className="p-2 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-slate-100 transition"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-3">
              <Link href="/login" className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-blue-600 transition">
                Sign In
              </Link>
              <Link href="/register" className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow transition">
                Register
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};
