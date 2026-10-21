"use client";

import React, { useState } from "react";
import useDialogState from "@/hooks/use-dialog-state";
import type { Member } from "@/types/member";

type OrganizationMembersDialogType = "view" | "change-role" | "remove";

type OrganizationMembersContextType = {
  open: OrganizationMembersDialogType | null;
  setOpen: (value: OrganizationMembersDialogType | null) => void;
  currentMember: Member | null;
  setCurrentMember: React.Dispatch<React.SetStateAction<Member | null>>;
  organizationId: string;
  currentUserId: string;
};

const OrganizationMembersContext = React.createContext<OrganizationMembersContextType | null>(null);

export function OrganizationMembersProvider({
  children,
  organizationId,
  currentUserId,
}: {
  children: React.ReactNode;
  organizationId: string;
  currentUserId: string;
}) {
  const [open, setOpen] = useDialogState<OrganizationMembersDialogType>(null);
  const [currentMember, setCurrentMember] = useState<Member | null>(null);

  return (
    <OrganizationMembersContext
      value={{
        open,
        setOpen,
        currentMember,
        setCurrentMember,
        organizationId,
        currentUserId,
      }}
    >
      {children}
    </OrganizationMembersContext>
  );
}

export function useOrganizationMembers() {
  const context = React.useContext(OrganizationMembersContext);
  if (!context) {
    throw new Error("useOrganizationMembers has to be used within <OrganizationMembersProvider>");
  }
  return context;
}
