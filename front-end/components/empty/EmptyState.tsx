"use client";

import { Users, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  onCreateNew: () => void;
}

export function EmptyState({ onCreateNew }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-[calc(100vh-8rem)]">
      <Users className="h-16 w-16 text-muted-foreground/30 mb-4" />
      <h3 className="text-xl font-medium text-muted-foreground">Select a campaign or create a new one</h3>
      <Button 
        className="mt-4"
        onClick={onCreateNew}
      >
        <Plus className="h-4 w-4 mr-2" />
        Create New Outreach
      </Button>
    </div>
  );
}