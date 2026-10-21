import { setActiveOrganizationSchema } from "./schema";
import { auth } from "@/lib/auth/auth";
import { findMemberByOrganizationAndUser } from "@/repositories/customers/memberRepository";
import { forbiddenResponse, noContentResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const PATCH = withErrorHandler(async (request) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session || ("error" in session && session.error)) {
    return unauthorizedResponse();
  }

  const { organizationId } = setActiveOrganizationSchema.parse(await request.json());
  const membership = await findMemberByOrganizationAndUser(organizationId, session.user.id);
  if (!membership) {
    return forbiddenResponse("You do not have access to this organization.");
  }

  await auth.api.setActiveOrganization({
    body: { organizationId },
    headers: request.headers,
  });

  return noContentResponse();
});
