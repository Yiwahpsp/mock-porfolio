import type { Metadata } from "next";
import { Prompt } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const prompt = Prompt({
  weight: ["400", "500", "700"],
  subsets: ["latin", "thai"],
  display: 'swap',
  variable: '--font-prompt',
  preload: true,
});

export const metadata: Metadata = {
  title: "CyberSecure Downloads",
  description: "Your source for advanced cybersecurity software downloads",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`bg-white min-h-screen ${prompt.className} antialiased`}>
        <nav className="top-0 fixed flex justify-between items-center bg-white shadow-md p-4 w-full h-16 text-gray-900">
          <Link href={"/"} className="font-bold text-xl">CyberSecure</Link>
          <div className="space-x-6">
            <Link href="/about" className="hover:font-semibold transform duration-200">About</Link>
            <Link href="/projects" className="hover:font-semibold transform duration-200">Downloads</Link>
            <Link href="/contact" className="hover:font-semibold transform duration-200">Support</Link>
          </div>
        </nav>
        <div className="flex flex-col justify-between bg-gray-900 pt-16 min-h-screen">
          {children}
          <footer className="bg-gray-900 p-4 font-light text-white text-sm text-center">
            <Link href={"/admin"}>&copy; {new Date().getFullYear()} CyberSecure Downloads</Link>
          </footer>
        </div>
      </body>
    </html>
  );
}
