// Hook for sendEmails API
import { Campaign } from "@/globals/type";
import { useCallback } from "react";

export function useSendEmails() {
  return useCallback(async (payload: Campaign) => {
    const res = await fetch("/api/sendEmails", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.json();
  }, []);
}
