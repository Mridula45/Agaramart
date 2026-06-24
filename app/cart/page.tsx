"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface CartItem {
  cart_item_id: number;
  product_id: number;
  quantity: number;
}

export default function CartPage() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
const placeOrder = async () => {
  try {
    const token = localStorage.getItem("token");

    const response = await axios.post(
      "http://127.0.0.1:8000/api/orders/place",
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    alert(
      `Order placed successfully! Order ID: ${response.data.order_id}`
    );

  } catch (error) {
    console.error(error);
    alert("Failed to place order");
  }
};
  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/api/cart",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setCartItems(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const removeItem = async (cartItemId: number) => {
    try {
      const token = localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:8000/api/cart/remove/${cartItemId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      fetchCart();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1120] p-10">
      <h1 className="text-5xl font-bold text-white mb-10">
        My Cart
      </h1>

      <div className="space-y-5">

        {cartItems.length === 0 ? (
          <p className="text-gray-400">
            Cart is empty
          </p>
        ) : (
          cartItems.map((item) => (
            <div
              key={item.cart_item_id}
              className="bg-white/5 border border-white/10 rounded-2xl p-5 flex justify-between items-center"
            >
              <div>
                <h2 className="text-white text-xl">
                  Product ID: {item.product_id}
                </h2>

                <p className="text-gray-400">
                  Quantity: {item.quantity}
                </p>
              </div>

              <button
                onClick={() =>
                  removeItem(item.cart_item_id)
                }
                className="bg-red-500 px-4 py-2 rounded-xl text-white"
              >
                Remove
              </button>
            </div>
          ))
        )}
<button
  onClick={placeOrder}
  className="mt-8 px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-600 text-white"
>
  Place Order
</button>
      </div>
    </div>
  );
}

