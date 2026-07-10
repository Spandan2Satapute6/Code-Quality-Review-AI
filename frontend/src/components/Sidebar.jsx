import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaUpload,
  FaHistory,
  FaChartBar,
  FaCog,
} from "react-icons/fa";

export default function Sidebar() {
  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <FaHome />,
    },
    {
      name: "Upload Project",
      path: "/dashboard",
      icon: <FaUpload />,
    },
    {
      name: "Review History",
      path: "/history",
      icon: <FaHistory />,
    },
    {
      name: "Reports",
      path: "/reports",
      icon: <FaChartBar />,
    },
    {
      name: "Settings",
      path: "/settings",
      icon: <FaCog />,
    },
  ];

  return (
    <div className="w-64 min-h-screen bg-slate-900 text-white p-6 shadow-xl">

      <h1 className="text-2xl font-bold text-blue-400 mb-10">
        Code Review AI
      </h1>

      <nav className="space-y-3">
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "hover:bg-slate-800 text-slate-300"
              }`
            }
          >
            <span className="text-lg">{item.icon}</span>
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

    </div>
  );
}