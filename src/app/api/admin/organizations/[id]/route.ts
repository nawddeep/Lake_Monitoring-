import {
  deleteOrganization,
  findById,
  updateOrganization,
} from "@/repositories/admin/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { updateOrganizationSchema } from "@/app/api/admin/organizations/schema";
import { withAdmin } from "@/app/api/admin/with-admin";
import { detailResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

export const GET = withAdmin(async (_request, context) => {
  const { id } = await context.params;
  const organization = await findById(id);
  if (!organization) return notFoundResponse("Organization not found");
  return detailResponse(serializeOrganization(organization));
});

export const PATCH = withAdmin(
  async (request, context) => {
    const { id } = await context.params;
    const existing = await findById(id);
    if (!existing) return notFoundResponse("Organization not found");

    const payload = updateOrganizationSchema.parse(await request.json());
    const updated = await updateOrganization(id, payload);
    return detailResponse(serializeOrganization(updated));
  },
  { organization: ["update"] },
);

export const DELETE = withAdmin(
  async (_request, context) => {
    const { id } = await context.params;
    const existing = await findById(id);
    if (!existing) return notFoundResponse("Organization not found");

    await deleteOrganization(id);
    return noContentResponse();
  },
  { organization: ["delete"] },
);
