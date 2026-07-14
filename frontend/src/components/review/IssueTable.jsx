import { useState, useMemo } from "react";
import SeverityBadge from "./SeverityBadge";
import { Search, ChevronDown, ChevronUp } from "lucide-react";

export default function IssueTable({ issues = [], type = "pylint" }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSeverity, setSelectedSeverity] = useState("ALL");
  const [sortField, setSortField] = useState("line");
  const [sortAsc, setSortAsc] = useState(true);

  // Normalize issues based on type (pylint or bandit)
  const normalizedIssues = useMemo(() => {
    return issues.map((issue, index) => {
      if (type === "pylint") {
        return {
          id: `pylint-${index}`,
          filename: issue.path ? issue.path.split(/[\\/]/).pop() : "unknown",
          fullPath: issue.path || "",
          line: issue.line || 0,
          column: issue.column || 0,
          severity: issue.type || "warning", // pylint uses type
          rule: issue.symbol || issue["message-id"] || "",
          message: issue.message || "",
          code: null
        };
      } else {
        // bandit
        return {
          id: `bandit-${index}`,
          filename: issue.filename ? issue.filename.split(/[\\/]/).pop() : "unknown",
          fullPath: issue.filename || "",
          line: issue.line_number || 0,
          column: issue.col_offset || 0,
          severity: issue.issue_severity || "medium",
          rule: issue.test_id || "",
          message: issue.issue_text || "",
          code: issue.code || null
        };
      }
    });
  }, [issues, type]);

  // Filter issues
  const filteredIssues = useMemo(() => {
    return normalizedIssues.filter((issue) => {
      const matchSearch =
        issue.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        issue.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        issue.rule.toLowerCase().includes(searchTerm.toLowerCase());
      
      const severityNorm = issue.severity.toUpperCase();
      const selectedNorm = selectedSeverity.toUpperCase();
      const matchSeverity =
        selectedNorm === "ALL" ||
        (selectedNorm === "HIGH" && (severityNorm === "HIGH" || severityNorm === "ERROR")) ||
        (selectedNorm === "MEDIUM" && (severityNorm === "MEDIUM" || severityNorm === "WARNING")) ||
        (selectedNorm === "LOW" && (severityNorm === "LOW" || severityNorm === "CONVENTION" || severityNorm === "REFACTOR"));

      return matchSearch && matchSeverity;
    });
  }, [normalizedIssues, searchTerm, selectedSeverity]);

  // Sort issues
  const sortedIssues = useMemo(() => {
    return [...filteredIssues].sort((a, b) => {
      let valA = a[sortField];
      let valB = b[sortField];

      if (typeof valA === "string") {
        valA = valA.toLowerCase();
        valB = valB.toLowerCase();
      }

      if (valA < valB) return sortAsc ? -1 : 1;
      if (valA > valB) return sortAsc ? 1 : -1;
      return 0;
    });
  }, [filteredIssues, sortField, sortAsc]);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  const SortIcon = ({ field }) => {
    if (sortField !== field) return null;
    return sortAsc ? <ChevronUp size={14} className="inline ml-1" /> : <ChevronDown size={14} className="inline ml-1" />;
  };

  return (
    <div className="space-y-4">
      {/* Filters and Search */}
      <div className="flex flex-col md:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-lg border border-slate-800">
        <div className="relative w-full md:w-80">
          <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-400">
            <Search size={16} />
          </span>
          <input
            type="text"
            placeholder="Search issues by message, file, or rule..."
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-250"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="flex items-center gap-3 w-full md:w-auto justify-end">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Filter Severity:</span>
          <select
            className="bg-slate-950 border border-slate-800 text-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-250 cursor-pointer"
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
          >
            <option value="ALL">All Severities</option>
            <option value="HIGH">High / Error</option>
            <option value="MEDIUM">Medium / Warning</option>
            <option value="LOW">Low / Refactor / Convention</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-inner">
        {sortedIssues.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-900/40 text-xs font-semibold text-slate-400 uppercase tracking-wider select-none">
                  <th className="py-3 px-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onClick={() => handleSort("filename")}>
                    File <SortIcon field="filename" />
                  </th>
                  <th className="py-3 px-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onClick={() => handleSort("line")}>
                    Line <SortIcon field="line" />
                  </th>
                  <th className="py-3 px-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onClick={() => handleSort("severity")}>
                    Severity <SortIcon field="severity" />
                  </th>
                  <th className="py-3 px-4 cursor-pointer hover:bg-slate-900/60 transition-colors" onClick={() => handleSort("rule")}>
                    Rule / ID <SortIcon field="rule" />
                  </th>
                  <th className="py-3 px-4 w-1/2">Message</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-sm text-slate-300">
                {sortedIssues.map((issue) => (
                  <tr key={issue.id} className="hover:bg-slate-900/30 transition-colors group">
                    <td className="py-3 px-4 font-mono text-xs text-blue-400 group-hover:text-blue-300 transition-colors">
                      {issue.filename}
                    </td>
                    <td className="py-3 px-4 font-mono text-xs text-slate-400">
                      {issue.line}:{issue.column}
                    </td>
                    <td className="py-3 px-4">
                      <SeverityBadge severity={issue.severity} />
                    </td>
                    <td className="py-3 px-4 font-mono text-xs text-slate-400">
                      {issue.rule}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-sans font-medium text-white">{issue.message}</div>
                      {issue.code && (
                        <pre className="mt-2 p-2 bg-slate-900 rounded border border-slate-800 font-mono text-xs text-emerald-400/90 overflow-x-auto whitespace-pre">
                          <code>{issue.code}</code>
                        </pre>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
            <p className="text-slate-400 font-medium text-lg">No static issues match your filters.</p>
            <p className="text-slate-500 text-sm mt-1">Try tweaking your search term or choosing "All Severities".</p>
          </div>
        )}
      </div>
      <div className="text-right text-xs text-slate-500">
        Showing {sortedIssues.length} of {normalizedIssues.length} findings
      </div>
    </div>
  );
}
