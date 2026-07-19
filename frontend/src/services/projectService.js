import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api/v1",
});

export const uploadProject = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const token = localStorage.getItem("token");

  const response = await API.post("/projects/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};