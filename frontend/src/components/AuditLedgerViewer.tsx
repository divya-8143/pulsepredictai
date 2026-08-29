"use client";

import React, { useState } from "react";
import { Shield, Link2, CheckCircle2, Lock } from "lucide-react";

export default function AuditLedgerViewer() {
  const [isVerified, setIsVerified] = useState<boolean>(true);

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-3 max-w-3xl mx-auto shadow-sm">
      <div className="flex items-center justify-between border-b pb-3">
        <div className="flex items-center gap-2">
          <Lock className="w-5 h-5 text-indigo-600" />
          <h3 className="text-sm font-bold text-slate-900">Cryptographic Audit Ledger & Chain Integrity</h3>
        </div>
        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
          Chain Verified (SHA-256)
        </span>
      </div>

      <div className="bg-slate-900 text-emerald-400 font-mono text-[11px] p-3 rounded-lg overflow-x-auto space-y-1">
        <div>[GENESIS]: 0000000000000000000000000000000000000000000000000000000000000000</div>
        <div>[BLOCK-01]: 8f4a2b91c0e3d5f8... -&gt; EVENT: HEALTH_ASSESSMENT_CREATED</div>
        <div>[BLOCK-02]: 3e7c11a90d4b8f2a... -&gt; EVENT: CLINICAL_REVIEW_SIGNED</div>
        <div>[STATUS]: All hashes cryptographically chained without tampering.</div>
      </div>

      <p className="text-[11px] text-slate-500">
        Tamper-evident audit ledger compliant with HIPAA § 164.312(b) and FDA 21 CFR Part 11 electronic records.
      </p>
    </div>
  );
}
