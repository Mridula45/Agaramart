"use client";

import ProtectedRoute from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import axios from "axios";

interface Address {
  address_id: number;
  full_name: string;
  phone: string;
  address_line: string;
  city: string;
  state: string;
  pincode: string;
  is_default: boolean;
}

export default function AddressPage() {

  const [addresses, setAddresses] =
    useState<Address[]>([]);

  const [fullName, setFullName] =
    useState("");

  const [phone, setPhone] =
    useState("");

  const [addressLine, setAddressLine] =
    useState("");

  const [city, setCity] =
    useState("");

  const [state, setState] =
    useState("");

  const [pincode, setPincode] =
    useState("");

  const [isDefault, setIsDefault] =
    useState(false);

  useEffect(() => {

    fetchAddresses();

  }, []);

  const fetchAddresses = async () => {

    try {

      const token =
        localStorage.getItem("token");

      const response =
        await axios.get(
          "http://127.0.0.1:8000/api/address",
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
          }
        );

      setAddresses(response.data);

    }

    catch (error) {

      console.error(error);

    }

  };

  const addAddress = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    try {

      const token =
        localStorage.getItem("token");

      await axios.post(
        "http://127.0.0.1:8000/api/address",
        {
          full_name: fullName,
          phone,
          address_line: addressLine,
          city,
          state,
          pincode,
          is_default: isDefault,
        },
        {
          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );

      setFullName("");
      setPhone("");
      setAddressLine("");
      setCity("");
      setState("");
      setPincode("");
      setIsDefault(false);

      fetchAddresses();

      alert("Address Added");

    }

    catch (error) {

      console.error(error);

      alert("Failed");

    }

  };

  const deleteAddress = async (
    id: number
  ) => {

    if (
      !confirm(
        "Delete this address?"
      )
    )
      return;

    try {

      const token =
        localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:8000/api/address/${id}`,
        {
          headers: {
            Authorization:
              `Bearer ${token}`,
          },
        }
      );

      fetchAddresses();

    }

    catch (error) {

      console.error(error);

    }

  };

  return (

    <ProtectedRoute allowedRoles={[1]}>

      <div className="min-h-screen bg-[#0B1120] text-white p-10">

        <h1 className="text-5xl font-bold mb-10">
          My Addresses
        </h1>

        <form
          onSubmit={addAddress}
          className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-10"
        >
              <div className="grid md:grid-cols-2 gap-5">

            <input
              type="text"
              placeholder="Full Name"
              value={fullName}
              onChange={(e) =>
                setFullName(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
              required
            />

            <input
              type="text"
              placeholder="Phone Number"
              value={phone}
              onChange={(e) =>
                setPhone(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
              required
            />

          </div>

          <textarea
            placeholder="Address Line"
            value={addressLine}
            onChange={(e) =>
              setAddressLine(e.target.value)
            }
            className="w-full mt-5 p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
            rows={3}
            required
          />

          <div className="grid md:grid-cols-3 gap-5 mt-5">

            <input
              type="text"
              placeholder="City"
              value={city}
              onChange={(e) =>
                setCity(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
              required
            />

            <input
              type="text"
              placeholder="State"
              value={state}
              onChange={(e) =>
                setState(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
              required
            />

            <input
              type="text"
              placeholder="Pincode"
              value={pincode}
              onChange={(e) =>
                setPincode(e.target.value)
              }
              className="p-4 rounded-xl bg-white/10 border border-white/10 outline-none"
              required
            />

          </div>

          <div className="flex items-center gap-3 mt-6">

            <input
              type="checkbox"
              checked={isDefault}
              onChange={(e) =>
                setIsDefault(e.target.checked)
              }
            />

            <label>
              Set as Default Address
            </label>

          </div>

          <button
            type="submit"
            className="mt-8 bg-gradient-to-r from-cyan-500 to-purple-600 px-8 py-4 rounded-2xl font-bold hover:scale-105 transition"
          >
            Add Address
          </button>

        </form>

        <h2 className="text-3xl font-bold mb-6">
          Saved Addresses
        </h2>

        <div className="grid lg:grid-cols-2 gap-6">

          {addresses.length === 0 ? (

            <div className="col-span-2 text-center py-10 text-gray-400">
              No addresses found.
            </div>

          ) : (

            addresses.map((address) => (

              <div
                key={address.address_id}
                className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl"
              >

                <div className="flex justify-between items-start">

                  <div>

                    <h3 className="text-2xl font-bold">
                      {address.full_name}
                    </h3>

                    <p className="text-gray-300 mt-2">
                      📞 {address.phone}
                    </p>

                    <p className="text-gray-400 mt-3">
                      {address.address_line}
                    </p>

                    <p className="text-gray-400">
                      {address.city}, {address.state}
                    </p>

                    <p className="text-gray-400">
                      {address.pincode}
                    </p>

                    {address.is_default && (

                      <span className="inline-block mt-4 bg-green-600 px-3 py-1 rounded-full text-sm">
                        ⭐ Default Address
                      </span>

                    )}

                  </div>

                </div>

                <div className="flex gap-4 mt-6">

                  <button
                    className="flex-1 bg-cyan-600 hover:bg-cyan-700 py-3 rounded-xl transition"
                  >
                    Deliver Here
                  </button>

                  <button
                    onClick={() =>
                      deleteAddress(address.address_id)
                    }
                    className="flex-1 bg-red-600 hover:bg-red-700 py-3 rounded-xl transition"
                  >
                    Delete
                  </button>

                </div>

              </div>

            ))

          )}

        </div>

      </div>

    </ProtectedRoute>

  );

}