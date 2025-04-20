import { Prospect } from "@/globals/type";
import React from "react";

interface ProspectStackListProps {
  prospects: Prospect[];
  selectedProspectId: number | null;
  onSelect: (index: number) => void;
}

function getInitials(name: string) {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase();
}

export const ProspectStackList: React.FC<ProspectStackListProps> = ({
  prospects,
  selectedProspectId,
  onSelect,
}) => {
  return (
    <div className="h-full flex gap-1 flex-col w-72 overflow-y-auto overflow-x-auto min-h-[calc(100vh-4rem)] border-r">
      {prospects.map((prospect, index) => (
        <div
          key={prospect.linkedinUrl}
          className={`cursor-pointer px-3 py-2 shadow-sm transition-all h-28 flex flex-col justify-center ${
            selectedProspectId === index
              ? "bg-white dark:bg-gray-900 border-l-4 border-primary"
              : "bg-white border-l-4 border-transparent hover:bg-muted hover:dark:bg-gray-900"
          }`}
          onClick={() => onSelect(index)}
        >
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 min-w-10 min-h-10 flex-shrink-0 bg-primary/10 flex items-center justify-center font-bold text-primary text-lg rounded-full">
              {getInitials(prospect.firstName + " " + prospect.lastName)}
            </div>
            <div>
              <div className="font-semibold text-base">
                {prospect.firstName + " " + prospect.lastName}
              </div>
              <div className="text-xs text-muted-foreground">
                {prospect.title} @ {prospect.organizationName}
              </div>
            </div>
          </div>
          <div className="mt-3 text-xs text-muted-foreground italic truncate">
            {
              prospect?.emailMessages?.[prospect?.emailMessages?.length - 1]
                ?.text
            }
          </div>
        </div>
      ))}
    </div>
  );
};
