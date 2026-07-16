import { useState, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  ShieldCheck,
  Binary,
  FolderOpen,
  FileSpreadsheet,
  AlertTriangle,
  FileCode,
  ArrowLeft,
  Settings,
  HelpCircle,
  Code
} from "lucide-react";
import MetricCard from "../../components/review/MetricCard";
import AnalysisCard from "../../components/review/AnalysisCard";
import IssueTable from "../../components/review/IssueTable";
import FileCard from "../../components/review/FileCard";
import SummaryCard from "../../components/review/SummaryCard";
import DashboardCards from "../../components/review/DashboardCards";
import AnalyticsCharts from "../../components/review/AnalyticsCharts";
export default function ReviewResult() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state;
  const [activeTab, setActiveTab] = useState("overview");
  const [searchTerm, setSearchTerm] = useState("");
  const [severityFilter, setSeverityFilter] = useState("All");
  const [sortBy, setSortBy] = useState("score");
  // Handle empty state gracefully
  if (!data) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center text-white px-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center max-w-md shadow-2xl">
          <HelpCircle size={64} className="mx-auto text-blue-500 mb-4 animate-bounce" />
          <h1 className="text-3xl font-extrabold mb-4 tracking-tight">No Review Found</h1>
          <p className="text-slate-400 mb-6">
            It looks like you haven't uploaded a project for static code analysis yet.
          </p>
          <button
            onClick={() => navigate("/dashboard")}
            className="w-full bg-blue-600 hover:bg-blue-700 transition-colors py-3 rounded-lg text-white font-bold inline-flex items-center justify-center gap-2"
          >
            <ArrowLeft size={16} /> Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const filesList = data.review || [];

  const filteredFiles = useMemo(() => {

  const result = filesList.filter((file) => {

    const matchesSearch =
      file.filename
        .toLowerCase()
        .includes(searchTerm.toLowerCase());

    const matchesSeverity =
      severityFilter === "All" ||
      (file.severity || "")
        .toLowerCase() === severityFilter.toLowerCase();

    return matchesSearch && matchesSeverity;

  });

  result.sort((a, b) => {

    if (sortBy === "score") {
      return (b.score || 0) - (a.score || 0);
    }

    if (sortBy === "name") {
      return a.filename.localeCompare(b.filename);
    }

    if (sortBy === "severity") {

      const order = {
        Critical: 4,
        High: 3,
        Medium: 2,
        Low: 1,
      };

      return (
        (order[b.severity] || 0) -
        (order[a.severity] || 0)
      );
    }

    return 0;

  });

  return result;

}, [filesList, searchTerm, severityFilter, sortBy]);

  // 1. Radon Aggregations
  const projectRadon = useMemo(() => {
    let totalLoc = 0;
    let totalSloc = 0;
    let totalLloc = 0;
    let totalComments = 0;
    let totalMulti = 0;
    let totalBlank = 0;
    let sumMi = 0;
    let countMi = 0;
    let allCC = [];

    filesList.forEach((file) => {
      if (!file.radon || !file.radon.success) return;

      // Raw metrics
      try {
        const rawObj = typeof file.radon.raw_metrics === "string" ? JSON.parse(file.radon.raw_metrics) : file.radon.raw_metrics;
        const raw = Object.values(rawObj)[0] || {};
        totalLoc += raw.loc || 0;
        totalSloc += raw.sloc || 0;
        totalLloc += raw.lloc || 0;
        totalComments += raw.comments || 0;
        totalMulti += raw.multi || 0;
        totalBlank += raw.blank || 0;
      } catch (e) {}

      // MI
      try {
        const miObj = typeof file.radon.maintainability === "string" ? JSON.parse(file.radon.maintainability) : file.radon.maintainability;
        const mi = Object.values(miObj)[0] || {};
        if (mi.mi !== undefined) {
          sumMi += mi.mi;
          countMi++;
        }
      } catch (e) {}

      // CC
      try {
        const ccObj = typeof file.radon.complexity === "string" ? JSON.parse(file.radon.complexity) : file.radon.complexity;
        const cc = Object.values(ccObj)[0] || [];
        cc.forEach((item) => {
          allCC.push({
            ...item,
            filename: file.filename
          });
        });
      } catch (e) {}
    });

    const avgMi = countMi > 0 ? sumMi / countMi : 100;
    
    // Map MI score to Grade
    let miGrade = "A";
    if (avgMi < 21) miGrade = "C";
    else if (avgMi < 51) miGrade = "B";

    // Complexity average
    const avgCc = allCC.length > 0 ? allCC.reduce((sum, item) => sum + item.complexity, 0) / allCC.length : 1;
    let ccGrade = "A";
    if (avgCc > 40) ccGrade = "F";
    else if (avgCc > 30) ccGrade = "E";
    else if (avgCc > 20) ccGrade = "D";
    else if (avgCc > 10) ccGrade = "C";
    else if (avgCc > 5) ccGrade = "B";

    return {
      raw: { loc: totalLoc, sloc: totalSloc, lloc: totalLloc, comments: totalComments, multi: totalMulti, blank: totalBlank },
      mi: { score: avgMi, grade: miGrade },
      cc: { list: allCC, avg: avgCc, grade: ccGrade }
    };
  }, [filesList]);

  // 2. Pylint Aggregations
  const projectPylint = useMemo(() => {
    let allIssues = [];
    let errors = 0;
    let warnings = 0;
    let conventions = 0;
    let refactors = 0;

    filesList.forEach((file) => {
      const issues = file.pylint?.success ? file.pylint.issues || [] : [];
      issues.forEach((issue) => {
        allIssues.push({
          ...issue,
          path: file.filename
        });
        if (issue.type === "error") errors++;
        else if (issue.type === "warning") warnings++;
        else if (issue.type === "convention") conventions++;
        else if (issue.type === "refactor") refactors++;
      });
    });

    // Score based on penalty deductions
    const pylintScore = Math.max(0, 10.0 - (errors * 2.0 + warnings * 1.0 + refactors * 0.5 + conventions * 0.2));

    return {
      issues: allIssues,
      errors,
      warnings,
      conventions,
      refactors,
      score: pylintScore
    };
  }, [filesList]);

  // 3. Bandit Aggregations
  const projectBandit = useMemo(() => {
    let allIssues = [];
    let high = 0;
    let medium = 0;
    let low = 0;

    filesList.forEach((file) => {
      const issues = file.bandit?.success ? file.bandit.report?.results || [] : [];
      issues.forEach((issue) => {
        allIssues.push({
          ...issue,
          filename: file.filename
        });
        if (issue.issue_severity === "HIGH") high++;
        else if (issue.issue_severity === "MEDIUM") medium++;
        else if (issue.issue_severity === "LOW") low++;
      });
    });

    return {
      issues: allIssues,
      high,
      medium,
      low
    };
  }, [filesList]);

  // 4. Global Metrics
  const totalFiles = filesList.length;
  const totalLinesOfCode = projectRadon.raw.loc || filesList.reduce((sum, f) => sum + (f.lines || 0), 0);
  const totalStaticIssues = projectPylint.issues.length + projectBandit.issues.length;
  const securityIssues = projectBandit.issues.length;
  const complexityGrade = projectRadon.cc.grade;
  const maintainabilityGrade = projectRadon.mi.grade;

  return (
    <div className="space-y-8">
      {/* Redirection header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <span className="text-xs font-semibold text-blue-500 uppercase tracking-widest">Static Code Analysis</span>
          <h1 className="text-3xl font-extrabold text-white mt-1 tracking-tight">
            Code Review Report: <span className="font-mono text-slate-400 text-2xl font-medium">{data.filename}</span>
          </h1>
        </div>
        <button
          onClick={() => navigate("/dashboard")}
          className="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 px-4 py-2.5 rounded-lg text-sm font-semibold text-slate-300 transition-all duration-200"
        >
          <ArrowLeft size={16} /> Dashboard
        </button>
      </div>

      {/* Tabs list */}
      <div className="flex border-b border-slate-800 overflow-x-auto gap-2">
        <button
          onClick={() => setActiveTab("overview")}
          className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 whitespace-nowrap cursor-pointer ${
            activeTab === "overview"
              ? "border-blue-500 text-blue-400 bg-blue-500/5"
              : "border-transparent text-slate-400 hover:text-white hover:bg-slate-900/50"
          }`}
        >
          <LayoutDashboard size={16} /> Overview
        </button>

        <button
          onClick={() => setActiveTab("pylint")}
          className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 whitespace-nowrap cursor-pointer ${
            activeTab === "pylint"
              ? "border-purple-500 text-purple-400 bg-purple-500/5"
              : "border-transparent text-slate-400 hover:text-white hover:bg-slate-900/50"
          }`}
        >
          <FileSpreadsheet size={16} /> Pylint Quality
        </button>

        <button
          onClick={() => setActiveTab("bandit")}
          className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 whitespace-nowrap cursor-pointer ${
            activeTab === "bandit"
              ? "border-red-500 text-red-400 bg-red-500/5"
              : "border-transparent text-slate-400 hover:text-white hover:bg-slate-900/50"
          }`}
        >
          <ShieldCheck size={16} /> Bandit Security
        </button>

        <button
          onClick={() => setActiveTab("radon")}
          className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 whitespace-nowrap cursor-pointer ${
            activeTab === "radon"
              ? "border-amber-500 text-amber-400 bg-amber-500/5"
              : "border-transparent text-slate-400 hover:text-white hover:bg-slate-900/50"
          }`}
        >
          <Binary size={16} /> Radon Metrics
        </button>

        <button
          onClick={() => setActiveTab("files")}
          className={`flex items-center gap-2 px-5 py-3 border-b-2 font-semibold text-sm transition-all duration-200 whitespace-nowrap cursor-pointer ${
            activeTab === "files"
              ? "border-green-500 text-green-400 bg-green-500/5"
              : "border-transparent text-slate-400 hover:text-white hover:bg-slate-900/50"
          }`}
        >
          <FolderOpen size={16} /> File Analysis
        </button>
      </div>

      {/* Tab Panels */}
      <div className="space-y-6">

        {/* TAB 1: OVERVIEW */}
        {activeTab === "overview" && (
          <div className="space-y-8 animate-fadeIn">

            {/* ================= Day 9 Project Health Dashboard ================= */}
            <DashboardCards dashboard={data.dashboard} />

            {/* ================= Existing Overview Metrics ================= */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">

              <MetricCard
                title="Total Files"
                value={totalFiles}
                icon={<FolderOpen size={20} />}
                color="blue"
              />

              <MetricCard
                title="Total LOC"
                value={totalLinesOfCode}
                icon={<FileCode size={20} />}
                color="purple"
              />

              <MetricCard
                title="Static Issues"
                value={totalStaticIssues}
                icon={<AlertTriangle size={20} />}
                color="orange"
                description={`${projectPylint.issues.length} Pylint | ${projectBandit.issues.length} Bandit`}
              />

              <MetricCard
                title="Security Issues"
                value={securityIssues}
                icon={<ShieldCheck size={20} />}
                color="red"
                description={`${projectBandit.high} High | ${projectBandit.medium} Med | ${projectBandit.low} Low`}
              />

              <MetricCard
                title="Complexity Grade"
                value={complexityGrade}
                icon={<Binary size={20} />}
                color="yellow"
                description={`Avg CC: ${projectRadon.cc.avg.toFixed(1)}`}
              />

              <MetricCard
                title="Maintainability"
                value={maintainabilityGrade}
                icon={<LayoutDashboard size={20} />}
                color="green"
                description={`Avg MI: ${projectRadon.mi.score.toFixed(1)}`}
              />

            </div>

            {/* ================= AI Project Summary ================= */}
            <SummaryCard summary={data.project_summary} />
            <AnalyticsCharts dashboard={data.dashboard} />

          </div>
        )}


        {/* TAB 2: PYLINT */}
        {activeTab === "pylint" && (
          <div className="space-y-6 animate-fadeIn">
            <AnalysisCard
              title="Pylint Quality Checker"
              icon={<FileSpreadsheet size={24} />}
              score={`${projectPylint.score.toFixed(1)}/10`}
              badgeText={projectPylint.score >= 8 ? "Good Standards" : projectPylint.score >= 6 ? "Moderate" : "Action Required"}
              badgeColor={projectPylint.score >= 8 ? "green" : projectPylint.score >= 6 ? "yellow" : "red"}
            >
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-slate-950 p-4 border border-slate-800 rounded-xl text-center">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Errors</p>
                  <p className="text-3xl font-black mt-2 text-red-500">{projectPylint.errors}</p>
                </div>
                <div className="bg-slate-950 p-4 border border-slate-800 rounded-xl text-center">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Warnings</p>
                  <p className="text-3xl font-black mt-2 text-amber-500">{projectPylint.warnings}</p>
                </div>
                <div className="bg-slate-950 p-4 border border-slate-800 rounded-xl text-center">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Convention Issues</p>
                  <p className="text-3xl font-black mt-2 text-blue-500">{projectPylint.conventions}</p>
                </div>
                <div className="bg-slate-950 p-4 border border-slate-800 rounded-xl text-center">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Refactor Suggestions</p>
                  <p className="text-3xl font-black mt-2 text-purple-500">{projectPylint.refactors}</p>
                </div>
              </div>

              <IssueTable issues={projectPylint.issues} type="pylint" />
            </AnalysisCard>
          </div>
        )}

        {/* TAB 3: BANDIT */}
        {activeTab === "bandit" && (
          <div className="space-y-6 animate-fadeIn">
            <AnalysisCard
              title="Bandit Security Analysis"
              icon={<ShieldCheck size={24} />}
              badgeText={projectBandit.high > 0 ? "Vulnerable" : projectBandit.medium > 0 ? "Warnings" : "Secure"}
              badgeColor={projectBandit.high > 0 ? "red" : projectBandit.medium > 0 ? "yellow" : "green"}
            >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="bg-slate-950 p-4 border border-slate-800/80 rounded-xl text-center border-l-4 border-l-red-500">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">High Severity</p>
                  <p className="text-3xl font-black mt-2 text-red-500">{projectBandit.high}</p>
                </div>
                <div className="bg-slate-950 p-4 border border-slate-800/80 rounded-xl text-center border-l-4 border-l-amber-500">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Medium Severity</p>
                  <p className="text-3xl font-black mt-2 text-amber-500">{projectBandit.medium}</p>
                </div>
                <div className="bg-slate-950 p-4 border border-slate-800/80 rounded-xl text-center border-l-4 border-l-blue-500">
                  <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Low Severity</p>
                  <p className="text-3xl font-black mt-2 text-blue-500">{projectBandit.low}</p>
                </div>
              </div>

              {projectBandit.issues.length > 0 && (
                <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 mb-6">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3">Security Recommendations</h3>
                  <ul className="list-disc pl-5 text-sm text-slate-400 space-y-2">
                    {projectBandit.high > 0 && <li>Immediate Attention: Resolve critical security vulnerabilities. Avoid insecure functions like <code className="text-red-400 font-mono">eval</code> or hardcoded passwords.</li>}
                    {projectBandit.medium > 0 && <li>Warning items: Remove unvetted function calls and sanitize external inputs.</li>}
                    <li>Use cryptography services with strong hashing and key derivation algorithms.</li>
                  </ul>
                </div>
              )}

              <IssueTable issues={projectBandit.issues} type="bandit" />
            </AnalysisCard>
          </div>
        )}

        {/* TAB 4: RADON */}
        {activeTab === "radon" && (
          <div className="space-y-6 animate-fadeIn">
            <AnalysisCard
              title="Radon Code Complexity & Metrics"
              icon={<Binary size={24} />}
              badgeText={`Maintainability Grade: ${projectRadon.mi.grade}`}
              badgeColor={projectRadon.mi.grade === "A" ? "green" : projectRadon.mi.grade === "B" ? "yellow" : "red"}
            >
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* CC & MI card */}
                <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-6">
                  <div>
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Complexity</h3>
                    <div className="flex items-baseline gap-2 mt-2">
                      <span className="text-4xl font-black text-white">{projectRadon.cc.avg.toFixed(1)}</span>
                      <span className="text-sm text-slate-500">Average CC</span>
                    </div>
                    <div className="mt-3 text-xs text-slate-400">
                      Average cyclomatic complexity per function. Target complexity below 5 for high quality.
                    </div>
                  </div>
                  
                  <div className="border-t border-slate-800 pt-5">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Maintainability Index</h3>
                    <div className="flex items-baseline gap-2 mt-2">
                      <span className="text-4xl font-black text-white">{projectRadon.mi.score.toFixed(1)}</span>
                      <span className="text-sm text-slate-500">Avg MI score</span>
                    </div>
                    <div className="mt-3 text-xs text-slate-400">
                      0–100 score. A (100–51) represents excellent codebase modularity and readability.
                    </div>
                  </div>
                </div>

                {/* Raw Metrics grid */}
                <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 lg:col-span-2 space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider border-b border-slate-800 pb-3">Raw Metrics Summary</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Lines of Code</p>
                      <p className="text-2xl font-black text-white mt-1">{projectRadon.raw.loc}</p>
                    </div>
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Source Lines (SLOC)</p>
                      <p className="text-2xl font-black text-white mt-1">{projectRadon.raw.sloc}</p>
                    </div>
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Logical Lines (LLOC)</p>
                      <p className="text-2xl font-black text-white mt-1">{projectRadon.raw.lloc}</p>
                    </div>
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Comment Lines</p>
                      <p className="text-2xl font-black text-emerald-400 mt-1">{projectRadon.raw.comments}</p>
                    </div>
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Blank Lines</p>
                      <p className="text-2xl font-black text-slate-400 mt-1">{projectRadon.raw.blank}</p>
                    </div>
                    <div className="bg-slate-900 p-4 border border-slate-800/40 rounded-lg">
                      <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Docstrings</p>
                      <p className="text-2xl font-black text-purple-400 mt-1">{projectRadon.raw.multi}</p>
                    </div>
                  </div>
                </div>

              </div>

              {/* CC Breakdown table */}
              {projectRadon.cc.list.length > 0 && (
                <div className="mt-8">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4">Function Complexity breakdown</h3>
                  <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="border-b border-slate-800 bg-slate-900/30 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                          <th className="p-3">File</th>
                          <th className="p-3">Function / Class</th>
                          <th className="p-3">Type</th>
                          <th className="p-3 text-center">Line</th>
                          <th className="p-3 text-center">CC Score</th>
                          <th className="p-3 text-center">Rank</th>
                        </tr>
                      </thead>
                      <tbody className="text-sm text-slate-300 divide-y divide-slate-800/60">
                        {projectRadon.cc.list
                          .sort((a, b) => b.complexity - a.complexity)
                          .map((item, idx) => (
                            <tr key={idx} className="hover:bg-slate-900/20">
                              <td className="p-3 font-mono text-xs text-blue-400">{item.filename}</td>
                              <td className="p-3 font-bold text-white font-mono">{item.name}</td>
                              <td className="p-3 capitalize text-xs text-slate-400">{item.type}</td>
                              <td className="p-3 text-center text-xs font-mono text-slate-400">{item.lineno}</td>
                              <td className="p-3 text-center font-bold">{item.complexity}</td>
                              <td className="p-3 text-center">
                                <span className={`inline-block px-2.5 py-0.5 rounded text-xs font-black ${
                                  item.rank === "A" ? "bg-green-500/10 text-green-400 border border-green-500/20" :
                                  item.rank === "B" ? "bg-blue-500/10 text-blue-400 border border-blue-500/20" :
                                  item.rank === "C" ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20" :
                                  "bg-red-500/10 text-red-400 border border-red-500/20"
                                }`}>
                                  {item.rank}
                                </span>
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </AnalysisCard>
          </div>
        )}

        {/* TAB 5: FILES */}
        {activeTab === "files" && (
          <div className="space-y-6 animate-fadeIn">

            <div className="flex justify-between items-center bg-slate-900/30 p-4 border border-slate-800/80 rounded-xl">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <FolderOpen size={20} className="text-green-500" />
                Scanned Files ({filteredFiles.length})
              </h2>

              <span className="text-xs text-slate-400">
                Click Expand Details on any file card to view specific code warnings
              </span>
            </div>

            <div className="space-y-4">

              {/* Search + Filter + Sort */}
              <div className="flex flex-col md:flex-row gap-4 mb-6">

                <input
                  type="text"
                  placeholder="🔍 Search files..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white"
                />

                <select
                  value={severityFilter}
                  onChange={(e) => setSeverityFilter(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white"
                >
                  <option>All</option>
                  <option>Critical</option>
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>

                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white"
                >
                  <option value="score">⭐ Highest AI Score</option>
                  <option value="severity">🚨 Highest Severity</option>
                  <option value="name">📄 File Name (A-Z)</option>
                </select>

              </div>

              {/* File Cards */}
              {filteredFiles.map((file, idx) => (
                <FileCard
                  key={idx}
                  file={file}
                />
              ))}

            </div>

          </div>
        )}
      </div>
    </div>
  );
}