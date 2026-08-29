import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("pulse_access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      if (typeof window !== "undefined") {
        const refreshToken = localStorage.getItem("pulse_refresh_token");
        if (refreshToken) {
          try {
            const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });
            const newAccessToken = res.data.access_token;
            localStorage.setItem("pulse_access_token", newAccessToken);
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return apiClient(originalRequest);
          } catch (refreshErr) {
            localStorage.removeItem("pulse_access_token");
            localStorage.removeItem("pulse_refresh_token");
            localStorage.removeItem("pulse_user");
            window.location.href = "/login";
          }
        }
      }
    }
    return Promise.reject(error);
  }
);
