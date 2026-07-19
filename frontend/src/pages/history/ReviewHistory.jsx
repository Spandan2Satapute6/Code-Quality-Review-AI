import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = "http://127.0.0.1:5000/api/v1";

export default function ReviewHistory() {
  const navigate = useNavigate();

  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
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
        alert(data.message || "Failed to fetch reviews");
      }
    } catch (error) {
      console.error(error);
      alert("Server Error");
    } finally {
      setLoading(false);
    }
  };

  const deleteReview = async (id) => {
    if (!window.confirm("Are you sure you want to delete this review?")) {
      return;
    }

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(`${API}/reviews/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        fetchReviews();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
      alert("Unable to delete review");
    }
  };

  const downloadPDF = async (id) => {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch(`${API}/report/${id}/pdf`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const msg = await response.text();
        console.error(msg);
        alert("Failed to download PDF");
        return;
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = `review_${id}.pdf`;

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Unable to download PDF");
    }
  };

  const filteredReviews = reviews.filter((review) => {
    const summary = review.summary || "";

    return (
      summary.toLowerCase().includes(search.toLowerCase()) ||
      String(review.id).includes(search)
    );
  });

  if (loading) {
    return (
      <div className="p-8 text-white text-xl">
        Loading Reviews...
      </div>
    );
  }

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold mb-6">
        Review History
      </h1>

      <input
        type="text"
        placeholder="Search by ID or Summary..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full mb-6 p-3 rounded text-black"
      />

      {filteredReviews.length === 0 ? (
        <div className="text-center text-gray-400">
          No Reviews Found
        </div>
      ) : (
        <table className="w-full border border-gray-600">
          <thead className="bg-slate-800">
            <tr>
              <th className="p-3 border">ID</th>
              <th className="p-3 border">Score</th>
              <th className="p-3 border">Summary</th>
              <th className="p-3 border">Date</th>
              <th className="p-3 border">Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredReviews.map((review) => (
              <tr key={review.id} className="text-center border">

                <td className="p-3 border">
                  {review.id}
                </td>

                <td className="p-3 border">
                  {review.overall_score}
                </td>

                <td className="p-3 border">
                  {review.summary}
                </td>

                <td className="p-3 border">
                  {review.created_at}
                </td>

                <td className="p-3 border">
                  <div className="flex justify-center gap-2">

                    <button
                      onClick={() => navigate(`/history/${review.id}`)}
                      className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
                    >
                      View
                    </button>

                    <button
                      onClick={() => downloadPDF(review.id)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
                    >
                      PDF
                    </button>

                    <button
                      onClick={() => deleteReview(review.id)}
                      className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
                    >
                      Delete
                    </button>

                  </div>
                </td>

              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}