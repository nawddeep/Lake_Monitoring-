import { listMembersSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { listOrganizationMembers } from "@/repositories/customers/memberRepository";
import { serializeMember } from "@/serializers/memberSerializer";
import { withCustomer } from "@/app/api/customer/with-customer";
import { paginatedResponse } from "@/app/api/response";

export const GET = withCustomer(async (request, _context, { organizationId }) => {
  const { page, perPage, order, sort, search, role } = validateQuery(request, listMembersSchema);

  const { data, total } = await listOrganizationMembers(organizationId, {
    options: { page, perPage, order, sort },
    filters: {
      search,
      roles: role?.length ? role : undefined,
    },
  });

  return paginatedResponse(data.map(serializeMember), { page, perPage, total });
});
