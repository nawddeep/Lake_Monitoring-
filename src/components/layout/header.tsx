"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

type HeaderProps = React.HTMLAttributes<HTMLElement> & {
  fixed?: boolean;
  shadowOnScroll?: boolean;
  ref?: React.Ref<HTMLElement>;
};

export function Header({
  className,
  fixed,
  shadowOnScroll = true,
  children,
  ...props
}: HeaderProps) {
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    if (!shadowOnScroll) return;

    const onScroll = () => {
      setOffset(document.body.scrollTop || document.documentElement.scrollTop);
    };

    // Add scroll listener to the body
    document.addEventListener("scroll", onScroll, { passive: true });

    // Clean up the event listener on unmount
    return () => document.removeEventListener("scroll", onScroll);
  }, [shadowOnScroll]);

  const hasScrolled = shadowOnScroll && offset > 10;

  return (
    <header
      className={cn(
        "z-50 h-16",
        fixed && "header-fixed peer/header sticky top-0 w-[inherit]",
        hasScrolled && fixed ? "shadow" : "shadow-none",
        className,
      )}
      {...props}
    >
      <div
        className={cn(
          "relative flex h-full items-center gap-3 p-4 sm:gap-4",
          hasScrolled &&
            fixed &&
            "after:absolute after:inset-0 after:-z-10 after:bg-background/20 after:backdrop-blur-lg",
        )}
      >
        {children}
      </div>
    </header>
  );
}
