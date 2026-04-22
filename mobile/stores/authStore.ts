import { create } from "zustand";
import * as SecureStore from "expo-secure-store";

import authService from "@/services/auth.service";
import { User } from "@/types/user.types";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (token: string, user?: User | null) => Promise<void>;
  setUser: (user: User | null) => void;
  logout: () => Promise<void>;
  loadToken: () => Promise<void>;
  hydrateAuth: () => Promise<void>;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  setAuth: async (token: string, user: User | null = null) => {
    await SecureStore.setItemAsync("access_token", token);
    set({ user, token, isAuthenticated: true, isLoading: false });
  },

  setUser: (user: User | null) => {
    set({ user });
  },

  logout: async () => {
    await SecureStore.deleteItemAsync("access_token");
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },

  loadToken: async () => {
    const token = await SecureStore.getItemAsync("access_token");
    set({ token, isAuthenticated: !!token, isLoading: false });
  },

  hydrateAuth: async () => {
    const token = await SecureStore.getItemAsync("access_token");

    if (!token) {
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
      return;
    }

    set({ token, isAuthenticated: true, isLoading: true });

    try {
      const user = await authService.getMe();
      set({ user, token, isAuthenticated: true, isLoading: false });
    } catch {
      await SecureStore.deleteItemAsync("access_token");
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
    }
  },
}));

export default useAuthStore;
