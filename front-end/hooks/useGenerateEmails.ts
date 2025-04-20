// Hook for generateEmails API
import { useCallback } from "react";

export function useGenerateEmails() {
  return useCallback(async (data: any) => {
    const res = await fetch("/api/generateEmails", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return res.json();
  }, []);
}
