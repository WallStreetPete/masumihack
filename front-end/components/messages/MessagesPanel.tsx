import React, { useState } from "react";
import { ArrowRight } from "lucide-react";

export interface Message {
  id: string;
  sender: "me" | "prospect";
  text: string;
  timestamp: string;
}

interface MessagesPanelProps {
  messages: Message[];
  prospectName: string;
  name: string;
  onSend?: (text: string) => void;
}

export const MessagesPanel: React.FC<MessagesPanelProps> = ({
  messages,
  prospectName,
  name,
  onSend,
}) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSend?.(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="h-full flex flex-col p-6 min-h-[calc(100vh-4rem)]">
      <div className="font-semibold text-lg mb-4">Conversation with {name}</div>
      <div className="flex-1 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.sender === "me" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`relative rounded-lg px-4 py-2 max-w-xs break-words border text-sm bg-white ${
                msg.sender === "me" ? "text-black" : "text-gray-900"
              }`}
            >
              {msg.text}
              <div className="text-[10px] text-muted-foreground mt-1 text-right">
                {msg.timestamp}
              </div>
              {/* Bubble tail */}
              
            </div>
          </div>
        ))}
      </div>
      <form
        className="flex items-center gap-2 mt-6"
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
      >
        <div className="relative flex-1">
          <textarea
            className="w-full h-40 rounded-2xl border border-gray-300 dark:border-gray-700 pr-16 pl-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary bg-white dark:bg-gray-900 text-base resize-none"
            placeholder={`Send a message to ${prospectName}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              } else if (e.key === "Tab") {
                e.preventDefault();
                const textarea = e.target as HTMLTextAreaElement;
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                setInput(
                  (prev) =>
                    prev.substring(0, start) + "\t" + prev.substring(end)
                );
                setTimeout(() => {
                  textarea.selectionStart = textarea.selectionEnd = start + 1;
                }, 0);
              }
            }}
          />
          <button
            type="submit"
            className="absolute top-1/2 right-4 -translate-y-1/2 rounded-full bg-primary text-white flex items-center justify-center h-10 w-10 hover:bg-primary/90 transition-colors disabled:opacity-50 shadow-md"
            disabled={!input.trim()}
            aria-label="Send"
          >
            <ArrowRight className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
