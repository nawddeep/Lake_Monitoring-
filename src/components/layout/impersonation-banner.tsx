"use client";

import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { authApi } from "@/services/api/auth/authApi";
import { Button } from "@/components/ui/button";

export function ImpersonationBanner({ userName }: { userName: string }) {
  const { mutate, isPending } = useMutation({
    mutationFn: authApi.stopImpersonating,
    onSuccess: () => window.location.assign("/admin/dashboard"),
    onError: () => toast.error("Failed to return to your admin session."),
  });

  return (
    <div className="fixed inset-x-0 top-4 z-[60] mx-auto flex w-fit max-w-[calc(100%-2rem)] items-center gap-3 rounded-lg border border-amber-300 bg-amber-50 px-4 py-2 text-sm text-amber-950 shadow-lg dark:border-amber-800 dark:bg-amber-950 dark:text-amber-50">
      <span>
        You are impersonating <strong>{userName}</strong>.
      </span>
      <Button
        className="cursor-pointer"
        size="sm"
        variant="outline"
        disabled={isPending}
        onClick={() => mutate()}
      >
        {isPending ? "Stopping..." : "Stop impersonating"}
      </Button>
    </div>
  );
}
