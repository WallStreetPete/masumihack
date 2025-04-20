"use client";

import { Users, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Campaign } from "@/globals/type";

interface CampaignSidebarProps {
  campaigns: Campaign[];
  onNewCampaign: () => void;
  onSelectCampaign: (campaign: Campaign, index: number) => void;
  selectedCampaignId: number | null;
}

export function CampaignSidebar({
  campaigns,
  onNewCampaign,
  onSelectCampaign,
  selectedCampaignId,
}: CampaignSidebarProps) {
  console.log(campaigns);
  return (
    <div className="w-80 border-r p-4 hidden md:block">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h2 className="font-semibold">Campaigns</h2>
          </div>
          <Button
            size="sm"
            onClick={onNewCampaign}
            className="flex items-center gap-1"
          >
            <Plus className="h-4 w-4" />
            New
          </Button>
        </div>
        <div className="space-y-2">
          {campaigns.map((campaign, index) => {
            const isSelected = selectedCampaignId === index;
            return (
              <div
                key={campaign.title}
                onClick={() => onSelectCampaign(campaign, index)}
                className={`bg-white p-4 rounded-lg cursor-pointer transition-colors border min-h-[84px] h-[84px] flex flex-col justify-between ${
                  isSelected
                    ? "border-primary ring-2 ring-primary/40 bg-primary/10"
                    : "hover:bg-secondary"
                }`}
              >
                <div className="flex items-center justify-between mb-2 min-h-[1.5rem]">
                  <p className="font-medium text-sm">{campaign.title}</p>
                  {isSelected ? (
                    <span className="ml-2 px-2 py-0.5 text-xs rounded-full bg-primary text-white">
                      Selected
                    </span>
                  ) : (
                    // Render invisible badge for consistent height
                    <span className="ml-2 px-2 py-0.5 text-xs rounded-full opacity-0 select-none">
                      Selected
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Users className="h-3 w-3" />
                  <span>{campaign.prospects?.length ?? 0} prospects</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
