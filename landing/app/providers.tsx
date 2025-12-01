"use client";

import { CacheProvider } from "@chakra-ui/next-js";
import { ColorModeScript } from "@chakra-ui/react";
import { SaasProvider } from "@saas-ui/react";
import { theme } from "@/theme";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <CacheProvider>
      <ColorModeScript initialColorMode={theme.config?.initialColorMode ?? "light"} />
      <SaasProvider theme={theme}>{children}</SaasProvider>
    </CacheProvider>
  );
}
