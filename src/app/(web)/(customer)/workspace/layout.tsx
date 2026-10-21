import type { ReactNode } from "react";
import { requireSession } from "@/lib/auth/session";
import { ImpersonationBanner } from "@/components/layout/impersonation-banner";

export default async function WorkspaceLayout({ children }: { children: ReactNode }) {
  const session = await requireSession();

  return (
    <>
      {session.session.impersonatedBy && <ImpersonationBanner userName={session.user.name} />}
      {children}
    </>
  );
}
