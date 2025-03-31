export default function Page() {
  return (
    <div className="flex flex-col gap-8 w-full h-[100%] bg-gray-900 py-20 px-5 max-w-[1024px] mx-auto">
      <div className="text-center space-y-8">
        <h2 className="text-3xl font-semibold text-yellow-500">About CyberSecure Downloads</h2>
        <p className="text-gray-200">
          We offer an exclusive selection of advanced software tools focused on cybersecurity,
          system analysis, and digital forensics. Our downloads are designed for professionals
          and enthusiasts who are not afraid to explore the cutting edge in software and security.
        </p>
      </div>
      <hr className="mt-4 w-full border-solid border-[0.5px] text-gray-400" />
      <div className="mt-6 space-y-4">
        <h3 className="text-xl font-semibold text-yellow-500">Our Mission</h3>
        <p className="text-gray-200">
          To empower users with powerful tools that combine innovation with robust security, while pushing the boundaries of software design.
        </p>
        <h3 className="text-xl font-semibold text-yellow-500">What We Do</h3>
        <ul className="list-disc list-inside text-gray-200">
          <li>Distribute state-of-the-art software solutions</li>
          <li>Provide reliable technical support and updates</li>
          <li>Maintain secure, transparent download channels</li>
        </ul>
      </div>
    </div>
  )
}