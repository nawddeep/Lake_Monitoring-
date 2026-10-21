"use client";

import { Button } from "@/components/ui/button";

interface CancelButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export function CancelButton({ onClick, disabled }: CancelButtonProps) {
  return (
    <Button type="button" variant="outline" onClick={onClick} disabled={disabled}>
      Cancel
    </Button>
  );
}
