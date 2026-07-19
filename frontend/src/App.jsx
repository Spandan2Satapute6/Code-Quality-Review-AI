import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReviewDetails from "./pages/history/ReviewDetails";
import DashboardLayout from "./layouts/DashboardLayout";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

import Dashboard from "./pages/dashboard/Dashboard";
import ReviewResult from "./pages/review/ReviewResult";
import ReviewHistory from "./pages/history/ReviewHistory";
import Reports from "./pages/reports/Reports";
import Settings from "./pages/settings/Settings";

import ProtectedRoute from "./routes/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/review" element={<ReviewResult />} />

          <Route path="/history" element={<ReviewHistory />} />

          {/* ADD THIS ROUTE */}
          <Route path="/history/:id" element={<ReviewDetails />} />

          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}