import { useState } from "react";
import SeverityBadge from "./SeverityBadge";
import { ChevronDown, ChevronUp, FileCode, CheckCircle, AlertTriangle, ShieldAlert } from "lucide-react";

export default function FileCard({ file }) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Parsing helper for Radon
  const parseRadon = () => {
    if (!file.radon || !file.radon.success) {
      return {
        cc: [],
        mi: { mi: 100, rank: "A" },
        raw: { loc: 0, lloc: 0, sloc: 0, comments: 0, multi: 0, blank: 0 }
      };
    }
    
    let cc = [];
    try {
      const ccObj = typeof file.radon.complexity === "string" ? JSON.parse(file.radon.complexity) : file.radon.complexity;
      cc = Object.values(ccObj)[0] || [];
    } catch (e) {}

    let mi = { mi: 100, rank: "A" };
    try {
      const miObj = typeof file.radon.maintainability === "string" ? JSON.parse(file.radon.maintainability) : file.radon.maintainability;
      mi = Object.values(miObj)[0] || { mi: 100, rank: "A" };
    } catch (e) {}

    let raw = { loc: 0, lloc: 0, sloc: 0, comments: 0, multi: 0, blank: 0 };
    try {
      const rawObj = typeof file.radon.raw_metrics === "string" ? JSON.parse(file.radon.raw_metrics) : file.radon.raw_metrics;
      raw = Object.values(rawObj)[0] || { loc: 0, lloc: 0, sloc: 0, comments: 0, multi: 0, blank: 0 };
    } catch (e) {}

    return { cc, mi, raw };
  };

  const { cc, mi, raw } = parseRadon();

  // Parse Pylint issues
  const pylintIssues = file.pylint?.success ? file.pylint.issues || [] : [];
  const errors = pylintIssues.filter(i => i.type === "error").length;
  const warnings = pylintIssues.filter(i => i.type === "warning").length;
  const refactors = pylintIssues.filter(i => i.type === "refactor").length;
  const conventions = pylintIssues.filter(i => i.type === "convention").length;

  // Calculate pylint score
  const pylintScore = Math.max(0, 10.0 - (errors * 2.0 + warnings * 1.0 + refactors * 0.5 + conventions * 0.2));

  // Parse Bandit issues
  const banditIssues = file.bandit?.success ? file.bandit.report?.results || [] : [];
  const highSec = banditIssues.filter(i => i.issue_severity === "HIGH").length;
  const medSec = banditIssues.filter(i => i.issue_severity === "MEDIUM").length;
  const lowSec = banditIssues.filter(i => i.issue_severity === "LOW").length;

  // Quality Score (0-100)
  const qualityScore = Math.round((pylintScore * 10 + mi.mi) / 2);

  // Security status
  let securityStatus = "Safe";
  let securityColor = "text-green-400 bg-green-500/10 border-green-500/20";
  let SecurityIcon = CheckCircle;

  if (highSec > 0) {
    securityStatus = "Vulnerable";
    securityColor = "text-red-400 bg-red-500/10 border-red-500/20";
    SecurityIcon = ShieldAlert;
  } else if (medSec > 0 || lowSec > 0) {
    securityStatus = "Warning";
    securityColor = "text-amber-400 bg-amber-500/10 border-amber-500/20";
    SecurityIcon = AlertTriangle;
  }

  // CC complexity level
  const maxCC = cc.length > 0 ? Math.max(...cc.map(c => c.complexity)) : 1;
  let ccLevel = "Low";
  let ccColor = "text-green-400";
  if (maxCC > 20) {
    ccLevel = "High";
    ccColor = "text-red-400";
  } else if (maxCC > 10) {
    ccLevel = "Medium";
    ccColor = "text-amber-400";
  }

  const totalIssues = pylintIssues.length + banditIssues.length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg transition-all duration-200 hover:border-slate-700">
      {/* File Card Header Summary */}
      <div className="p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-5 bg-slate-900">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-slate-950 rounded-lg text-blue-400">
            <FileCode size={24} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white font-mono">{file.filename}</h3>
            <p className="text-xs text-slate-400 font-mono mt-0.5">{file.path}</p>
          </div>
        </div>

        {/* Metrics Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:flex lg:items-center gap-4 lg:gap-8">
          {/* Quality Score */}
          <div className="flex items-center gap-2.5">
            <div className={`relative flex items-center justify-center w-12 h-12 rounded-full border-2 ${
              qualityScore >= 80 ? "border-green-500 text-green-400" :
              qualityScore >= 50 ? "border-amber-500 text-amber-400" :
              "border-red-500 text-red-400"
            } bg-slate-950 font-black text-sm`}>
              {qualityScore}
            </div>
            <div>
              <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Quality Score</p>
              <p className="text-xs font-bold text-slate-300">Scale 0-100</p>
            </div>
          </div>

          {/* Security Status */}
          <div>
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">Security Status</p>
            <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded border text-xs font-semibold ${securityColor}`}>
              <SecurityIcon size={12} />
              {securityStatus}
            </span>
          </div>

          {/* Radon Complexity & Maintainability */}
          <div>
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Complexity</p>
            <p className="text-sm font-bold text-slate-300 mt-0.5">
              Max CC: <span className={ccColor}>{maxCC} ({ccLevel})</span>
            </p>
          </div>

          <div>
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Maintainability</p>
            <p className="text-sm font-bold text-slate-300 mt-0.5">
              MI: <span className={mi.mi >= 50 ? "text-green-400" : "text-amber-400"}>{mi.mi.toFixed(1)} ({mi.rank})</span>
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between lg:justify-end gap-4 border-t border-slate-800 lg:border-none pt-4 lg:pt-0">
          <div className="text-left lg:text-right">
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Issues Count</p>
            <p className="text-sm font-bold text-white mt-0.5">
              {totalIssues > 0 ? (
                <span className="text-amber-400">{totalIssues} Issues</span>
              ) : (
                <span className="text-green-400">Clean</span>
              )}
            </p>
          </div>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 px-3 py-2 rounded-lg text-xs font-semibold text-slate-300 transition-all duration-200"
          >
            {isExpanded ? (
              <>
                Hide Details <ChevronUp size={14} />
              </>
            ) : (
              <>
                Expand Details <ChevronDown size={14} />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Expandable Details Area */}
      {isExpanded && (
        <div className="border-t border-slate-800 bg-slate-950/60 p-5 space-y-6">
          {/* Radon Raw metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 bg-slate-900/40 p-4 rounded-xl border border-slate-800/60">
            <div>
              <p className="text-xs text-slate-500">Lines of Code</p>
              <p className="text-base font-extrabold text-white mt-0.5">{raw.loc}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Source Lines (SLOC)</p>
              <p className="text-base font-extrabold text-white mt-0.5">{raw.sloc}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Logical Lines (LLOC)</p>
              <p className="text-base font-extrabold text-white mt-0.5">{raw.lloc}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Comment Lines</p>
              <p className="text-base font-extrabold text-emerald-400 mt-0.5">{raw.comments}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Blank Lines</p>
              <p className="text-base font-extrabold text-slate-400 mt-0.5">{raw.blank}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Docstring Lines</p>
              <p className="text-base font-extrabold text-purple-400 mt-0.5">{raw.multi}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            {/* Pylint Findings */}
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-slate-300 border-b border-slate-800 pb-2 flex items-center justify-between">
                <span>Pylint Code Standards Check</span>
                <span className="text-xs text-slate-500">{pylintIssues.length} issues</span>
              </h4>
              {pylintIssues.length > 0 ? (
                <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
                  {pylintIssues.map((issue, idx) => (
                    <div key={idx} className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 flex items-start justify-between gap-3 text-xs">
                      <div className="space-y-1">
                        <div className="font-semibold text-white">{issue.message}</div>
                        <div className="font-mono text-slate-500">
                          Line {issue.line}:{issue.column} | Rule: {issue.symbol} ({issue["message-id"]})
                        </div>
                      </div>
                      <SeverityBadge severity={issue.type} />
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic py-4">No code quality issues found by Pylint!</p>
              )}
            </div>

            {/* Bandit Security Findings */}
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-slate-300 border-b border-slate-800 pb-2 flex items-center justify-between">
                <span>Bandit Security Scanner</span>
                <span className="text-xs text-slate-500">{banditIssues.length} findings</span>
              </h4>
              {banditIssues.length > 0 ? (
                <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
                  {banditIssues.map((issue, idx) => (
                    <div key={idx} className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 space-y-2 text-xs">
                      <div className="flex items-start justify-between gap-3">
                        <div className="space-y-1">
                          <div className="font-semibold text-white">{issue.issue_text}</div>
                          <div className="font-mono text-slate-500">
                            Line {issue.line_number} | Rule: {issue.test_id} ({issue.test_name})
                          </div>
                        </div>
                        <SeverityBadge severity={issue.issue_severity} />
                      </div>
                      {issue.code && (
                        <pre className="p-2 bg-slate-950 border border-slate-800 rounded font-mono text-[10px] text-emerald-400 overflow-x-auto whitespace-pre">
                          <code>{issue.code}</code>
                        </pre>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic py-4">No security vulnerabilities found by Bandit!</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
