export default function Page() {
  return (
    <div className="w-full h-[100%] bg-gray-900 py-20 px-5 space-y-8 max-w-lg mx-auto">
      <div className="text-center">
        <h2 className="text-3xl font-semibold text-yellow-500">Contact Us</h2>
      </div>
      <div className="mx-auto w-full h-fit max-w-2xl  rounded-2xl py-8 px-8 md:px-12">
        <form className="space-y-4 text-gray-100">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="First Name"
              className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-900"
            />
            <input
              type="text"
              placeholder="Last Name"
              className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-900"
            />
          </div>
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-900"
          />
          <input
            type="tel"
            placeholder="Phone"
            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-900"
          />
          <textarea
            placeholder="Message"
            rows={4}
            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-900"
          ></textarea>
          <button
            type="submit"
            className="w-full mt-4 bg-white text-yellow-500 font-semibold py-2 px-4 rounded-lg hover:text-white hover:bg-yellow-500 transition"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  )
}