"use client";

import { type ReactNode, createContext, useCallback, useContext, useMemo } from "react";
import type {
  OrganizationPermissionCheck,
  OrganizationPermissions,
} from "@/lib/auth/organization-permissions";

type OrganizationPermissionContextValue = {
  permissions: OrganizationPermissions;
  can: (requiredPermissions: OrganizationPermissionCheck) => boolean;
};

const OrganizationPermissionContext = createContext<OrganizationPermissionContextValue | null>(
  null,
);

type OrganizationPermissionProviderProps = {
  children: ReactNode;
  permissions: OrganizationPermissions;
};

export function OrganizationPermissionProvider({
  children,
  permissions,
}: OrganizationPermissionProviderProps) {
  const can = useCallback(
    (requiredPermissions: OrganizationPermissionCheck) =>
      Object.entries(requiredPermissions).every(([resource, actions]) => {
        const grantedActions = permissions[resource as keyof OrganizationPermissions] as
          readonly string[] | undefined;
        const requiredActions = Array.isArray(actions) ? actions : [actions];

        return requiredActions.every((action) => grantedActions?.includes(action) ?? false);
      }),
    [permissions],
  );

  const value = useMemo(() => ({ permissions, can }), [can, permissions]);

  return <OrganizationPermissionContext value={value}>{children}</OrganizationPermissionContext>;
}

export function useOrganizationPermissions(): OrganizationPermissionContextValue {
  const context = useContext(OrganizationPermissionContext);

  if (!context) {
    throw new Error(
      "useOrganizationPermissions must be used within an OrganizationPermissionProvider",
    );
  }

  return context;
}
