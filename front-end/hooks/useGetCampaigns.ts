// Hook for getCampaigns API
import { useCallback } from "react";

export function useGetCampaigns() {
  return useCallback(async () => {
    const res = await fetch("/api/getCampaigns");
    const { campaigns } = await res.json();
    return campaigns;
  }, []);
}
