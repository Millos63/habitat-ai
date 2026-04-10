import { create } from "zustand";
import { ColorSchemeName } from "react-native";

interface ThemeState {
  colorScheme: ColorSchemeName;
  setColorScheme: (scheme: ColorSchemeName) => void;
  toggleColorScheme: () => void;
}

const useThemeStore = create<ThemeState>((set, get) => ({
  colorScheme: "light",

  setColorScheme: (scheme: ColorSchemeName) => {
    set({ colorScheme: scheme });
  },

  toggleColorScheme: () => {
    const current = get().colorScheme;
    set({ colorScheme: current === "dark" ? "light" : "dark" });
  },
}));

export default useThemeStore;
