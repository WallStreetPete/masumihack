"use client";

import { Scale } from "lucide-react";

interface LoadingStateProps {
  title: string;
  description: string;
}

export function LoadingState({ title, description }: LoadingStateProps) {
  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col items-center justify-center">
      <div className="relative">
        <Scale className="h-12 w-12 text-primary animate-bounce" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-24 w-24 border-4 border-primary rounded-full border-t-transparent animate-spin"></div>
      </div>
      <h2 className="mt-8 text-2xl font-semibold">{title}</h2>
      <p className="text-muted-foreground mt-2">{description}</p>
    </div>
  );
}