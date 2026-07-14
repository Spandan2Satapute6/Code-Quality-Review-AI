export default function AnalysisCard({ title, icon, score, badgeText, badgeColor = "blue", children }) {
  const badgeColors = {
    blue: "bg-blue-500/15 text-blue-400 border-blue-500/20",
    red: "bg-red-500/15 text-red-400 border-red-500/20",
    green: "bg-green-500/15 text-green-400 border-green-500/20",
    yellow: "bg-amber-500/15 text-amber-400 border-amber-500/20",
    purple: "bg-purple-500/15 text-purple-400 border-purple-500/20",
  };

  const selectedBadgeColor = badgeColors[badgeColor] || badgeColors.blue;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 p-5 gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-slate-950 rounded-lg text-blue-400">
            {icon}
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">{title}</h2>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          {score !== undefined && (
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-slate-400">Score:</span>
              <span className="text-2xl font-black text-white">{score}</span>
            </div>
          )}
          {badgeText && (
            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${selectedBadgeColor}`}>
              {badgeText}
            </span>
          )}
        </div>
      </div>
      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
