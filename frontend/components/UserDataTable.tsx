"use client";
import { useEffect, useState } from "react";
import GetUserData from "@/libs/getUserData";
import Link from "next/link";
import { Trash } from "lucide-react";
import DeleteUserData from "@/libs/deleteUserData";

interface UserData {
  id: number;
  url: string;
  username: string;
  password: string;
  timestamp: string;
}

export default function UserDataTable() {
  const PAGE_SIZE = 7;
  const [currentPage, setCurrentPage] = useState(1);
  const [userData, setUserData] = useState<UserData[]>([]);
  const [error, setError] = useState("");
  const totalPages = Math.ceil(userData.length / PAGE_SIZE);
  const displayedUsers = userData.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);
  const paginationNeeded = userData.length > PAGE_SIZE;

  const handleDeleteUserData = (id: number) => async () => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        setError("No authentication token found. Please log in.");
        return;
      }
      await DeleteUserData(id, token);
      setUserData((prevData) => prevData.filter((user) => user.id !== id));
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    }
  }

  // Format timestamp to readable date
  const formatTimestamp = (timestamp: string) => {
    try {
      // Convert string timestamp to number
      const date = new Date(parseFloat(timestamp) * 1000);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    } catch {
      return timestamp; // Return original if parsing fails
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("authToken");
        console.log("Token:", token);
        if (!token) {
          setError("No authentication token found. Please log in.");
          return;
        }
        const data = await GetUserData(token);
        setUserData(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred.");
        }
      }
    };

    fetchData();
  }, []);

  // Then in your table rendering:
  return (
    <div className="w-full overflow-x-auto rounded-lg border border-gray-300 shadow-sm">
      {error && <p className="text-red-500 text-center py-4">{error}</p>}
      <table className="w-full text-sm text-left border-collapse">
        <thead className="bg-gray-100 border-b">
          <tr>
            <th className="text-center w-4/12 px-4 py-4 text-gray-600 font-medium uppercase tracking-wide">URL</th>
            <th className="text-center w-2/12 px-4 py-4 text-gray-600 font-medium uppercase tracking-wide">USERNAME/EMAIL</th>
            <th className="text-center w-2/12 px-4 py-4 text-gray-600 font-medium uppercase tracking-wide">PASSWORD</th>
            <th className="text-center w-3/12 px-4 py-4 text-gray-600 font-medium uppercase tracking-wide">TIMESTAMP</th>
            <th className="text-center w-1/12 px-4 py-4 text-gray-600 font-medium uppercase tracking-wide">DELETE</th>
          </tr>
        </thead>
        <tbody>
          {displayedUsers.map((user) => (
            <tr key={user.id} className="border-b hover:bg-gray-800 text-sm">
              <td className="text-left w-4/12 px-4 py-4 text-yellow-500 truncate max-w-[150px]">
                <Link href={user.url} target="_blank" className="hover:underline">{user.url}</Link>
              </td>
              <td className="text-left w-2/12 px-4 py-4">{user.username}</td>
              <td className="text-left w-2/12 px-4 py-4">{user.password}</td>
              <td className="text-center w-3/12 px-4 py-4">{formatTimestamp(user.timestamp)}</td>
              <td className="text-left w-1/12 px-4 py-4">
                <button className="text-red-500 hover:text-red-700 cursor-pointer flex justify-center items-center w-full" onClick={() => handleDeleteUserData(user.id)}>
                  <Trash size={16} strokeWidth={2} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex items-center justify-between p-3 bg-white">
        <button
          className={`px-3 py-1 rounded ${(!paginationNeeded || currentPage === 1) ? 'text-gray-400 cursor-not-allowed' : 'text-gray-900 hover:text-yellow-500'}`}
          disabled={!paginationNeeded || currentPage === 1}
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
        >
          Previous
        </button>

        <span className="text-gray-600">
          {paginationNeeded
            ? `Page ${currentPage} of ${totalPages}`
            : "All items"}
        </span>

        <button
          className={`px-3 py-1 rounded ${(!paginationNeeded || currentPage === totalPages) ? 'text-gray-400 cursor-not-allowed' : 'text-gray-900 hover:text-yellow-500'}`}
          disabled={!paginationNeeded || currentPage === totalPages}
          onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
        >
          Next
        </button>
      </div>
    </div>
  );
}