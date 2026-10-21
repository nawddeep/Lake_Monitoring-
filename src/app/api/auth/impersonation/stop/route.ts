import { auth } from "@/lib/auth/auth";
import { forbiddenResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session || ("error" in session && session.error)) {
    return unauthorizedResponse();
  }

  if (!session.session.impersonatedBy) {
    return forbiddenResponse("You are not impersonating a user.");
  }

  return auth.api.stopImpersonating({
    headers: request.headers,
    asResponse: true,
  });
});
