"use client";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import LoginUser from "@/libs/loginUser";

export default function Page() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent page refresh

    if (!username || !password) {
      setError("Both fields are required!");
      return;
    }

    setError("");

    try {
      const response = await LoginUser(username, password);

      if (!response) {
        setError("Error logging in, please try again later.");
        return;
      }

      if (response.error) {
        setError(response.message)
        return;
      }
      console.log("Login successful:", response);

      router.push("/admin/dashboard");
    } catch (error) {
      console.error("Error logging in:", error);
      setError("An error occurred. Please try again later.");
    }
  };

  return (
    <div className="flex-1 text-white text-center flex items-center justify-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        <div className="w-full flex flex-row justify-center">
          <label htmlFor="username">Username: </label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            className="bg-gray-700 w-full ms-2 px-2 py-1 rounded-xl"
          />
        </div>
        <div className="w-full flex flex-row justify-center">
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="bg-gray-700 w-full ms-2 px-2 py-1 rounded-xl"
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button
          type="submit"
          className="bg-yellow-500 w-full rounded-xl px-3 py-2 hover:bg-white hover:text-yellow-500 transition cursor-pointer duration-200 ease-in-out"
        >
          Login
        </button>
      </form>
    </div>
  );
}
