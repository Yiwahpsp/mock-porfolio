"use client";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
interface LoginFormData {
  username: string;
  password: string;
}

export default function Page() {
  const [formData, setFormData] = useState<LoginFormData>({
    username: "",
    password: "",
  });

  const router = useRouter();

  const [error, setError] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Basic validation
    if (!formData.username || !formData.password) {
      setError("Both fields are required!");
      return;
    }

    setError("");
    // Here you can handle form submission (e.g., API call)
    if (formData.username !== "admin" || formData.password !== "p@ssw0rd!") {
      setError("Wrong password or username");
      return;
    }
    console.log("Form Submitted", formData);
    router.push("/admin/dashboard");
  };

  return (
    <div className="flex-1 text-white text-center flex items-center justify-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <div className="w-full flex flex-row justify-center">
          <label htmlFor="username">Username: </label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
            className="bg-gray-700 w-full ms-2 ps-1"
          />
        </div>
        <div className="w-full flex flex-row justify-center">
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            className="bg-gray-700 ms-2 w-full ps-1"
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button
          type="submit"
          className="bg-yellow-500 w-full rounded px-3 py-2"
        >
          Login
        </button>
      </form>
    </div>
  );
}
