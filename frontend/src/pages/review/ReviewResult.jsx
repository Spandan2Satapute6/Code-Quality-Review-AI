import { useLocation, useNavigate } from "react-router-dom";

export default function ReviewResult() {

  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state;

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">

        <div>

          <h1 className="text-3xl font-bold mb-6">
            No Review Found
          </h1>

          <button
            onClick={() => navigate("/dashboard")}
            className="bg-blue-600 px-6 py-3 rounded-lg"
          >
            Back to Dashboard
          </button>

        </div>

      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <h1 className="text-4xl font-bold mb-8">
        AI Code Review Report
      </h1>

      {/* Project Summary */}

      <div className="bg-slate-900 rounded-xl p-6 mb-8">

        <h2 className="text-2xl font-bold mb-4">
          Project Summary
        </h2>

        <p>
          <b>Summary:</b>
          <br />
          {data.project_summary?.summary || "No summary"}
        </p>

        <br />

        <p>
          <b>Verdict:</b> {data.project_summary?.verdict}
        </p>

        <p>
          <b>Overall Score:</b> {data.project_summary?.overall_score}
        </p>

      </div>

      {/* File Reviews */}

      <div className="bg-slate-900 rounded-xl p-6">

        <h2 className="text-2xl font-bold mb-6">
          File Reviews
        </h2>

        {data.review?.map((file, index) => (

          <div
            key={index}
            className="border border-slate-700 rounded-lg p-5 mb-5"
          >

            <h3 className="text-xl font-bold text-green-400">
              {file.filename}
            </h3>

            <p className="mt-2">
              <b>Score:</b> {file.score}
            </p>

            <p className="mt-2">
              <b>Lines:</b> {file.lines}
            </p>

            <div className="mt-3">

              <b>Issues</b>

              <ul className="list-disc ml-6">

                {file.issues?.length > 0 ? (
                  file.issues.map((issue, i) => (
                    <li key={i}>{issue}</li>
                  ))
                ) : (
                  <li>No issues found.</li>
                )}

              </ul>

            </div>

            <div className="mt-3">

              <b>Suggestions</b>

              <ul className="list-disc ml-6">

                {file.suggestions?.length > 0 ? (
                  file.suggestions.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))
                ) : (
                  <li>No suggestions.</li>
                )}

              </ul>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}