import type { ReactNode } from "react";
import { InviteTeamMemberModal } from "./_components/invite-team-member-modal";
import { NavTabs } from "@/components/navigation/nav-tabs";
import { ContentLayout } from "@/components/platform/content-layout";

export default function MembersLayout({ children }: { children: ReactNode }) {
  return (
    <ContentLayout
      title="Admin Team"
      description="Manage your team members"
      actions={<InviteTeamMemberModal />}
    >
      <NavTabs
        tabs={[
          { label: "Members", href: "/admin/team" },
          { label: "Invitations", href: "/admin/team/invitations" },
        ]}
      />
      {children}
    </ContentLayout>
  );
}
