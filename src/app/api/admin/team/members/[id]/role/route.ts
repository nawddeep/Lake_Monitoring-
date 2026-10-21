import { z } from "zod";
import { updateTeamMemberRole } from "@/repositories/admin/teamRepository";
import { serializeUser } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { detailResponse, forbiddenResponse, notFoundResponse } from "@/app/api/response";

const changeRoleSchema = z.object({
  role: z.enum(["admin", "user"]),
});

export const PATCH = withAdmin(
  async (request, { params }, { user: currentUser }) => {
    const { id } = await params;
    if (id === currentUser.id) {
      return forbiddenResponse("You cannot change your own role.");
    }

    const { role } = changeRoleSchema.parse(await request.json());
    const user = await updateTeamMemberRole(id, role);
    if (!user) return notFoundResponse();
    return detailResponse(serializeUser(user));
  },
  { user: ["set-role"] },
);
