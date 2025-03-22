export default function Page() {
  const projects = [
    {
      title: "Smart-Lock System",
      description: "A secure IoT-based smart lock integrating fingerprint, numpad, and RFID authentication, with real-time monitoring via Firebase and Blynk.",
      tech: ["ESP32", "Firebase", "React", "Blynk"],
    },
    {
      title: "ML Paper Categorization",
      description: "A machine learning model that predicts the category of academic papers based on metadata such as author, organization, and abstract.",
      tech: ["Python", "ML", "NLP"],
    },
    {
      title: "Portfolio Website",
      description: "A responsive and interactive portfolio showcasing my skills, projects, and experience as a full-stack developer and ML enthusiast.",
      tech: ["React", "Tailwind", "Next.js"],
    },
  ];

  return (
    <div className="flex flex-col gap-8 w-full h-[100%] bg-gray-900 py-20 px-5 max-w-[1024px] mx-auto">
      <h2 className="text-3xl font-semibold text-yellow-500 text-center mb-6">My Projects</h2>
      <div className="space-y-8">
        {projects.map((project, index) => (
          <div key={index} className="p-6 border rounded-lg shadow-sm bg-gray-50">
            <h3 className="text-xl font-semibold text-gray-800">{project.title}</h3>
            <p className="mt-2 text-gray-600">{project.description}</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {project.tech.map((tech, i) => (
                <span key={i} className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm">
                  {tech}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}