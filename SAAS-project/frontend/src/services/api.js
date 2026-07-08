import axios from "axios";

// Base URL of our Flask backend.
// Locally this falls back to localhost:5000. In production (e.g. Vercel),
// set VITE_API_URL to your deployed backend's URL, like:
// https://stockflow-backend.onrender.com/api
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Attach the JWT token (if we have one) to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
