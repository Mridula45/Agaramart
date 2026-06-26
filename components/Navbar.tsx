"use client";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";

export default function Navbar() {
  const { user, logout } = useAuth();
{user?.name}
<button onClick={logout}>
Logout
</button>
  return (
    <nav className="sticky top-0 z-50 backdrop-blur-xl bg-white/5 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">

        <Link href="/">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            AgaraMart
          </h1>
        </Link>

        <div className="flex gap-6 text-white">
          <Link href="/products">Products</Link>
          <Link href="/cart">Cart</Link>
          <Link href="/orders">Orders</Link>
          <Link href="/login">Login</Link>
          <Link href="/register">Register</Link>
        </div>

      </div>
    </nav>
  );
}