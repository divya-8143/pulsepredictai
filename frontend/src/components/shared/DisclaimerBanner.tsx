import React, { useState } from "react";
import { ShieldAlert, X } from "lucide-react";

export const DisclaimerBanner: React.FC = () => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5 text-xs text-amber-900 flex items-center justify-between">
      <div className="flex items-center gap-2 max-w-5xl mx-auto">
        <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0" />
        <span>
          <strong>Clinical Risk Monitoring Notice:</strong> PulsePredict AI provides multi-model predictive risk estimation for research, preventive health tracking, and clinical decision support. Predictions do <strong>NOT</strong> constitute a formal medical diagnosis. Always consult a licensed physician for healthcare decisions.
        </span>
      </div>
      <button 
        onClick={() => setDismissed(true)} 
        className="text-amber-700 hover:text-amber-950 p-1 rounded-md transition"
        aria-label="Dismiss disclaimer"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
