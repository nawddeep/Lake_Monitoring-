import { UsersPageClient } from "./_components/users-page-client";
import { requireSession } from "@/lib/auth/session";

export default async function UsersPage() {
  const { user } = await requireSession();

  return <UsersPageClient currentUserId={user.id} />;
}
