import { redirect } from "next/navigation";
import { requireSession } from "@/lib/auth/session";
import { findOrganizationById } from "@/repositories/customers/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { ContentLayout } from "@/components/platform/content-layout";
import { OrganizationSummary } from "@/app/(web)/(customer)/workspace/(portal)/organization/_components/organization-summary";

export default async function OrganizationPage() {
  const session = await requireSession();
  const organizationId = session.session.activeOrganizationId;

  if (!organizationId) {
    redirect("/workspace/select-organization");
  }

  const organization = await findOrganizationById(organizationId);
  if (!organization) {
    redirect("/workspace/no-organization");
  }

  return (
    <ContentLayout
      title="Organization"
      description="Review the organization details for this workspace."
    >
      <OrganizationSummary organization={serializeOrganization(organization)} />
    </ContentLayout>
  );
}
