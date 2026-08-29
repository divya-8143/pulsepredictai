import { create } from "zustand";
import { User, UserRole } from "@/types";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (user: User, token: string, refreshToken?: string) => void;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  setAuth: (user, token, refreshToken) => {
    if (typeof window !== "undefined") {
      localStorage.setItem("pulse_access_token", token);
      if (refreshToken) {
        localStorage.setItem("pulse_refresh_token", refreshToken);
      }
      localStorage.setItem("pulse_user", JSON.stringify(user));
    }
    set({ user, token, isAuthenticated: true, isLoading: false });
  },
  logout: () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("pulse_access_token");
      localStorage.removeItem("pulse_refresh_token");
      localStorage.removeItem("pulse_user");
    }
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },
  initialize: () => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("pulse_access_token");
      const userStr = localStorage.getItem("pulse_user");
      if (token && userStr) {
        try {
          const user = JSON.parse(userStr);
          set({ user, token, isAuthenticated: true, isLoading: false });
          return;
        } catch (e) {
          console.error("Failed to parse stored user", e);
        }
      }
    }
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },
}));
