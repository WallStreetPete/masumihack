"use client";

import { Scale, Wallet } from "lucide-react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import React, { useEffect, useState } from "react";

export function Navbar() {
  const walletAddress =
    "addr_test1qru52hurwws02w9kygpw7m4u53sp3p6rxz56hrsz0r8ulmjmuj66yqjne4zrjjzpkume8j0mmugug8j2duwcxrlz5ffqmdspv4";
  const [balance, setBalance] = useState<number | null>(null);

  useEffect(() => {
    async function fetchBalance() {
      try {
        const res = await fetch(
          `https://cardano-preprod.blockfrost.io/api/v0/addresses/${walletAddress}`,
          {
            headers: {
              project_id: "preprodlvWXtnmJtSKQbOuh87p7tqz3qEo13IEm",
            },
          }
        );
        if (!res.ok) return;
        const data = await res.json();
        // Find the ADA balance (lovelace)
        const lovelace = data.amount?.find(
          (a: any) => a.unit === "lovelace"
        )?.quantity;
        if (lovelace) {
          setBalance(Number(lovelace) / 1_000_000);
        } else {
          setBalance(0);
        }
      } catch {
        setBalance(null);
      }
    }
    fetchBalance();
  }, [walletAddress]);

  return (
    <nav className="border-b dark:bg-gray-900">
      <div className="flex justify-between h-16 items-center px-2 sm:px-4 lg:px-6">
        <div className="flex items-center">
          <Image
            src="/logo.png"
            alt="ScaleUp Logo"
            width={144}
            height={144}
            className="h-36 w-36 object-contain"
            priority
          />
        </div>
        <div className="flex items-center gap-4">
          <div className="p-2 rounded-lg flex items-center">
            <Wallet className="h-5 w-5 text-primary mr-2" />
            <span className="font-medium">
              {balance !== null
                ? `₳${balance.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}`
                : "₳--"}
            </span>
          </div>
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="default" className="w-md">
                Top Up
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Top Up Your Account</DialogTitle>
                <DialogDescription>
                  Please send ADA to the following address:
                </DialogDescription>
              </DialogHeader>
              <div className="flex flex-col space-y-4">
                <div className="bg-muted p-4 rounded-lg break-all font-mono text-sm">
                  {walletAddress}
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>
    </nav>
  );
}
