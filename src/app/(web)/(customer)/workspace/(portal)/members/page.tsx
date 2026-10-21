import { requireSession } from "@/lib/auth/session";
import { MembersTable } from "@/app/(web)/(customer)/workspace/(portal)/members/_components/members-table";

export default async function MembersPage() {
  const { user } = await requireSession();
  return <MembersTable currentUserId={user.id} />;
}
