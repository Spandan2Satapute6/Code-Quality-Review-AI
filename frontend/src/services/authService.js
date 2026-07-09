import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api/v1/auth",
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerUser = (data) => api.post("/register", data);

export const loginUser = (data) => api.post("/login", data);

export const getProfile = (token) =>
  api.get("/profile", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export default api;