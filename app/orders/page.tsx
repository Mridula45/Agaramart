"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Order {
  order_id: number;
  total_amount: number;
  status: string;
  payment_status: string;
}

export default function OrdersPage() {

  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetchOrders();
  }, []);

  const proceedToPayment = async (orderId: number) => {

  try {

    const token = localStorage.getItem("token");

    const response = await axios.post(
      `http://127.0.0.1:8000/api/payment/create-order/${orderId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    console.log(response.data);

    alert(
      `Razorpay Order Created: ${response.data.razorpay_order_id}`
    );

  } catch (error) {

    console.error(error);
    alert("Payment initialization failed");

  }
};

  const fetchOrders = async () => {

    try {

      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/api/orders/my-orders",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setOrders(response.data);

    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1120] p-10">

      <h1 className="text-5xl font-bold text-white mb-10">
        My Orders
      </h1>

      <div className="space-y-5">

        {orders.map((order) => (

          <div
            key={order.order_id}
            className="bg-white/5 border border-white/10 rounded-2xl p-5"
          >
            <h2 className="text-white text-xl">
              Order #{order.order_id}
            </h2>

            <p className="text-gray-400">
              Amount: ₹{order.total_amount}
            </p>

            <p className="text-cyan-400">
              Status: {order.status}
            </p>

            <p className="text-purple-400">
              Payment: {order.payment_status}
            </p>
            <button
  onClick={() => proceedToPayment(order.order_id)}
  className="mt-4 px-5 py-2 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 text-white"
>
  Proceed To Pay
</button>

{order.payment_status !== "Paid" && (
  <button
    onClick={() => proceedToPayment(order.order_id)}
    className="mt-4 px-5 py-2 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 text-white"
  >
    Proceed To Pay
  </button>
)}

          </div>

        ))}

      </div>

    </div>
  );
}