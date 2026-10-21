import { createOrganizationSchema, listOrganizationsSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { createOrganization, listOrganizations } from "@/repositories/admin/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { createdResponse, paginatedResponse } from "@/app/api/response";

export const GET = withAdmin(async (request) => {
  const validated = validateQuery(request, listOrganizationsSchema);
  const { page, perPage, order, sort, search } = validated;

  const { data, total } = await listOrganizations({
    options: { page, perPage, order, sort },
    filters: search ? { search } : undefined,
  });

  return paginatedResponse(data.map(serializeOrganization), {
    page,
    perPage,
    total,
  });
});

export const POST = withAdmin(
  async (request) => {
    const validated = createOrganizationSchema.parse(await request.json());
    const organization = await createOrganization(validated);
    return createdResponse(serializeOrganization(organization));
  },
  { organization: ["create"] },
);
