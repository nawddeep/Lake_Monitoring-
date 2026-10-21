import { listTeamMembersSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { listTeamMembers } from "@/repositories/admin/teamRepository";
import { serializeUser } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { paginatedResponse } from "@/app/api/response";

export const GET = withAdmin(async (request) => {
  const validated = validateQuery(request, listTeamMembersSchema);
  const { page, perPage, order, sort, status } = validated;

  const { data, total } = await listTeamMembers({
    params: { page, perPage, order, sort },
    filters: { status },
  });
  return paginatedResponse(data.map(serializeUser), {
    page,
    perPage,
    total,
  });
});
