import { NextResponse } from "next/server";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL!);

export async function GET() {
  try {
    console.log("Fetching emails from redis...");
    const keys = await redis.keys("sendEmails:*");
    const values = keys.length > 0 ? await redis.mget(...keys) : [];
    const campaigns = values
      .map((val) => (val ? JSON.parse(val) : null))
      .filter(Boolean);

    console.log(campaigns);

    return NextResponse.json({ campaigns });
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 500 }
    );
  }
}
