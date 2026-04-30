import axios from "axios";

// Create axios instance
const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Upload image to backend
export const uploadImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await API.post("/upload", formData);

    return response.data; // now returning JSON (image + metrics)
  } catch (error) {
    console.error("API upload error:", error);
    throw error;
  }
};