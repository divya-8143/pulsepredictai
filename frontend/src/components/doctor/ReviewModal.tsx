import React, { useState } from "react";
import { apiClient } from "@/lib/api";
import { X, CheckCircle2, AlertCircle } from "lucide-react";

interface ReviewModalProps {
  assessmentId: string;
  patientName: string;
  onClose: () => void;
  onSuccess: () => void;
}

export const ReviewModal: React.FC<ReviewModalProps> = ({
  assessmentId,
  patientName,
  onClose,
  onSuccess,
}) => {
  const [clinicalNotes, setClinicalNotes] = useState("");
  const [recommendation, setRecommendation] = useState("CLINICAL_FOLLOWUP");
  const [requiresFollowup, setRequiresFollowup] = useState(true);
  const [followUpDate, setFollowUpDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await apiClient.post("/doctor/reviews", {
        assessment_id: assessmentId,
        clinical_notes: clinicalNotes,
        recommendation: recommendation,
        requires_followup: requiresFollowup,
        follow_up_date: followUpDate || null,
      });
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to submit clinical review.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg w-full p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">Physician Clinical Review</h3>
            <p className="text-xs text-slate-500">Patient: {patientName}</p>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-700 rounded-lg">
            <X className="w-4 h-4" />
          </button>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700">Clinical Evaluation & Notes</label>
            <textarea
              required
              rows={4}
              value={clinicalNotes}
              onChange={(e) => setClinicalNotes(e.target.value)}
              className="mt-1 w-full p-3 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-purple-500 focus:outline-none"
              placeholder="Document clinical diagnosis correlation, risk findings, and prescription directives..."
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700">Clinical Recommendation</label>
              <select
                value={recommendation}
                onChange={(e) => setRecommendation(e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-purple-500 focus:outline-none"
              >
                <option value="LIFESTYLE_MOD">Lifestyle Modification</option>
                <option value="CLINICAL_FOLLOWUP">Specialist Consultation / Follow-Up</option>
                <option value="URGENT_CARE">Urgent Care Escalation</option>
                <option value="NO_ACTION">No Immediate Action Required</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Recommended Follow-up Date</label>
              <input
                type="date"
                value={followUpDate}
                onChange={(e) => setFollowUpDate(e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-purple-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-bold transition shadow disabled:opacity-50"
            >
              {loading ? "Submitting..." : "Sign & Submit Review"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
