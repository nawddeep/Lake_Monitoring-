import { auth } from "@/lib/auth/auth";
import { listUserOrganizations } from "@/repositories/customers/organizationRepository";
import { serializeOrganization } from "@/serializers/organizationSerializer";
import { listResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const GET = withErrorHandler(async (request) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session || ("error" in session && session.error)) {
    return unauthorizedResponse();
  }

  const organizations = await listUserOrganizations(session.user.id);
  return listResponse(organizations.map(serializeOrganization));
});
