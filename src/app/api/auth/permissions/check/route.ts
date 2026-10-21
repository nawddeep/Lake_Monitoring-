import { checkPermissionsSchema } from "./schema";
import { auth } from "@/lib/auth/auth";
import { detailResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const body = checkPermissionsSchema.parse(await request.json());

  const result = await auth.api.userHasPermission({
    body: { permissions: body.permissions },
    headers: request.headers,
  });

  return detailResponse({ allowed: result.success });
});
