"use client";

import { type ReactNode, createContext, useCallback, useContext, useMemo } from "react";
import type { AdminPermissionCheck, AdminPermissions } from "@/lib/auth/admin-permissions";

type AdminPermissionContextValue = {
  permissions: AdminPermissions;
  can: (requiredPermissions: AdminPermissionCheck) => boolean;
};

const AdminPermissionContext = createContext<AdminPermissionContextValue | null>(null);

type AdminPermissionProviderProps = {
  children: ReactNode;
  permissions: AdminPermissions;
};

export function AdminPermissionProvider({ children, permissions }: AdminPermissionProviderProps) {
  const can = useCallback(
    (requiredPermissions: AdminPermissionCheck) =>
      Object.entries(requiredPermissions).every(([resource, actions]) => {
        const grantedActions = permissions[resource as keyof AdminPermissions] as
          readonly string[] | undefined;
        const requiredActions = Array.isArray(actions) ? actions : [actions];

        return requiredActions.every((action) => grantedActions?.includes(action) ?? false);
      }),
    [permissions],
  );

  const value = useMemo(() => ({ permissions, can }), [can, permissions]);

  return <AdminPermissionContext value={value}>{children}</AdminPermissionContext>;
}

export function useAdminPermissions(): AdminPermissionContextValue {
  const context = useContext(AdminPermissionContext);

  if (!context) {
    throw new Error("useAdminPermissions must be used within an AdminPermissionProvider");
  }

  return context;
}
