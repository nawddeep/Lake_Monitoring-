import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { type AdminPermissions } from "@/lib/auth/admin-permissions";
import { auth } from "@/lib/auth/auth";

export async function requirePermission(permissions: AdminPermissions): Promise<void> {
  const session = await auth.api.getSession({ headers: await headers() });

  const { success } = await auth.api.userHasPermission({
    body: {
      userId: session?.user.id,
      permissions: permissions as Record<string, string[]>,
    },
  });

  if (!success) redirect("/admin/dashboard");
}
