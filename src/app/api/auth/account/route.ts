import { updateAccountSchema } from "./schema";
import { auth } from "@/lib/auth/auth";
import { updateUser } from "@/repositories/auth/userRepository";
import { noContentResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const PATCH = withErrorHandler(async (request) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session || ("error" in session && session.error)) {
    return unauthorizedResponse();
  }

  const validated = updateAccountSchema.parse(await request.json());
  await updateUser(session.user.id, validated);
  return noContentResponse();
});
