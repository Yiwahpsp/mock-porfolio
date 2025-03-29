import type { Metadata } from "next";
import { Prompt } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const prompt = Prompt({
  weight: ["400", "500", "700"],
  subsets: ["latin", "thai"],
  display: 'swap',
  variable: '--font-prompt',
});

export const metadata: Metadata = {
  title: "My Portfolio",
  description: "My professional web development portfolio",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`bg-white min-h-screen ${prompt.className} antialiased`}
      >
        <nav className="top-0 fixed flex justify-between items-center bg-white shadow-md p-4 w-full h-16 text-gray-900">
          <Link href={"/"} className="font-bold text-xl">My Portfolio</Link>
          <div className="space-x-6">
            <Link href="/about">About</Link>
            <Link href="/projects">Projects</Link>
            <Link href="/contact">Contact</Link>
          </div>
        </nav>
        <div className="flex flex-col justify-between bg-gray-900 pt-16 min-h-screen">
          {children}
          <footer className="bg-gray-900 p-4 font-light text-white text-sm text-center">
            <Link href={"/admin"}>&copy; {new Date().getFullYear()} My Portfolio</Link>
          </footer>
        </div>
      </body>
    </html>
  );
}
