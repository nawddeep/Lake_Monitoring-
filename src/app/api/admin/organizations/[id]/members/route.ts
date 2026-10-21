import { listMembersSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { listOrganizationMembers } from "@/repositories/admin/memberRepository";
import { serializeMember } from "@/serializers/memberSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { paginatedResponse } from "@/app/api/response";

export const GET = withAdmin(async (request, { params }) => {
  const { id: organizationId } = await params;
  const validated = validateQuery(request, listMembersSchema);
  const { page, perPage, order, sort, search, status, role } = validated;
  const roles = role?.filter(Boolean);

  const { data, total } = await listOrganizationMembers(organizationId, {
    options: { page, perPage, order, sort },
    filters: {
      status: status && status.length > 0 ? status : undefined,
      roles: roles && roles.length > 0 ? roles : undefined,
      search,
    },
  });

  return paginatedResponse(data.map(serializeMember), {
    page,
    perPage,
    total,
  });
});
