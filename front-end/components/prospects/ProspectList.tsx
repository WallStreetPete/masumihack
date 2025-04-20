"use client";

import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Prospect } from "@/globals/type";

interface ProspectListProps {
  prospects: Prospect[];
  selectedProspects: Prospect[];
  onToggleProspect: (p: Prospect) => void;
  onToggleAll: () => void;
}

export function ProspectList({
  prospects,
  selectedProspects,
  onToggleProspect,
  onToggleAll,
}: ProspectListProps) {
  console.log(prospects);

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-semibold">Found Prospects</h1>
          <p className="text-muted-foreground mt-1">
            Select the prospects you want to reach out to
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-4 px-4">
                <Checkbox
                  checked={selectedProspects.length === prospects.length}
                  onCheckedChange={onToggleAll}
                />
              </th>
              <th className="text-left py-4 px-4 font-medium">Name</th>
              <th className="text-left py-4 px-4 font-medium">Company</th>
              <th className="text-left py-4 px-4 font-medium">
                Title/Seniority
              </th>
              <th className="text-left py-4 px-4 font-medium">Email</th>
              <th className="text-left py-4 px-4 font-medium">LinkedIn</th>
            </tr>
          </thead>
          <tbody>
            {prospects.map((prospect) => (
              <tr
                key={prospect.linkedinUrl}
                className="border-b hover:bg-muted/50 transition-colors"
              >
                <td className="py-4 px-4">
                  <Checkbox
                    checked={selectedProspects.includes(prospect)}
                    onCheckedChange={() => onToggleProspect(prospect)}
                  />
                </td>
                <td className="py-4 px-4 font-medium">
                  {prospect.firstName + " " + prospect.lastName}
                </td>
                <td className="py-4 px-4 font-medium">
                  {prospect.organizationName}
                </td>
                <td className="py-4 px-4">
                  {(() => {
                    const title = prospect.title
                      ? prospect.title.charAt(0).toUpperCase() +
                        prospect.title.slice(1)
                      : null;
                    const seniority = prospect.seniority
                      ? prospect.seniority.charAt(0).toUpperCase() +
                        prospect.seniority.slice(1)
                      : null;
                    if (title && seniority) return `${title} / ${seniority}`;
                    if (title) return title;
                    if (seniority) return seniority;
                    return "N/A";
                  })()}
                </td>
                <td className="py-4 px-4 font-medium">
                  {prospect.email ? prospect.email : "N/A"}
                </td>
                <td className="py-4 px-4 font-medium">
                  {prospect.linkedinUrl ? prospect.linkedinUrl : "N/A"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
