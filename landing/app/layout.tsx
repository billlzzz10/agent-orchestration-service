import type { Metadata } from "next";
import "./globals.css";
import "@fontsource/inter/variable.css";
import { Providers } from "./providers";

const title = "Agent Orchestration Platform";
const description =
  "Streamline your AI agent workflows with a secure orchestration platform built for enterprise automation.";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || ""),
  title: {
    template: "%s | Agent Orchestration Platform",
    default: title
  },
  description,
  openGraph: {
    title,
    description,
    url: "https://agent-orchestration.example.com",
    siteName: "Agent Orchestration Platform",
    locale: "en_US",
    type: "website"
  },
  twitter: {
    card: "summary_large_image",
    title,
    description
  }
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
