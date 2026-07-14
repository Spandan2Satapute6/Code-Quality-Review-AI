import { AlertCircle, AlertTriangle, Info, RefreshCw } from "lucide-react";

export default function SeverityBadge({ severity }) {
  const norm = (severity || "").toLowerCase().trim();

  let colorClasses = "bg-slate-800 text-slate-300 border-slate-700";
  let icon = <Info size={14} />;
  let label = severity;

  if (norm === "high" || norm === "error" || norm === "critical") {
    colorClasses = "bg-red-500/10 text-red-400 border-red-500/20";
    icon = <AlertCircle size={14} className="animate-pulse" />;
    label = norm === "high" ? "High Security" : severity;
  } else if (norm === "medium" || norm === "warning") {
    colorClasses = "bg-amber-500/10 text-amber-400 border-amber-500/20";
    icon = <AlertTriangle size={14} />;
    label = norm === "medium" ? "Medium Security" : severity;
  } else if (norm === "low") {
    colorClasses = "bg-blue-500/10 text-blue-400 border-blue-500/20";
    icon = <Info size={14} />;
    label = "Low Security";
  } else if (norm === "convention" || norm === "info") {
    colorClasses = "bg-sky-500/10 text-sky-400 border-sky-500/20";
    icon = <Info size={14} />;
  } else if (norm === "refactor") {
    colorClasses = "bg-purple-500/10 text-purple-400 border-purple-500/20";
    icon = <RefreshCw size={14} />;
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${colorClasses}`}>
      {icon}
      <span className="capitalize">{label}</span>
    </span>
  );
}
