"use client";

import React, { useState } from "react";
import useDialogState from "@/hooks/use-dialog-state";
import type { User } from "@/types/user";

type MembersDialogType = "view" | "change-role" | "revoke-access";

type MembersContextType = {
  open: MembersDialogType | null;
  setOpen: (str: MembersDialogType | null) => void;
  currentRow: User | null;
  setCurrentRow: React.Dispatch<React.SetStateAction<User | null>>;
  currentUserId: string | null;
};

const MembersContext = React.createContext<MembersContextType | null>(null);

export function MembersProvider({
  children,
  currentUserId = null,
}: {
  children: React.ReactNode;
  currentUserId?: string | null;
}) {
  const [open, setOpen] = useDialogState<MembersDialogType>(null);
  const [currentRow, setCurrentRow] = useState<User | null>(null);

  return (
    <MembersContext value={{ open, setOpen, currentRow, setCurrentRow, currentUserId }}>
      {children}
    </MembersContext>
  );
}

export function useMembers() {
  const context = React.useContext(MembersContext);
  if (!context) throw new Error("useMembers has to be used within <MembersProvider>");
  return context;
}
