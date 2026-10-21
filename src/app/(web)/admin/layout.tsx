import { redirect } from "next/navigation";
import type { ReactNode } from "react";
import { getAdminPermissions } from "@/lib/auth/admin-permissions";
import { requireSession } from "@/lib/auth/session";
import { serializeUser } from "@/serializers/userSerializer";
import { AppShell } from "@/components/layout/app-shell";
import { Header } from "@/components/layout/header";
import { ImpersonationBanner } from "@/components/layout/impersonation-banner";
import { Sidebar } from "@/app/(web)/admin/_components/sidebar";
import { AdminPermissionProvider } from "@/context/admin-permission-provider";

function hasAdminPortalAccess(role?: string | null): boolean {
  return role != null;
}

export default async function AdminLayout({ children }: { children: ReactNode }) {
  const session = await requireSession();

  if (!hasAdminPortalAccess(session.user.role)) {
    redirect("/unauthorized");
  }

  const user = serializeUser(session.user);
  const permissions = getAdminPermissions(session.user.role);

  return (
    <AdminPermissionProvider permissions={permissions}>
      {session.session.impersonatedBy && <ImpersonationBanner userName={session.user.name} />}
      <AppShell header={<Header fixed shadowOnScroll={false} />} sidebar={<Sidebar user={user} />}>
        {children}
      </AppShell>
    </AdminPermissionProvider>
  );
}
