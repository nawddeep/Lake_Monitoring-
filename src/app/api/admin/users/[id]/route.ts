import { deleteUser } from "@/repositories/admin/userRepository";
import { withAdmin } from "@/app/api/admin/with-admin";
import { forbiddenResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

export const DELETE = withAdmin(
  async (_request, { params }, { user }) => {
    const { id } = await params;
    if (id === user.id) {
      return forbiddenResponse("You cannot delete your own account.");
    }

    const deleted = await deleteUser(id);
    if (!deleted) return notFoundResponse();
    return noContentResponse();
  },
  { user: ["delete"] },
);
