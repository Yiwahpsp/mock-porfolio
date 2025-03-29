"use client"

import UserDataTable from "@/components/UserDataTable"
import DeleteAllUserData from "@/libs/deleteAllUserData"

export default function Page() {
  const handleDeleteAll = async () => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No authentication token found. Please log in.");
        return;
      }

      const response = await DeleteAllUserData(token);
      if (response.error) {
        console.error("Error deleting all user data:", response.message);
      } else {
        console.log("All user data deleted successfully:", response);
        // Optionally, refresh the page or update the state to reflect the changes
        window.location.reload();
      }
    } catch (error) {
      console.error("Error deleting all user data:", error);
    }
  }
  return (
    <div className="flex flex-col gap-8 w-full h-[100%] bg-gray-900 py-20 px-5 max-w-[1024px] mx-auto">
      <div className="flex flex-row justify-between items-center">
        <h2 className="text-white text-4xl font-semibold rounded-xl">Admin Dashboard</h2>
        <button onClick={handleDeleteAll} className="font-semibold px-3 py-2 rounded-xl text-white bg-yellow-500 hover:text-yellow-500 hover:bg-white">Delete All</button>
      </div>
      <UserDataTable />
    </div>
  )
}
