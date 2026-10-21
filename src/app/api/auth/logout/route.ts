import { auth } from "@/lib/auth/auth";
import { noContentResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  await auth.api.signOut({ headers: request.headers });
  return noContentResponse();
});
