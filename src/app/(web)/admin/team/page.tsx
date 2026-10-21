import { MembersPageClient } from "./_components/members-page-client";
import { requireSession } from "@/lib/auth/session";

export default async function MembersPage() {
  const { user } = await requireSession();
  return <MembersPageClient currentUserId={user.id} />;
}
