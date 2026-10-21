"use client";

import React, { useState } from "react";
import useDialogState from "@/hooks/use-dialog-state";
import type { Member } from "@/types/member";

type DialogType = "view" | "change-role" | "remove";

type MembersContextValue = {
  open: DialogType | null;
  setOpen: (value: DialogType | null) => void;
  currentMember: Member | null;
  setCurrentMember: React.Dispatch<React.SetStateAction<Member | null>>;
  currentUserId: string;
};

const MembersContext = React.createContext<MembersContextValue | null>(null);

export function MembersProvider({
  children,
  currentUserId,
}: {
  children: React.ReactNode;
  currentUserId: string;
}) {
  const [open, setOpen] = useDialogState<DialogType>(null);
  const [currentMember, setCurrentMember] = useState<Member | null>(null);

  return (
    <MembersContext value={{ open, setOpen, currentMember, setCurrentMember, currentUserId }}>
      {children}
    </MembersContext>
  );
}

export function useMembers() {
  const context = React.useContext(MembersContext);
  if (!context) throw new Error("useMembers must be used within MembersProvider.");
  return context;
}
