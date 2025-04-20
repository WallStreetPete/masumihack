// app/api/sendEmails/route.ts

import { NextRequest, NextResponse } from "next/server";

import type { Prospect, Campaign } from "@/globals/type";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

export async function POST(req: NextRequest) {
  try {
    const { prospects, emailTone, emailLength, emailStyle, emailContext } =
      await req.json();

    const formattedProspects: Prospect[] = [];

    for (const prospect of prospects) {
      const text = await generateEmails(
        prospect,
        emailTone,
        emailLength,
        emailStyle,
        emailContext
      );

      formattedProspects.push({
        ...prospect,
        emailMessages: [{ from: "me", text }],
      });
    }

    return NextResponse.json({ prospects: formattedProspects });
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 500 }
    );
  }
}

const generateEmails = async (
  prospect: Prospect,
  emailTone: string,
  emailLength: string,
  emailStyle: string,
  emailContext: string
) => {
  const { text } = await generateText({
    model: openai("o4-mini"),
    prompt: `You are an expert email copywriter. Write a personalized email for each prospect in the following list. Use the specified tone, length, style, and context.
              Prospect: ${JSON.stringify(prospect)}
              Email Tone: ${emailTone}
              Email Length: ${emailLength}
              Email Style: ${emailStyle}
              Email Context: ${emailContext}
  
              Instructions:
              - Address each prospect by their name.
              - Tailor the email content to the prospect’s background or company if information is provided.
              - Follow the requested tone, length, and style.
              - Ensure the email is relevant to the provided context.
              - Output each email as a separate object with the prospect's name and the generated email.

              Only include the content of the email, nothing else. Do not add any additional text. Only return text, nothing else. Do not return a json
              Simply return the text, fill in the blanks with the info from prospects. Please add in the name as Peter Lu and the company as Autonmonton. 
              Name 
              Company 

              and that's it
  
              Generate the emails now.`,
  });
  return text;
};
