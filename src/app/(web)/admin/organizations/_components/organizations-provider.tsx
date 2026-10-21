"use client";

import React, { useState } from "react";
import useDialogState from "@/hooks/use-dialog-state";
import type { Organization } from "@/types/organization";

type OrganizationDialogType = "edit" | "delete";

type OrganizationsContextValue = {
  open: OrganizationDialogType | null;
  setOpen: (value: OrganizationDialogType | null) => void;
  currentOrganization: Organization | null;
  setCurrentOrganization: React.Dispatch<React.SetStateAction<Organization | null>>;
};

const OrganizationsContext = React.createContext<OrganizationsContextValue | null>(null);

export function OrganizationsProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useDialogState<OrganizationDialogType>(null);
  const [currentOrganization, setCurrentOrganization] = useState<Organization | null>(null);

  return (
    <OrganizationsContext value={{ open, setOpen, currentOrganization, setCurrentOrganization }}>
      {children}
    </OrganizationsContext>
  );
}

export function useOrganizations() {
  const context = React.useContext(OrganizationsContext);
  if (!context) {
    throw new Error("useOrganizations must be used within <OrganizationsProvider>");
  }
  return context;
}
