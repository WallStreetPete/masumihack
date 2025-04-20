"use client";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface AudienceSearchProps {
  description: string;
  onDescriptionChange: (value: string) => void;
  onExampleClick: (example: string) => void;
  onNext: () => void;
}

export function AudienceSearch({
  description,
  onDescriptionChange,
  onExampleClick,
  onNext,
}: AudienceSearchProps) {
  const examples = [
    "Seed-stage investors focused on B2B SaaS with $500K-$1M check sizes",
    "Angel investors with experience in AI and machine learning startups",
    "Series A investors interested in companies with $10K+ MRR and proven product-market fit",
    "VCs specializing in enterprise software with $1M-$5M investments",
    "Strategic investors in the AI/ML space looking for companies with strong IP",
    "Early-stage investors interested in SaaS companies with 100%+ YoY growth",
  ];

  return (
    <div className="space-y-8">
      <Card className="p-6">
        <h2 className="text-2xl font-semibold mb-4">
          Find Your Target Audience
        </h2>
        <p className="text-muted-foreground">
          Describe the type of people you want to reach out to. Be specific
          about their interests, profession, location, or any other relevant
          characteristics that will help us find the perfect match for your
          campaign.
        </p>
      </Card>

      <div className="space-y-6">
        <div className="relative">
          <Textarea
            value={description}
            onChange={(e) => onDescriptionChange(e.target.value)}
            placeholder="Describe your target audience (e.g., Software engineers in San Francisco interested in AI)"
            className="min-h-[200px] text-lg p-4 resize-none bg-white"
          />
          <Button
            className="absolute right-4 bottom-4"
            size="lg"
            onClick={onNext}
          >
            Next
          </Button>
        </div>

        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground">
            Examples:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {examples.map((example, index) => (
              <div
                key={index}
                onClick={() => onExampleClick(example)}
                className="p-4 bg-white border rounded-xl cursor-pointer hover:bg-secondary/50 transition-colors duration-200"
              >
                {example}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
