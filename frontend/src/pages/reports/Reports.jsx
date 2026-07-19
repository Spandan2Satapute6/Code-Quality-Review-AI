import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000/api/v1";

export default function Reports() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch(`${API}/reviews`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setReviews(data.data || []);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
      alert("Unable to fetch reports");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-white text-xl">
        Loading Reports...
      </div>
    );
  }

  const totalReviews = reviews.length;

  const averageScore =
    totalReviews > 0
      ? (
          reviews.reduce(
            (sum, review) => sum + (review.overall_score || 0),
            0
          ) / totalReviews
        ).toFixed(2)
      : 0;

  const highestScore =
    totalReviews > 0
      ? Math.max(...reviews.map((r) => r.overall_score || 0))
      : 0;

  const lowestScore =
    totalReviews > 0
      ? Math.min(...reviews.map((r) => r.overall_score || 0))
      : 0;

  return (
    <div className="p-8 text-white">

      <h1 className="text-3xl font-bold mb-8">
        Reports & Analytics
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">

        <div className="bg-slate-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-slate-300">
            Total Reviews
          </h2>

          <p className="text-4xl font-bold mt-3 text-blue-400">
            {totalReviews}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-slate-300">
            Average Score
          </h2>

          <p className="text-4xl font-bold mt-3 text-green-400">
            {averageScore}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-slate-300">
            Highest Score
          </h2>

          <p className="text-4xl font-bold mt-3 text-yellow-400">
            {highestScore}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-slate-300">
            Lowest Score
          </h2>

          <p className="text-4xl font-bold mt-3 text-red-400">
            {lowestScore}
          </p>
        </div>

      </div>

      <div className="bg-slate-900 rounded-lg p-6 shadow">

        <h2 className="text-2xl font-bold mb-4">
          Review Summary
        </h2>

        {reviews.length === 0 ? (
          <p className="text-slate-400">
            No reviews available.
          </p>
        ) : (
          <table className="w-full border border-slate-700">

            <thead className="bg-slate-800">
              <tr>
                <th className="p-3 border">ID</th>
                <th className="p-3 border">Score</th>
                <th className="p-3 border">Summary</th>
                <th className="p-3 border">Created</th>
              </tr>
            </thead>

            <tbody>
              {reviews.map((review) => (
                <tr key={review.id}>

                  <td className="border p-3">
                    {review.id}
                  </td>

                  <td className="border p-3">
                    {review.overall_score}
                  </td>

                  <td className="border p-3">
                    {review.summary || "No summary"}
                  </td>

                  <td className="border p-3">
                    {review.created_at}
                  </td>

                </tr>
              ))}
            </tbody>

          </table>
        )}

      </div>

    </div>
  );
}