"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {

  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {

    e.preventDefault();

    try {

      // Login

      const response = await axios.post(
        "http://127.0.0.1:8000/api/auth/login",
        {
          email,
          password
        }
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      // Get user profile

      const profile = await axios.get(
        "http://127.0.0.1:8000/api/auth/me",
        {
          headers: {
            Authorization:
              `Bearer ${response.data.access_token}`
          }
        }
      );

      const role = profile.data.role_id;

      alert("Login Successful");

      if (role === 1) {

        router.push("/products");

      }

      else if (role === 2) {

        router.push("/vendor");

      }

      else if (role === 3) {

        router.push("/admin");

      }

      else if (role === 4) {

        router.push("/superadmin");

      }

    }

    catch (error: any) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );

    }

  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-[#0B1120]">

      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-xl shadow-lg w-96 text-black"
      >

        <h1 className="text-4xl font-bold text-center mb-6">
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>
            setEmail(e.target.value)
          }
          className="w-full border p-3 rounded-lg mb-4"
        />

        <div className="relative">

          <input
            type={
              showPassword
              ? "text"
              : "password"
            }
            placeholder="Password"
            value={password}
            onChange={(e)=>
              setPassword(e.target.value)
            }
            className="w-full border p-3 rounded-lg"
          />

          <button
            type="button"
            className="absolute right-3 top-3 text-blue-600"
            onClick={()=>
              setShowPassword(
                !showPassword
              )
            }
          >
            {showPassword ? "Hide" : "Show"}
          </button>

        </div>

        <button
          type="submit"
          className="mt-6 w-full bg-blue-600 text-white py-3 rounded-lg"
        >
          Login
        </button>

        <div className="text-center mt-5">

          <Link
            href="/forgot-password"
            className="text-blue-600 hover:underline"
          >
            Forgot Password?
          </Link>

        </div>

        <div className="text-center mt-2">

          <Link
            href="/register"
            className="text-blue-600 hover:underline"
          >
            Create Account
          </Link>

        </div>

      </form>

    </div>

  );

}