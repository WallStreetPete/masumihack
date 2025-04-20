// Hook for searchProspects API
import { useCallback } from "react";

export function useSearchProspects() {
  return useCallback(async (description: string) => {
    const params = new URLSearchParams({ description });
    const res = await fetch(`/api/getProspects?${params.toString()}`);

    const { prospects, campaignTitle } = await res.json();

    return { prospects, campaignTitle };
  }, []);
}
