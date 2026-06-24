"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  product_id: number;
  product_name: string;
  description: string;
  price: number;
  image_url: string;
}

export default function ProductsPage() {
  const [search, setSearch] = useState("");
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const fetchProducts = async () => {

      try {

        const response = await axios.get(
          "http://127.0.0.1:8000/api/products"
        );

        setProducts(response.data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }
    };

    fetchProducts();

  }, []);

  const filteredProducts = products.filter((product) =>
    product.product_name.toLowerCase().includes(search.toLowerCase())
  );

  <input
  type="text"
  placeholder="Search products..."
  value={search}
  onChange={(e) => setSearch(e.target.value)}
  className="w-full mb-8 p-4 rounded-2xl bg-white/5 border border-white/10 text-white"
/>

const addToCart = async (productId: number) => {

  const token = localStorage.getItem("token");

  if (!token) {
    alert("Please login first");
    return;
  }

  try {

    await axios.post(
      "http://127.0.0.1:8000/api/cart/add",
      {
        product_id: productId,
        quantity: 1
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert("Added to cart");

  } catch (error) {

    console.error(error);
    alert("Failed to add product");

  }
};

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white">
        Loading Products...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1120] p-10">

      <h1 className="text-5xl font-bold text-white mb-10">
        Products
      </h1>

      <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-8">

        {filteredProducts.map((product) => (

          <div
            key={product.product_id}
            className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl overflow-hidden hover:scale-105 transition duration-300"
          >

            <img
  src={
    `http://127.0.0.1:8000${product.image_url}`
  }
              alt={product.product_name}
              className="w-full h-56 object-cover"
            />

            <div className="p-5">

              <h2 className="text-white text-xl font-bold">
                {product.product_name}
              </h2>

              <p className="text-gray-400 mt-2">
                {product.description}
              </p>

              <p className="text-cyan-400 text-2xl font-bold mt-4">
                ₹{product.price}
              </p>

              <button
  onClick={() => addToCart(product.product_id)}
  className="w-full mt-5 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 text-white"
>
  Add To Cart
</button>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}