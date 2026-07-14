export default function MetricCard({ title, value, icon, description, color = "blue" }) {
  const colorMap = {
    blue: "from-blue-600/10 to-blue-500/5 text-blue-400 border-blue-500/10",
    red: "from-red-600/10 to-red-500/5 text-red-400 border-red-500/10",
    green: "from-green-600/10 to-green-500/5 text-green-400 border-green-500/10",
    purple: "from-purple-600/10 to-purple-500/5 text-purple-400 border-purple-500/10",
    orange: "from-orange-600/10 to-orange-500/5 text-orange-400 border-orange-500/10",
    yellow: "from-amber-600/10 to-amber-500/5 text-amber-400 border-amber-500/10",
  };

  const selectedColor = colorMap[color] || colorMap.blue;

  return (
    <div className={`relative overflow-hidden bg-gradient-to-br ${selectedColor} border rounded-xl p-5 shadow-lg`}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">{title}</p>
          <p className="text-3xl font-extrabold mt-2 tracking-tight text-white">{value}</p>
        </div>
        <div className="p-2.5 bg-slate-950/40 rounded-lg text-current">
          {icon}
        </div>
      </div>
      {description && (
        <p className="text-xs text-slate-400 mt-2">{description}</p>
      )}
    </div>
  );
}
