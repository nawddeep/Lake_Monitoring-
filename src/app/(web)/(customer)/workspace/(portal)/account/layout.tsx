import type { ReactNode } from "react";
import { NavTabs } from "@/components/navigation/nav-tabs";
import { ContentLayout } from "@/components/platform/content-layout";

export default function AccountLayout({ children }: { children: ReactNode }) {
  return (
    <ContentLayout title="Account" description="Manage your profile and settings.">
      <NavTabs
        tabs={[
          { label: "Profile", href: "/workspace/account" },
          { label: "Security", href: "/workspace/account/security" },
        ]}
      />
      {children}
    </ContentLayout>
  );
}
