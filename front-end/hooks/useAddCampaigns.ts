// Hook for addCampaigns API
import { useCallback } from "react";

export function useAddCampaigns() {
  return useCallback(async (data: any) => {
    const res = await fetch("/api/addCampaigns", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return res.json();
  }, []);
}
