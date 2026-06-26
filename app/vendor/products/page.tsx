"use client";

import ProtectedRoute from "@/components/ProtectedRoute";
import Pagination from "@/components/pagination";
import Link from "next/link";
import { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  product_id: number;
  product_name: string;
  description: string;
  price: number;
  stock_quantity: number;
  image_url: string;
}

export default function VendorProducts() {

  const [products, setProducts] = useState<Product[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchProducts(page);
  }, [page, search]);

  const fetchProducts = async (
    currentPage: number
  ) => {

    try {

      const token =
        localStorage.getItem("token");

      const response =
        await axios.get(
          `http://127.0.0.1:8000/api/products/my-products?page=${currentPage}&limit=6&search=${search}`,
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
          }
        );

      setProducts(
        response.data.products
      );

      setTotalPages(
        response.data.total_pages
      );

    } catch (error) {

      console.error(error);

    }

  };

  const deleteProduct = async (
    id: number
  ) => {

    if (
      !confirm(
        "Delete this product?"
      )
    )
      return;

    try {

      const token =
        localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:8000/api/products/${id}`,
        {
          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );

      fetchProducts(page);

      alert(
        "Product deleted successfully"
      );

    } catch (error) {

      console.error(error);

      alert(
        "Failed to delete product"
      );

    }

  };

  return (

    <ProtectedRoute
      allowedRoles={[2]}
    >

      <div className="min-h-screen bg-[#0B1120] text-white p-10">

        <div className="flex justify-between items-center mb-10">

          <div>

            <h1 className="text-5xl font-bold">
              My Products
            </h1>

            <p className="text-gray-400 mt-2">
              Manage your products here.
            </p>

          </div>

        </div>

        <div className="mb-8">

          <input
            type="text"
            placeholder="🔍 Search Products..."
            value={search}
            onChange={(e) => {

              setSearch(
                e.target.value
              );

              setPage(1);

            }}
            className="w-full md:w-96 p-4 rounded-2xl bg-white/10 border border-white/10 outline-none focus:border-cyan-400"
          />

        </div>

        <div className="grid lg:grid-cols-3 gap-8">

          {products.length === 0 ? (

            <div className="col-span-3 text-center py-20">

              <h2 className="text-4xl font-bold text-gray-300">
                No Products Found
              </h2>

              <p className="text-gray-500 mt-4">
                Start selling by adding your first product.
              </p>

            </div>

          ) : (

            products.map((product) => (

              <div
                key={product.product_id}
                className="bg-white/5 border border-white/10 rounded-3xl overflow-hidden backdrop-blur-xl hover:scale-105 transition duration-300"
              >

                <img
                  src={`http://127.0.0.1:8000${product.image_url}`}
                  alt={product.product_name}
                  className="w-full h-60 object-cover"
                />

                <div className="p-6">

                  <h2 className="text-2xl font-bold">
                    {product.product_name}
                  </h2>

                  <p className="text-gray-400 mt-2 line-clamp-2">
                    {product.description}
                  </p>

                  <div className="flex justify-between items-center mt-5">

                    <span className="text-cyan-400 text-2xl font-bold">
                      ₹{product.price}
                    </span>

                    <span className="text-gray-400">
                      Stock: {product.stock_quantity}
                    </span>

                  </div>

                  <div className="flex gap-3 mt-6">

                   <Link
  href={`/vendor/edit-product/${product.product_id}`}
  className="flex-1"
>
  <button
    className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-xl transition"
  >
    Edit
  </button>
</Link>

                    <button
                      onClick={() =>
                        deleteProduct(product.product_id)
                      }
                      className="flex-1 bg-red-600 hover:bg-red-700 py-3 rounded-xl transition"
                    >
                      Delete
                    </button>

                  </div>

                </div>

              </div>

            ))

          )}

        </div>

        <Pagination
          page={page}
          totalPages={totalPages}
          onPageChange={setPage}
        />

      </div>

    </ProtectedRoute>

  );

}