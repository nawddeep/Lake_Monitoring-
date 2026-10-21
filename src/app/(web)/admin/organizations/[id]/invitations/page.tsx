import { OrganizationInvitationsTable } from "@/app/(web)/admin/organizations/[id]/invitations/_components/organization-invitations-table";

export default async function OrganizationInvitationsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return <OrganizationInvitationsTable organizationId={id} />;
}
