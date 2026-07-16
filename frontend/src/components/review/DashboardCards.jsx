import {
  FolderOpen,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Shield,
  Gauge
} from "lucide-react";

function StatCard({ icon, title, value, color }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-500">
            {title}
          </p>

          <h2 className="text-3xl font-black text-white mt-2">
            {value}
          </h2>
        </div>

        <div className={`p-3 rounded-lg ${color}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default function DashboardCards({ dashboard }) {

  if (!dashboard) return null;

  return (

    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-5">

      <StatCard
        title="Overall Score"
        value={dashboard.overall_score}
        color="bg-green-500/10 text-green-400"
        icon={<Gauge size={28} />}
      />

      <StatCard
        title="Files"
        value={dashboard.total_files}
        color="bg-blue-500/10 text-blue-400"
        icon={<FolderOpen size={28} />}
      />

      <StatCard
        title="Passed"
        value={dashboard.passed_files}
        color="bg-emerald-500/10 text-emerald-400"
        icon={<CheckCircle2 size={28} />}
      />

      <StatCard
        title="Failed"
        value={dashboard.failed_files}
        color="bg-red-500/10 text-red-400"
        icon={<XCircle size={28} />}
      />

      <StatCard
        title="AI Issues"
        value={dashboard.total_ai_issues}
        color="bg-yellow-500/10 text-yellow-400"
        icon={<AlertTriangle size={28} />}
      />

      <StatCard
        title="Security"
        value={dashboard.security_issues}
        color="bg-purple-500/10 text-purple-400"
        icon={<Shield size={28} />}
      />

    </div>

  );
}