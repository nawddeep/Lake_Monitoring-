import { listUsersSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { listUsers } from "@/repositories/admin/userRepository";
import { serializeUserWithAccess } from "@/serializers/userSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { paginatedResponse } from "@/app/api/response";

export const GET = withAdmin(async (request) => {
  const { page, perPage, order, sort, search, status, access } = validateQuery(
    request,
    listUsersSchema,
  );
  const { data, total } = await listUsers({
    options: { page, perPage, order, sort },
    filters: { search, status, access },
  });

  return paginatedResponse(data.map(serializeUserWithAccess), { page, perPage, total });
});
