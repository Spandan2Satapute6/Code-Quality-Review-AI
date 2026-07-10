import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { uploadProject } from "../../services/projectService";

export default function Dashboard() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    try {
      setLoading(true);

      const result = await uploadProject(file);

      console.log(result);

      navigate("/review", {
        state: result.data,
      });

    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-white">

      {/* Dashboard Cards */}

      <div className="grid md:grid-cols-4 gap-6">

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Projects</h2>
          <p className="text-5xl font-bold mt-4">1</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Reviews</h2>
          <p className="text-5xl font-bold mt-4">1</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Issues</h2>
          <p className="text-5xl font-bold mt-4">AI</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">AI Score</h2>
          <p className="text-5xl font-bold mt-4 text-green-400">
            Ready
          </p>
        </div>

      </div>

      {/* Upload Section */}

      <div className="mt-8 bg-slate-900 rounded-xl p-8">

        <h2 className="text-2xl font-bold mb-4">
          Upload Your Project
        </h2>

        <p className="text-slate-400 mb-6">
          Upload your project ZIP file for AI-powered code review.
        </p>

        <label className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg cursor-pointer inline-block">

          {loading ? "Uploading..." : "Upload Project"}

          <input
            type="file"
            accept=".zip"
            hidden
            onChange={handleUpload}
          />

        </label>

      </div>

    </div>
  );
}