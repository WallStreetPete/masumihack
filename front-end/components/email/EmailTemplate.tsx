"use client";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface EmailTemplateProps {
  emailTemplate: string;
  onEmailTemplateChange: (value: string) => void;
  emailStyle: string;
  onEmailStyleChange: (value: string) => void;
  emailLength: string;
  onEmailLengthChange: (value: string) => void;
  emailTone: string;
  onEmailToneChange: (value: string) => void;
  selectedCount: number;
  onGenerateEmails: () => void;
}

export function EmailTemplate({
  emailTemplate,
  onEmailTemplateChange,
  emailStyle,
  onEmailStyleChange,
  emailLength,
  onEmailLengthChange,
  emailTone,
  onEmailToneChange,
  selectedCount,
  onGenerateEmails,
}: EmailTemplateProps) {
  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Create Email Template</h2>

      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium mb-2 bg-white">Key Points</h3>
          <Textarea
            value={emailTemplate}
            onChange={(e) => onEmailTemplateChange(e.target.value)}
            placeholder={`- Main value proposition

- Key metrics and growth

- Specific ask or next steps

- Relevant experience or connection`}
            className="min-h-[200px] mb-4 font-mono bg-white"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium">Style</label>
            <Select value={emailStyle} onValueChange={onEmailStyleChange}>
              <SelectTrigger className="mt-2">
                <SelectValue placeholder="Select style" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="auto">Auto</SelectItem>
                <SelectItem value="direct">Direct</SelectItem>
                <SelectItem value="narrative">Narrative</SelectItem>
                <SelectItem value="problem-solution">
                  Problem-Solution
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="cursor-pointer">
            <label className="text-sm font-medium">Length</label>
            <Select value={emailLength} onValueChange={onEmailLengthChange}>
              <SelectTrigger className="mt-2">
                <SelectValue placeholder="Select length" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="auto">Auto</SelectItem>
                <SelectItem value="short">Short</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="long">Long</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="bg-white p-1 rounded">
            <label className="text-sm font-medium">Tone</label>
            <Select value={emailTone} onValueChange={onEmailToneChange}>
              <SelectTrigger className="mt-2">
                <SelectValue placeholder="Select tone" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="auto">Auto</SelectItem>
                <SelectItem value="professional">Professional</SelectItem>
                <SelectItem value="friendly">Friendly</SelectItem>
                <SelectItem value="formal">Formal</SelectItem>
                <SelectItem value="casual">Casual</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <Button
          className="w-full mt-6"
          size="lg"
          onClick={onGenerateEmails}
          disabled={!emailTemplate.trim() || selectedCount === 0}
        >
          Generate Emails ({selectedCount})
        </Button>
      </div>
    </Card>
  );
}
