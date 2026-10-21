"use client";

import { Button } from "@/components/ui/button";

interface DestructiveButtonProps {
  onClick: () => void;
  isPending?: boolean;
  label?: string;
  pendingLabel?: string;
}

export function DestructiveButton({
  onClick,
  isPending = false,
  label = "Delete",
  pendingLabel = "Deleting...",
}: DestructiveButtonProps) {
  return (
    <Button variant="destructive" onClick={onClick} disabled={isPending}>
      {isPending ? pendingLabel : label}
    </Button>
  );
}
