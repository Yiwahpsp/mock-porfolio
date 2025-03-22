export default function Page() {
  return (
    <div className="flex flex-col gap-8 w-full h-[100%] bg-gray-900 py-20 px-5">
      <div className="text-center space-y-8">
        <h2 className="text-3xl font-semibold text-yellow-500">About Me</h2>
        <p className="text-gray-200">
          Hi, I&apos;m a passionate developer with a keen interest in UX/UI design,
          full-stack development, and machine learning. My journey in technology
          has been driven by curiosity and a desire to create meaningful digital experiences.
        </p>
      </div>
      <hr className="mt-4 w-full border-solid border-[0.5px] text-gray-400" />
      <div className="mt-6 space-y-4">
        <h3 className="text-xl font-semibold text-yellow-500">My Mission</h3>
        <p className="text-gray-200">
          My goal is to craft user-centric applications that are both functional and visually engaging.
          I strive to bridge the gap between technology and human interaction through thoughtful design and efficient development.
        </p>
        <h3 className="text-xl font-semibold text-yellow-500">What I Do</h3>
        <ul className="list-disc list-inside text-gray-200">
          <li>Build intuitive and responsive web applications</li>
          <li>Design engaging user experiences with a focus on accessibility</li>
          <li>Develop machine learning models to extract insights from data</li>
          <li>Continuously learn and experiment with new technologies</li>
        </ul>
      </div>
    </div>
  )
}