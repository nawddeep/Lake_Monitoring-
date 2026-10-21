import { resetPasswordSchema } from "./schema";
import { APIError } from "better-auth";
import { auth } from "@/lib/auth/auth";
import { noContentResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const body = resetPasswordSchema.parse(await request.json());

  try {
    await auth.api.resetPassword({
      body: { newPassword: body.newPassword, token: body.token },
    });
  } catch (error) {
    if (error instanceof APIError) {
      return unauthorizedResponse(error.body?.message ?? "Failed to reset password.");
    }
    throw error;
  }

  return noContentResponse();
});
