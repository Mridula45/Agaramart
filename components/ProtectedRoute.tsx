"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

interface Props {
  children: React.ReactNode;
  allowedRoles: number[];
}

export default function ProtectedRoute({
  children,
  allowedRoles,
}: Props) {

  const { user, loading } = useAuth();

  const router = useRouter();

  useEffect(() => {

    if (loading) return;

    if (!user) {
      router.replace("/login");
      return;
    }

    if (
      !allowedRoles.includes(
        user.role_id
      )
    ) {

      router.replace("/");

    }

  }, [user, loading]);

  if (loading)
    return (
      <div className="min-h-screen flex justify-center items-center bg-[#0B1120] text-white">
        Loading...
      </div>
    );

  if (!user) return null;

  if (
    !allowedRoles.includes(
      user.role_id
    )
  )
    return null;

  return <>{children}</>;
}