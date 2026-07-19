import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const API = "http://127.0.0.1:5000/api/v1";

export default function ReviewDetails() {
  const { id } = useParams();

  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReview();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchReview = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch(`${API}/reviews/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setReview(data.data);
      } else {
        alert(data.message || "Failed to load review");
      }
    } catch (error) {
      console.error(error);
      alert("Unable to fetch review");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-white text-xl">
        Loading...
      </div>
    );
  }

  if (!review) {
    return (
      <div className="p-8 text-white text-xl">
        Review not found.
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 text-white">

      <h1 className="text-4xl font-bold">
        Review Details
      </h1>

      <div className="bg-slate-900 rounded-lg shadow-lg p-6 border border-slate-700">

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <p><strong>Review ID:</strong> {review.id}</p>

          <p><strong>Project ID:</strong> {review.project_id}</p>

          <p><strong>Overall Score:</strong> {review.overall_score}</p>

          <p><strong>Quality Score:</strong> {review.quality_score}</p>

          <p><strong>Security Score:</strong> {review.security_score}</p>

          <p><strong>Maintainability Score:</strong> {review.maintainability_score}</p>

          <p><strong>Complexity Score:</strong> {review.complexity_score}</p>

        </div>

        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">
            Summary
          </h2>

          <div className="bg-slate-800 rounded p-4 border border-slate-700">
            {review.summary && review.summary.trim() !== ""
              ? review.summary
              : "No summary available."}
          </div>
        </div>

      </div>

      <div className="bg-slate-900 rounded-lg shadow-lg p-6 border border-slate-700">

        <h2 className="text-2xl font-bold mb-4">
          Full AI Report
        </h2>

        <pre className="bg-slate-800 text-green-300 p-4 rounded overflow-auto whitespace-pre-wrap text-sm">
          {JSON.stringify(review.report_json, null, 2)}
        </pre>

      </div>

    </div>
  );
}