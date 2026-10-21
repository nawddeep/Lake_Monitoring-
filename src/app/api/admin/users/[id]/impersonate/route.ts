import { auth } from "@/lib/auth/auth";
import { findUserById } from "@/repositories/admin/userRepository";
import { withAdmin } from "@/app/api/admin/with-admin";
import { forbiddenResponse, notFoundResponse } from "@/app/api/response";

export const POST = withAdmin(
  async (request, { params }, { user }) => {
    const { id } = await params;
    if (id === user.id) {
      return forbiddenResponse("You cannot impersonate your own account.");
    }

    const targetUser = await findUserById(id);
    if (!targetUser) {
      return notFoundResponse("User not found.");
    }

    if (targetUser.role === "admin") {
      return forbiddenResponse("Admin accounts cannot be impersonated.");
    }

    if (targetUser.banned) {
      return forbiddenResponse("Banned users cannot be impersonated.");
    }

    return auth.api.impersonateUser({
      body: { userId: id },
      headers: request.headers,
      asResponse: true,
    });
  },
  { user: ["impersonate"] },
);
