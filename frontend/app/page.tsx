"use client";
import React, { useState } from "react";
import Link from "next/link";
import { ArrowRight, Download, Search, Shield, Code } from "lucide-react";

export default function Page() {
  const [showInstructions, setShowInstructions] = useState(false);

  const handleDownload = () => {
    setShowInstructions(true);

    // Add check for download failure
    const downloadTimer = setTimeout(() => {
      alert("Download may have failed. Please try again or contact support.");
    }, 5000); // Show error if download doesn't start within 5 seconds

    // Clear the timer if component unmounts
    return () => clearTimeout(downloadTimer);
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Hero Section */}
      <section className="flex gap-5 flex-col px-5 items-center justify-center text-center h-[80vh] min-h-[500px] py-20 relative">
        <h2 className="text-white text-4xl font-semibold">
          Welcome to CyberSecure Downloads
        </h2>
        <p className="text-white text-3xl font-semibold">
          Premium software downloads with verified security
        </p>

        <div className="flex flex-wrap gap-4 justify-center">
          <a
            href="https://mock-porfolio.onrender.com/api/download/client-app"
            onClick={handleDownload}
            className="mt-5 cursor-pointer flex justify-center rounded-2xl items-center text-white hover:text-gray-900 gap-2 bg-yellow-500 px-6 py-3 w-fit shadow-md shadow-gray-600"
            download="cybersecure-installer.exe"
          >
            <Download size={16} className="" strokeWidth={3} />
            <div className="font-semibold ">Download Now</div>
          </a>
        </div>

        {/* Instructions popup */}
        {showInstructions && (
          <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 w-full text-gray-800 max-w-md bg-white p-5 rounded-lg shadow-lg text-left">
            <h4 className="font-bold text-lg mb-2">Installation Started!</h4>
            <p className="mb-2">
              To install the software:
            </p>
            <ol className="list-decimal pl-5 space-y-1 text-sm">
              <li>Locate the downloaded file</li>
              <li>Double-click to run the installer</li>
              <li>Follow the on-screen setup instructions</li>
              <li>Restart your computer if prompted</li>
            </ol>
            <button
              onClick={() => setShowInstructions(false)}
              className="mt-3 bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded text-sm"
            >
              Close
            </button>
          </div>
        )}
      </section>

      {/* Software Categories Section */}
      <section id="software" className="bg-white py-20 px-5 text-gray-900">
        <div className="max-w-6xl mx-auto px-6">
          <h3 className="text-2xl font-bold text-center">Popular Software Categories</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-6">
            <div className="p-6 shadow-lg rounded-lg bg-gray-50 hover:bg-gray-100 transition cursor-pointer">
              <div className="flex items-center mb-3">
                <Shield className="mr-2 text-yellow-500" size={20} />
                <h4 className="text-lg font-semibold">Security Tools</h4>
              </div>
              <p className="text-sm mt-2">Protect your system with our premium antivirus, firewall and encryption tools.</p>
              <Link
                href={"/downloads"}
                className="mt-4 text-sm text-yellow-500 font-medium flex items-center">
                Read More <ArrowRight size={14} className="ml-1" />
              </Link>
            </div>
            <div className="p-6 shadow-lg rounded-lg bg-gray-50 hover:bg-gray-100 transition cursor-pointer">
              <div className="flex items-center mb-3">
                <Code className="mr-2 text-yellow-500" size={20} />
                <h4 className="text-lg font-semibold">Development Tools</h4>
              </div>
              <p className="text-sm mt-2">IDEs, code editors, and development frameworks for all programming needs.</p>
              <Link
                href={"/downloads"}
                className="mt-4 text-sm text-yellow-500 font-medium flex items-center">
                Read More <ArrowRight size={14} className="ml-1" />
              </Link>
            </div>
            <div className="p-6 shadow-lg rounded-lg bg-gray-50 hover:bg-gray-100 transition cursor-pointer">
              <div className="flex items-center mb-3">
                <Search className="mr-2 text-yellow-500" size={20} />
                <h4 className="text-lg font-semibold">Productivity Apps</h4>
              </div>
              <p className="text-sm mt-2">Office suites, task managers, and tools to boost your daily productivity.</p>
              <Link
                href={"/downloads"}
                className="mt-4 text-sm text-yellow-500 font-medium flex items-center">
                Read More <ArrowRight size={14} className="ml-1" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Support Section */}
      <section id="support" className="py-20 text-center px-5 space-y-4">
        <h3 className="text-2xl text-white font-bold">Need Technical Support?</h3>
        <p className="text-white text-lg max-w-xl mx-auto">
          Our team is ready to help with installation problems or software questions
        </p>
        <Link href="/support" className="mt-5 mx-auto flex justify-center cursor-pointer rounded-2xl items-center gap-2 bg-white hover:bg-yellow-500 text-yellow-500 hover:text-white px-6 py-3 w-fit shadow-md shadow-gray-400">
          <div className=" rounded-lg font-semibold">Get Support</div>
          <ArrowRight size={16} className="" strokeWidth={3} />
        </Link>
      </section>
    </div>
  );
};

