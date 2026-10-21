import { redirect } from "next/navigation";
import { CustomerDashboard } from "./_components/customer-dashboard";
import { requireSession } from "@/lib/auth/session";
import { findOrganizationById } from "@/repositories/customers/organizationRepository";
import { ContentLayout } from "@/components/platform/content-layout";

export default async function CustomerHomePage() {
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
      title={organization.name}
      description="This is the place to manage your members, invitations, and organization details."
    >
      <CustomerDashboard />
    </ContentLayout>
  );
}
