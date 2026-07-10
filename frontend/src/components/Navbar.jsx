import { useAuth } from "../context/AuthContext";
import { FaUserCircle } from "react-icons/fa";

export default function Navbar() {
  const { user } = useAuth();

  return (
    <div className="bg-slate-900 border-b border-slate-800 px-8 py-5 flex justify-between items-center">

      <h1 className="text-2xl font-bold text-white">
        Dashboard
      </h1>

      <div className="flex items-center gap-3 text-white">
        <FaUserCircle size={28} />
        <div>
          <p className="font-semibold">
            {user?.name || "User"}
          </p>
          <p className="text-sm text-slate-400">
            Logged In
          </p>
        </div>
      </div>

    </div>
  );
}