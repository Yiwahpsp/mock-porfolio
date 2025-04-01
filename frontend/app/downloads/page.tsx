import Link from "next/link";

export default function Page() {
  const softwares = [
    {
      title: "Ultimate Password Extractor",
      description: "Extract and manage passwords with state-of-the-art security protocols.",
      tech: ["Windows", "AES", "DPAPI"],
    },
    {
      title: "System Vulnerability Scanner",
      description: "Scan and detect vulnerabilities across your network effortlessly.",
      tech: ["Nmap", "Python", "Automation"],
    },
    {
      title: "Malware Analyzer Pro",
      description: "Analyze and dissect suspicious files in a secure sandbox environment.",
      tech: ["Sandbox", "Analysis", "Reporting"],
    },
  ];

  return (
    <div className="flex flex-col gap-8 w-full h-[100%] bg-gray-900 py-20 px-5 max-w-[1024px] mx-auto">
      <h2 className="text-3xl font-semibold text-yellow-500 text-center mb-6">Available Downloads</h2>
      <div className="space-y-8">
        {softwares.map((software, index) => (
          <div key={index} className="p-6 border rounded-lg shadow-sm bg-gray-50">
            <h3 className="text-xl font-semibold text-gray-800">{software.title}</h3>
            <p className="mt-2 text-gray-600">{software.description}</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {software.tech.map((tech, i) => (
                <span key={i} className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm">
                  {tech}
                </span>
              ))}
            </div>
            <Link href="#" className="mt-5 flex justify-center cursor-pointer rounded-2xl items-center gap-2 hover:bg-yellow-500 text-yellow-500 hover:text-white px-6 py-3 w-fit">
              <div className=" rounded-lg">Download now</div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}