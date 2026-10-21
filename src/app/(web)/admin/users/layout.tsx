import type { ReactNode } from "react";
import { ContentLayout } from "@/components/platform/content-layout";

export default function UsersLayout({ children }: { children: ReactNode }) {
  return (
    <ContentLayout title="Users" description="Manage users across the platform.">
      {children}
    </ContentLayout>
  );
}
