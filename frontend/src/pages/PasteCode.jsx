import { useState } from "react";

const API = "http://127.0.0.1:5000/api/v1";

export default function PasteCode() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const reviewCode = async () => {
    if (!code.trim()) {
      alert("Please paste your code.");
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(`${API}/code/review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          code,
          language,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.data);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto">

      <h1 className="text-3xl font-bold mb-6">
        Paste Code Review
      </h1>

      <div className="mb-4">
        <label className="font-semibold">
          Language
        </label>

        <select
          className="border rounded px-3 py-2 ml-4"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="javascript">JavaScript</option>
          <option value="cpp">C++</option>
          <option value="c">C</option>
        </select>
      </div>

      <textarea
        className="w-full h-96 border rounded-lg p-4 font-mono"
        placeholder="Paste your source code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <button
        onClick={reviewCode}
        disabled={loading}
        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded"
      >
        {loading ? "Reviewing..." : "Review Code"}
      </button>

      {result && (
        <div className="mt-8 border rounded-lg p-6 bg-gray-50">

          <h2 className="text-2xl font-bold mb-4">
            Review Result
          </h2>

          <pre className="overflow-auto whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>

        </div>
      )}

    </div>
  );
}
