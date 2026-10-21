import { findTeamMember, revokeTeamMemberAccess } from "@/repositories/admin/teamRepository";
import { serializeUser } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import {
  conflictResponse,
  detailResponse,
  forbiddenResponse,
  noContentResponse,
  notFoundResponse,
} from "@/app/api/response";

export const GET = withAdmin(async (_request, { params }) => {
  const { id } = await params;
  const user = await findTeamMember(id);
  if (!user) return notFoundResponse();
  return detailResponse(serializeUser(user));
});

export const DELETE = withAdmin(
  async (_request, { params }, { user }) => {
    const { id } = await params;
    if (id === user.id) {
      return forbiddenResponse("You cannot delete your own account.");
    }

    const result = await revokeTeamMemberAccess(id);
    if (result === "not_found") return notFoundResponse();
    if (result === "last_admin") {
      return conflictResponse("You cannot revoke access from the last administrator.");
    }

    return noContentResponse();
  },
  { user: ["set-role"] },
);
