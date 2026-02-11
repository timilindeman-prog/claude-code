import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Minimal App Generator UI",
  description: "A minimal Next.js app with textarea, button, and output area.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
