import React from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function Page() {

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Hero Section */}
      <section className="flex gap-5 flex-col px-5 items-center justify-center text-center h-[80vh] min-h-[500px] py-20">
        <h2 className="text-white text-4xl font-semibold">I&apos;m <span className="text-yellow-500">Jane,</span></h2>
        <p className="text-white text-3xl font-semibold">Full-Stack Developer</p>
        <Link href="/projects" className="mt-5 flex justify-center rounded-2xl items-center gap-2 bg-white px-6 py-3 w-fit  shadow-md shadow-gray-400">
          <div className=" text-yellow-500 rounded-lg font-semibold">Go to see projects</div>
          <ArrowRight size={16} className="text-yellow-500" strokeWidth={3} />
        </Link>
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
        <Link href="/contact" className="mt-5 mx-auto flex justify-center rounded-2xl items-center gap-2 bg-white px-6 py-3 w-fit  shadow-md shadow-gray-400">
          <div className=" text-yellow-500 rounded-lg font-semibold">Get in touch</div>
          <ArrowRight size={16} className="text-yellow-500" strokeWidth={3} />
        </Link>
      </section>
    </div>
  );
};

