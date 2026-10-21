import { requireSession } from "@/lib/auth/session";
import { OrganizationMembersTable } from "@/app/(web)/admin/organizations/[id]/members/_components/organization-members-table";

export default async function OrganizationMembersPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const { user } = await requireSession();

  return <OrganizationMembersTable organizationId={id} currentUserId={user.id} />;
}
