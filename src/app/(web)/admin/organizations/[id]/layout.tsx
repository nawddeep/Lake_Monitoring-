import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { findById } from "@/repositories/admin/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { ContentLayout } from "@/components/platform/content-layout";
import { OrganizationSummary } from "@/app/(web)/admin/organizations/[id]/_components/organization-summary";
import { OrganizationTabs } from "@/app/(web)/admin/organizations/[id]/_components/organization-tabs";
import { InviteOrganizationMemberModal } from "@/app/(web)/admin/organizations/[id]/invitations/_components/invite-organization-member-modal";

export default async function OrganizationLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const organization = await findById(id);
  if (!organization) {
    notFound();
  }

  const serializedOrganization = serializeOrganization(organization);

  return (
    <ContentLayout
      title={serializedOrganization.name}
      backHref="/admin/organizations"
      actions={<InviteOrganizationMemberModal organizationId={serializedOrganization.id} />}
    >
      <div className="space-y-8">
        <OrganizationSummary organization={serializedOrganization} />

        <OrganizationTabs organizationId={serializedOrganization.id}>{children}</OrganizationTabs>
      </div>
    </ContentLayout>
  );
}
