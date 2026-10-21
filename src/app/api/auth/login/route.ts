import { loginSchema } from "./schema";
import { APIError } from "better-auth";
import { auth } from "@/lib/auth/auth";
import { noContentResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const body = loginSchema.parse(await request.json());

  try {
    await auth.api.signInEmail({ body: { email: body.email, password: body.password } });
  } catch (error) {
    if (error instanceof APIError) {
      return unauthorizedResponse(error.body?.message ?? "Invalid email or password.");
    }
    throw error;
  }

  return noContentResponse();
});
