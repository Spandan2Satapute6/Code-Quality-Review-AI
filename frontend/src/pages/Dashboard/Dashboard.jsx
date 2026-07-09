import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <div className="flex justify-between items-center px-8 py-5 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold">
            Code Quality Review AI
          </h1>
          <p className="text-slate-400">
            Welcome {user?.name || "User"} 👋
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 px-5 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>

      {/* Dashboard Cards */}
      <div className="grid md:grid-cols-4 gap-6 p-8">

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Projects</h2>
          <p className="text-5xl font-bold mt-4">0</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Reviews</h2>
          <p className="text-5xl font-bold mt-4">0</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">Issues</h2>
          <p className="text-5xl font-bold mt-4">0</p>
        </div>

        <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
          <h2 className="text-lg font-semibold">AI Score</h2>
          <p className="text-5xl font-bold mt-4 text-green-400">100%</p>
        </div>

      </div>

      {/* Upload Section */}
      <div className="mx-8 bg-slate-900 rounded-xl p-8">

        <h2 className="text-2xl font-bold mb-4">
          Upload Your Project
        </h2>

        <p className="text-slate-400 mb-6">
          Upload your project ZIP file for AI-powered code review.
        </p>

        <button className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg">
          Upload Project
        </button>

      </div>

    </div>
  );
}