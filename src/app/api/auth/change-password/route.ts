import { changePasswordSchema } from "./schema";
import { APIError } from "better-auth";
import { auth } from "@/lib/auth/auth";
import { noContentResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const body = changePasswordSchema.parse(await request.json());

  try {
    await auth.api.changePassword({
      body: { currentPassword: body.currentPassword, newPassword: body.newPassword },
      headers: request.headers,
    });
  } catch (error) {
    if (error instanceof APIError) {
      return unauthorizedResponse(error.body?.message ?? "Failed to change password.");
    }
    throw error;
  }

  return noContentResponse();
});
