"use client";

import { ApiError } from "@/services/api/client";

type Props = {
  isError: boolean;
  error: Error | null;
  fallback?: string;
};

export function MutationError({
  isError,
  error,
  fallback = "Something went wrong. Please try again.",
}: Props) {
  if (!isError || !error) return null;

  if (error instanceof ApiError && error.status === 400 && error.details?.length) {
    return (
      <ul className="space-y-1">
        {error.details.map((detail, i) => (
          <li key={i} className="text-sm text-destructive">
            {detail.message}
          </li>
        ))}
      </ul>
    );
  }

  return <p className="text-sm text-destructive">{fallback}</p>;
}
