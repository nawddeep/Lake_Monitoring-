import { redirect } from "next/navigation";
import { requireSession } from "@/lib/auth/session";
import { listUserOrganizations } from "@/repositories/customers/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { ContentLayout } from "@/components/platform/content-layout";
import { OrganizationSelector } from "@/app/(web)/(customer)/workspace/select-organization/_components/organization-selector";

export default async function SelectOrganizationPage() {
  const session = await requireSession();
  const organizations = await listUserOrganizations(session.user.id);

  if (organizations.length === 0) {
    redirect("/workspace/no-organization");
  }

  if (
    session.session.activeOrganizationId &&
    organizations.some((organization) => organization.id === session.session.activeOrganizationId)
  ) {
    redirect("/workspace");
  }

  const serializedOrganizations = organizations.map(serializeOrganization);

  return (
    <ContentLayout
      title="Choose an organization"
      description="Select the organization you would like to access."
    >
      <OrganizationSelector organizations={serializedOrganizations} />
    </ContentLayout>
  );
}
