import { unbanUser } from "@/repositories/admin/userRepository";
import { serializeUser } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { detailResponse, notFoundResponse } from "@/app/api/response";

export const POST = withAdmin(
  async (_request, { params }) => {
    const { id } = await params;
    const updated = await unbanUser(id);
    if (!updated) return notFoundResponse("User not found.");

    return detailResponse(serializeUser(updated));
  },
  { user: ["ban"] },
);
