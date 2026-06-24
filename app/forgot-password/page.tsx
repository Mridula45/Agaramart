"use client";

import { useState } from "react";
import axios from "axios";
export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");

  const handleSubmit = async () => {

    try {

      await axios.post(
        "http://127.0.0.1:8000/api/auth/forgot-password",
        {
          email
        }
      );

      alert(
        "OTP sent successfully"
      );

    } catch (error) {

      alert(
        "Email not found"
      );

    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0B1120]">

      <div className="bg-white p-8 rounded-xl shadow-lg w-96">

        <h1 className="text-3xl font-bold text-black text-center mb-6">
          Forgot Password
        </h1>

        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          onChange={(e) =>
            setEmail(
              e.target.value
            )
          }
          className="w-full border p-3 rounded-lg text-black mb-4"
        />

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 text-white p-3 rounded-lg"
        >
          Send OTP
        </button>

      </div>

    </div>
  );
}
