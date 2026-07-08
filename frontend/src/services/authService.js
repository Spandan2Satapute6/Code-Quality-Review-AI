import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api/v1/auth",
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerUser = (data) =>
  API.post("/register", data);

export const loginUser = (data) =>
  API.post("/login", data);

export const getProfile = (token) =>
  API.get("/profile", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });