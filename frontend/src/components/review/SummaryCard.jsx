import { CheckCircle2, AlertOctagon, Lightbulb, Trophy, Target } from "lucide-react";


export default function SummaryCard({ summary }) {
  if (!summary) return null;

  const score = summary.overall_score || 0;
  const verdict = summary.verdict || "Under Review";

  const getVerdictStyle = () => {
    const v = verdict.toLowerCase();
    if (v.includes("pass") || v.includes("good") || score >= 80) {
      return "bg-green-500/10 text-green-400 border-green-500/20";
    }
    if (v.includes("fail") || v.includes("need") || score < 50) {
      return "bg-red-500/10 text-red-400 border-red-500/20";
    }
    return "bg-amber-500/10 text-amber-400 border-amber-500/20";
  };

  return (
    <div className="space-y-6">
      {/* Top Banner Verdict */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold text-white tracking-wide">Project Analysis Summary</h2>
            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getVerdictStyle()}`}>
              {verdict}
            </span>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            {summary.summary || "No project summary assessment generated yet."}
          </p>
        </div>
        
        {/* Score Circle */}
        <div className="flex flex-col items-center justify-center bg-slate-950 p-6 rounded-xl border border-slate-800 min-w-[9rem]">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Overall Score</span>
          <span className={`text-5xl font-black mt-2 tracking-tight ${
            score >= 80 ? "text-green-400" :
            score >= 60 ? "text-amber-400" :
            "text-red-400"
          }`}>
            {score}
          </span>
          <span className="text-[10px] text-slate-400 mt-1">out of 100</span>
        </div>
      </div>

      {/* Grid of Strengths, Weaknesses, Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        {summary.strengths && summary.strengths.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2 border-b border-slate-800 pb-3">
              <Trophy size={16} className="text-yellow-400" />
              Key Strengths
            </h3>
            <ul className="space-y-2.5">
              {summary.strengths.map((str, i) => (
                <li key={i} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <CheckCircle2 size={16} className="text-green-400 shrink-0 mt-0.5" />
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {summary.weaknesses && summary.weaknesses.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2 border-b border-slate-800 pb-3">
              <AlertOctagon size={16} className="text-red-400" />
              Areas of Improvement
            </h3>
            <ul className="space-y-2.5">
              {summary.weaknesses.map((weak, i) => (
                <li key={i} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-400 shrink-0 mt-2"></span>
                  <span>{weak}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {summary.recommendations && summary.recommendations.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg md:col-span-2">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2 border-b border-slate-800 pb-3">
              <Lightbulb size={16} className="text-amber-400 animate-pulse" />
              Architectural Recommendations
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {summary.recommendations.map((rec, i) => (
                <div key={i} className="p-3 bg-slate-950 rounded-lg border border-slate-800/60 flex items-start gap-3 text-sm text-slate-300">
                  <Target size={16} className="text-blue-400 shrink-0 mt-0.5" />
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
