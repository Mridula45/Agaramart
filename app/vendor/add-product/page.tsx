"use client";

import ProtectedRoute from "@/components/ProtectedRoute";

import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

interface Category {
  category_id: number;
  category_name: string;
}

export default function AddProduct() {

  const router = useRouter();

  const [categories, setCategories] =
    useState<Category[]>([]);

  const [categoryId, setCategoryId] =
    useState("");

  const [productName, setProductName] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [price, setPrice] =
    useState("");

  const [stock, setStock] =
    useState("");

  const [image, setImage] =
    useState<File | null>(null);

  const [preview, setPreview] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  useEffect(() => {

    fetchCategories();

  }, []);

  const fetchCategories = async () => {

    try {

      const response =
        await axios.get(
          "http://127.0.0.1:8000/api/categories"
        );

      setCategories(response.data);

    }

    catch (error) {

      console.error(error);

    }

  };

  const uploadImage = async () => {

    if (!image) return "";

    const token =
      localStorage.getItem("token");

    const formData =
      new FormData();

    formData.append(
      "file",
      image
    );

    const response =
      await axios.post(
        "http://127.0.0.1:8000/api/upload",
        formData,
        {
          headers: {
            Authorization:
              `Bearer ${token}`,
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

    return response.data.image_url;

  };

  const handleSubmit = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    if (
      !productName ||
      !description ||
      !price ||
      !stock ||
      !categoryId
    ) {

      alert(
        "Please fill all fields."
      );

      return;

    }

    try {

      setLoading(true);

      const imageUrl =
        await uploadImage();

      const token =
        localStorage.getItem("token");

      await axios.post(
        "http://127.0.0.1:8000/api/products",
        {

          category_id:
            Number(categoryId),

          product_name:
            productName,

          description,

          price:
            Number(price),

          stock_quantity:
            Number(stock),

          image_url:
            imageUrl

        },
        {
          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );

      alert(
        "Product Added Successfully"
      );

      router.push(
        "/vendor/products"
      );

    }

    catch (error) {

      console.error(error);

      alert(
        "Failed to add product"
      );

    }

    finally {

      setLoading(false);

    }

  };

  return (

    <ProtectedRoute
      allowedRoles={[2]}
    >

      <div className="min-h-screen bg-[#0B1120] text-white flex justify-center items-center p-10">

        <form
          onSubmit={handleSubmit}
          className="bg-white/5 border border-white/10 backdrop-blur-xl rounded-3xl p-10 w-full max-w-2xl"
        >

          <h1 className="text-4xl font-bold mb-8">

            Add Product

          </h1>
                    <input
            type="text"
            placeholder="Product Name"
            value={productName}
            onChange={(e) =>
              setProductName(e.target.value)
            }
            className="w-full p-4 rounded-xl bg-white/10 border border-white/10 mb-5 outline-none"
          />

          <textarea
            placeholder="Product Description"
            value={description}
            onChange={(e) =>
              setDescription(e.target.value)
            }
            rows={4}
            className="w-full p-4 rounded-xl bg-white/10 border border-white/10 mb-5 outline-none"
          />

          <select
            value={categoryId}
            onChange={(e) =>
              setCategoryId(e.target.value)
            }
            className="w-full p-4 rounded-xl bg-white/10 border border-white/10 mb-5 outline-none"
          >
            <option value="">
              Select Category
            </option>

            {categories.map((category) => (

              <option
                key={category.category_id}
                value={category.category_id}
                className="text-black"
              >
                {category.category_name}
              </option>

            ))}

          </select>

          <div className="grid md:grid-cols-2 gap-5">

            <input
              type="number"
              placeholder="Price"
              value={price}
              onChange={(e) =>
                setPrice(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
            />

            <input
              type="number"
              placeholder="Stock Quantity"
              value={stock}
              onChange={(e) =>
                setStock(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
            />

          </div>

          <div className="mt-6">

            <label className="block mb-3 text-gray-300">
              Product Image
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={(e) => {

                if (!e.target.files) return;

                const file =
                  e.target.files[0];

                setImage(file);

                setPreview(
                  URL.createObjectURL(file)
                );

              }}
              className="w-full p-3 rounded-xl bg-white/10 border border-white/10"
            />

          </div>

          {preview && (

            <div className="mt-6">

              <img
                src={preview}
                alt="Preview"
                className="h-56 rounded-2xl object-cover border border-white/10"
              />

            </div>

          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-8 w-full bg-gradient-to-r from-cyan-500 to-purple-600 py-4 rounded-2xl text-lg font-bold hover:scale-105 transition disabled:opacity-60"
          >
            {loading
              ? "Adding Product..."
              : "Add Product"}
          </button>

        </form>

      </div>

    </ProtectedRoute>

  );

}