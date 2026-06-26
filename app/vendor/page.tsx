"use client";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";

interface Dashboard {
  vendor_name: string;
  total_products: number;
  total_orders: number;
  pending_orders: number;
  revenue: number;
}

export default function VendorDashboard() {
  const [dashboard, setDashboard] =
    useState<Dashboard | null>(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/api/vendor/dashboard",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setDashboard(response.data);
    } catch (error) {
      console.error(error);
      alert("Unable to load dashboard");
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1120] text-white p-10">

      {/* Header */}
      <div className="mb-10">
        <h1 className="text-5xl font-bold">
          Vendor Dashboard
        </h1>

        <p className="text-gray-400 mt-2 text-lg">
          Welcome back,{" "}
          <span className="text-cyan-400 font-semibold">
            {dashboard?.vendor_name}
          </span>
        </p>

        <p className="text-gray-500">
          Manage your products, orders and business.
        </p>
      </div>

      {/* Cards */}

      <div className="grid md:grid-cols-4 gap-6 mb-10">

        <div className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-6 hover:scale-105 transition">

          <p className="text-gray-400">
            Products
          </p>

          <h2 className="text-4xl font-bold mt-3">
            {dashboard?.total_products}
          </h2>

        </div>

        <div className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-6 hover:scale-105 transition">

          <p className="text-gray-400">
            Orders
          </p>

          <h2 className="text-4xl font-bold mt-3">
            {dashboard?.total_orders}
          </h2>

        </div>

        <div className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-6 hover:scale-105 transition">

          <p className="text-gray-400">
            Pending
          </p>

          <h2 className="text-4xl font-bold mt-3">
            {dashboard?.pending_orders}
          </h2>

        </div>

        <div className="rounded-3xl bg-gradient-to-r from-cyan-500 to-purple-600 p-6 hover:scale-105 transition">

          <p className="text-white">
            Revenue
          </p>

          <h2 className="text-4xl font-bold mt-3">
            ₹{dashboard?.revenue}
          </h2>

        </div>

      </div>

      {/* Quick Actions */}

      <div className="grid md:grid-cols-3 gap-6">

        <Link
          href="/vendor/products"
          className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-8 hover:border-cyan-400 transition"
        >
          <h2 className="text-2xl font-bold">
            📦 My Products
          </h2>

          <p className="text-gray-400 mt-2">
            View, edit and delete products.
          </p>
        </Link>

        <Link
          href="/vendor/add-product"
          className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-8 hover:border-green-400 transition"
        >
          <h2 className="text-2xl font-bold">
            ➕ Add Product
          </h2>

          <p className="text-gray-400 mt-2">
            Add a new product to your store.
          </p>
        </Link>

        <Link
          href="/vendor/orders"
          className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-8 hover:border-purple-400 transition"
        >
          <h2 className="text-2xl font-bold">
            🛒 Orders
          </h2>

          <p className="text-gray-400 mt-2">
            View customer orders.
          </p>
        </Link>

      </div>

    </div>
  );
}