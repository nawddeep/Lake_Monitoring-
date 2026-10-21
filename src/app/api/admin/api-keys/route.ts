import { listApiKeysSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { listApiKeys } from "@/repositories/admin/apiKeyRepository";
import { serializeApiKey } from "@/serializers/apiKeySerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { paginatedResponse } from "@/app/api/response";

export const GET = withAdmin(
  async (request) => {
    const validated = validateQuery(request, listApiKeysSchema);
    const { page, perPage, order, sort, enabled, search } = validated;

    const { data, total } = await listApiKeys({
      options: { page, perPage, order, sort },
      filters: { enabled, search },
    });

    return paginatedResponse(data.map(serializeApiKey), {
      page: validated.page,
      perPage: validated.perPage,
      total,
    });
  },
  { apiKey: ["read:any"] },
);
