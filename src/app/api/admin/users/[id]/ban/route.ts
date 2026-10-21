import { banUserSchema } from "./schema";
import { banUser } from "@/repositories/admin/userRepository";
import { serializeUser } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { detailResponse, forbiddenResponse, notFoundResponse } from "@/app/api/response";

export const POST = withAdmin(
  async (request, { params }, { user }) => {
    const { id } = await params;
    if (id === user.id) {
      return forbiddenResponse("You cannot ban your own account.");
    }

    const body = banUserSchema.parse(await request.json());
    const updated = await banUser(id, body);
    if (!updated) return notFoundResponse("User not found.");

    return detailResponse(serializeUser(updated));
  },
  { user: ["ban"] },
);
