import { NextResponse } from "next/server";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { exec } from "child_process";
import { Prospect } from "@/globals/type";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const description = searchParams.get("description") as string;

    if (!description) {
      return NextResponse.json(
        { error: "Missing description" },
        { status: 400 }
      );
    }

    const { text } = await generateText({
      model: openai("o4-mini"),
      prompt: `Create a short title for this campign description ${description}. Only return the short description. Keep it short`,
    });

    const campaignTitle = text;
    const formattedProspects = await getProspects(description);

    return NextResponse.json({ prospects: formattedProspects, campaignTitle });
  } catch (error) {
    console.log(error);
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 500 }
    );
  }
}

// function to return prospects
export async function getProspects(description: string) {
  const curlCommand = `curl -X POST http://localhost:8000/start_job \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d '${JSON.stringify({ text: description })}'`;

  //   // First request: start_job
  const startJobResponse = await new Promise<any>((resolve, reject) => {
    exec(curlCommand, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      try {
        const json = JSON.parse(stdout);
        resolve(json);
      } catch (parseError) {
        reject(parseError);
      }
    });
  });

  if (!startJobResponse || !startJobResponse.job_id) {
    throw new Error("Failed to get job_id from start_job response");
  }

  // Second request: status with job_id
  const statusCurlCommand = `curl -X GET 'http://localhost:8000/status?job_id=${startJobResponse.job_id}' -H 'accept: application/json'`;

  const prospects = await new Promise<any>((resolve, reject) => {
    exec(statusCurlCommand, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      try {
        const json = JSON.parse(stdout);
        resolve(json);
      } catch (parseError) {
        reject(parseError);
      }
    });
  });

  const toJson = JSON.parse(prospects.result.tasks_output[0].raw);

  const formattedProspects: Prospect[] = toJson.map((prospect: any) => ({
    firstName: prospect.first_name,
    lastName: prospect.last_name,
    title: prospect.title,
    seniority: prospect.seniority,
    organizationName: prospect.organization_name,
    linkedinUrl: prospect.linkedin_url,
    email:
      prospect.email === "email_not_unlocked@domain.com"
        ? Math.random() < 0.5
          ? `${prospect.first_name.toLowerCase()}@${prospect.organization_name
              .replace(/\s+/g, "")
              .toLowerCase()}.com`
          : "N/A"
        : prospect.email,
    description: prospect.description,
    emailMessages: [],
  }));

  return formattedProspects;
}
