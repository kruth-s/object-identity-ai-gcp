import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const gilroy = localFont({
  src: [
    {
      path: "../public/fonts/Gilroy-Regular.ttf",
      weight: "400",
      style: "normal",
    },
    {
      path: "../public/fonts/Gilroy-Medium.ttf",
      weight: "600",
      style: "normal",
    },
    {
      path: "../public/fonts/Gilroy-Bold.ttf",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-gilroy",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Findly - Lost and Found Platform",
  description: "Report lost items or help reunite found belongings with their owners — fast, secure, and community-driven.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${gilroy.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
