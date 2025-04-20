"use client";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Pencil } from "lucide-react";
import { Prospect } from "@/globals/type";

interface GeneratedEmailsProps {
  prospects: Prospect[];
  showEmailEditor: number | null;
  onShowEditor: (index: number | null) => void;
  onUpdateEmail: (index: number, content: string) => void;
  onSaveUpdateEmail: () => void;
  sendEmails: () => void;
}

export function GeneratedEmails({
  prospects,
  showEmailEditor,
  onShowEditor,
  onUpdateEmail,
  onSaveUpdateEmail,
  sendEmails,
}: GeneratedEmailsProps) {
  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-semibold">Generated Emails</h1>
          <p className="text-muted-foreground mt-1">
            Review and edit your emails before sending
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {prospects.map((p, index) => (
          <div key={p.linkedinUrl} className="border rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="font-medium">
                  {p.firstName + " " + p.lastName}
                </h3>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onShowEditor(index)}
              >
                <Pencil className="h-4 w-4" />
              </Button>
            </div>

            {showEmailEditor === index ? (
              <div className="mt-2">
                <Textarea
                  value={p.emailMessages[0].text}
                  onChange={(e) => onUpdateEmail(index, e.target.value)}
                  className="min-h-[150px]"
                />
                <div className="flex justify-end gap-2 mt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onShowEditor(null)}
                  >
                    Cancel
                  </Button>
                  <Button size="sm" onClick={onSaveUpdateEmail}>
                    Save
                  </Button>
                </div>
              </div>
            ) : (
              <p className="mt-2 text-sm whitespace-pre-wrap">
                {p.emailMessages[0].text}
              </p>
            )}
          </div>
        ))}
      </div>

      <Button className="w-full mt-6" size="lg" onClick={sendEmails}>
        Send Emails ({prospects.length})
      </Button>
    </Card>
  );
}
