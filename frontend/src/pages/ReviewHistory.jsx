import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = "http://127.0.0.1:5000/api/v1";

export default function ReviewHistory() {
  const navigate = useNavigate();

  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

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

console.log("Status:", response.status);
console.log("API Response:", data);
console.log("Reviews:", data.data);

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
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this review?"
    );

    if (!confirmDelete) return;

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

      const response = await fetch(
        `${API}/report/${id}/pdf`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        alert("Failed to download PDF");
        return;
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = `review_${id}.pdf`;

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Unable to download PDF");
    }
  };
const filteredReviews = reviews.filter((review) =>
  review.summary.toLowerCase().includes(search.toLowerCase()) ||
  String(review.id).includes(search)
);
  if (loading) {
    return (
      <div className="p-8 text-center text-lg">
        Loading Reviews...
      </div>
    );
  }

  return (
    <div className="p-8">

      <h1 className="text-3xl font-bold mb-6">
        Review History
      </h1>
      <input
  type="text"
  placeholder="Search by ID or Summary..."
  value={search}
  onChange={(e) => setSearch(e.target.value)}
  className="w-full p-3 border rounded-lg mb-6"
/>
{filteredReviews.length === 0 ? (
        <div className="text-center text-gray-500 text-lg">
          No Reviews Found
        </div>
      ) : (
        <table className="w-full border border-gray-300">

          <thead className="bg-gray-200">

            <tr>
              <th className="border p-3">ID</th>
              <th className="border p-3">Overall Score</th>
              <th className="border p-3">Summary</th>
              <th className="border p-3">Created</th>
              <th className="border p-3">Actions</th>
            </tr>

          </thead>

          <tbody>

          {filteredReviews.map((review) => (

              <tr key={review.id} className="hover:bg-gray-100">

                <td className="border p-3">
                  {review.id}
                </td>

                <td className="border p-3">
                  {review.overall_score}
                </td>

                <td className="border p-3">
                  {review.summary}
                </td>

                <td className="border p-3">
                  {review.created_at}
                </td>

                <td className="border p-3">

  <div className="flex gap-2">

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