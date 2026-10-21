import type { ReactNode } from "react";
import { NavTabs } from "@/components/navigation/nav-tabs";
import { ContentLayout } from "@/components/platform/content-layout";
import { InviteMemberModal } from "@/app/(web)/(customer)/workspace/(portal)/members/_components/invite-member-modal";

export default function MembersLayout({ children }: { children: ReactNode }) {
  return (
    <ContentLayout
      title="Members"
      description="Manage workspace access for your organization."
      actions={<InviteMemberModal />}
    >
      <NavTabs
        tabs={[
          { label: "Members", href: "/workspace/members" },
          { label: "Invitations", href: "/workspace/members/invitations" },
        ]}
      />
      {children}
    </ContentLayout>
  );
}
