"use client";

import { useRouter } from "next/navigation";
import { createClient } from "../src/utils/supabase/client";

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = async () => {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/login");
    router.refresh();
  };

  return (
    <button
      type="button"
      onClick={handleLogout}
      className="bg-transparent border-0 p-0 text-inherit cursor-pointer font-inherit"
    >
      Logout
    </button>
  );
}