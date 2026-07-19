import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Settings() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [profile, setProfile] = useState({
    name: "",
    email: "",
  });

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:5000/api/v1/profile",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setProfile(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const updateProfile = async () => {
    try {
      await axios.put(
        "http://127.0.0.1:5000/api/v1/profile",
        {
          name: profile.name,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Profile updated successfully");
    } catch (err) {
      alert(err.response?.data?.message || "Update failed");
    }
  };

  const changePassword = async () => {
    try {
      await axios.put(
        "http://127.0.0.1:5000/api/v1/profile/password",
        {
          old_password: oldPassword,
          new_password: newPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Password changed successfully");

      setOldPassword("");
      setNewPassword("");
    } catch (err) {
      alert(err.response?.data?.message || "Password update failed");
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="text-white max-w-2xl space-y-8">
      <h1 className="text-3xl font-bold">
        Account Settings
      </h1>

      <div className="space-y-4">
        <input
          className="w-full p-3 rounded bg-slate-800"
          value={profile.name}
          onChange={(e) =>
            setProfile({
              ...profile,
              name: e.target.value,
            })
          }
          placeholder="Name"
        />

        <input
          className="w-full p-3 rounded bg-slate-800"
          value={profile.email}
          disabled
        />

        <button
          onClick={updateProfile}
          className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded"
        >
          Update Profile
        </button>
      </div>

      <div className="space-y-4">
        <input
          type="password"
          className="w-full p-3 rounded bg-slate-800"
          placeholder="Current Password"
          value={oldPassword}
          onChange={(e) => setOldPassword(e.target.value)}
        />

        <input
          type="password"
          className="w-full p-3 rounded bg-slate-800"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />

        <button
          onClick={changePassword}
          className="bg-green-600 hover:bg-green-700 px-5 py-2 rounded"
        >
          Change Password
        </button>
      </div>

      <button
        onClick={handleLogout}
        className="bg-red-600 hover:bg-red-700 px-5 py-2 rounded"
      >
        Logout
      </button>
    </div>
  );
}