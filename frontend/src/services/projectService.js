import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000/api/v1",
});

export const uploadProject = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await API.post("/projects/upload", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};