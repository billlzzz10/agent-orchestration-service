import { extendTheme, type ThemeConfig } from "@chakra-ui/react";
import { theme as baseTheme } from "@saas-ui/theme";

const config: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false
};

export const theme = extendTheme(baseTheme, {
  config,
  fonts: {
    heading: "InterVariable, var(--font-inter), system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    body: "InterVariable, var(--font-inter), system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
  },
  styles: {
    global: {
      body: {
        bg: "slate.950",
        color: "whiteAlpha.900"
      }
    }
  },
  colors: {
    brand: {
      50: "#eff6ff",
      100: "#dbeafe",
      200: "#bfdbfe",
      300: "#93c5fd",
      400: "#60a5fa",
      500: "#3b82f6",
      600: "#2563eb",
      700: "#1d4ed8",
      800: "#1e40af",
      900: "#1e3a8a"
    }
  }
});
