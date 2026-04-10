import { create } from "zustand";
import * as SecureStore from "expo-secure-store";
import { User } from "@/types/user.types";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (user: User, token: string) => Promise<void>;
  logout: () => Promise<void>;
  loadToken: () => Promise<void>;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  setAuth: async (user: User, token: string) => {
    await SecureStore.setItemAsync("access_token", token);
    set({ user, token, isAuthenticated: true, isLoading: false });
  },

  logout: async () => {
    await SecureStore.deleteItemAsync("access_token");
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },

  loadToken: async () => {
    const token = await SecureStore.getItemAsync("access_token");
    set({ token, isAuthenticated: !!token, isLoading: false });
  },
}));

export default useAuthStore;
