import React from "react";

export function EmailProgress({ progress = 0 }: { progress?: number }) {
  // Clamp progress to [0, 100]
  const barProgress = Math.max(0, Math.min(progress, 100));

  let mainText = "";
  let subText = "";

  if (barProgress < 95) {
    mainText = "Generating emails...";
    subText = "We're crafting personalized emails for your prospects";
  } else if (barProgress < 100) {
    mainText = "Almost done!";
    subText = "Finalizing email content...";
  } else {
    mainText = "Completed!";
    subText = "Emails are ready to review!";
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center">
      <div className="relative w-96">
        <div className="w-full bg-gray-200 rounded-full h-3 mb-4 overflow-hidden">
          <div
            className="bg-primary h-3 rounded-full"
            style={{
              width: `${barProgress}%`,
              transition: "width 2.2s cubic-bezier(0.4, 0, 0.2, 1)",
            }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500 w-full">
          <span className={barProgress < 95 ? "font-bold text-primary" : ""}>Generating</span>
          <span className={barProgress >= 95 && barProgress < 100 ? "font-bold text-primary" : ""}>Almost done</span>
          <span className={barProgress >= 100 ? "font-bold text-primary" : ""}>Complete</span>
        </div>
      </div>
      <h2 className="mt-8 text-2xl font-semibold text-center">{mainText}</h2>
      <p className="text-muted-foreground mt-2">{subText}</p>
    </div>
  );
}
