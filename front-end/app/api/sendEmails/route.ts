// app/api/sendEmails/route.ts

import { NextRequest, NextResponse } from "next/server";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL!);

type MyRequestBody = { name: string };

export async function POST(req: NextRequest) {
  try {
    const body: MyRequestBody = await req.json();
    const timestamp = Date.now();

    const redisKey = `sendEmails:${timestamp}`;

    await redis.set(redisKey, JSON.stringify(body));

    return NextResponse.json({
      response: `Saved to redis with key ${redisKey}`,
    });
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 500 }
    );
  }
}
