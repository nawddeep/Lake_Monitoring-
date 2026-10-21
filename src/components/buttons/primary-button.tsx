"use client";

import { Button } from "@/components/ui/button";

interface PrimaryButtonProps {
  children: React.ReactNode;
  isPending?: boolean;
  pendingLabel?: string;
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
  className?: string;
  disabled?: boolean;
}

export function PrimaryButton({
  children,
  isPending = false,
  pendingLabel,
  type = "button",
  onClick,
  className,
  disabled,
}: PrimaryButtonProps) {
  return (
    <Button type={type} onClick={onClick} disabled={isPending || disabled} className={className}>
      {isPending && pendingLabel ? pendingLabel : children}
    </Button>
  );
}
