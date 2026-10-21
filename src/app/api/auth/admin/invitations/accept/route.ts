import { AcceptAdminInvitationValidator } from "./validator";
import { APIError } from "better-auth";
import { auth } from "@/lib/auth/auth";
import { prisma } from "@/lib/prisma";
import { markInvitationAccepted } from "@/repositories/auth/invitationRepository";
import { conflictResponse, createdResponse, validationErrorResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const validator = new AcceptAdminInvitationValidator(await request.json());
  const isValid = await validator.validate();
  if (!isValid) return validationErrorResponse(validator.errors);

  const { invitationId, trimmedFirstName, trimmedLastName, fullName, email, password, role } =
    validator.data;

  try {
    await auth.api.signUpEmail({
      body: {
        name: fullName,
        email,
        password,
        firstName: trimmedFirstName,
        lastName: trimmedLastName,
      },
    });
  } catch (error) {
    if (error instanceof APIError) {
      return conflictResponse(error.body?.message ?? "Unable to complete the invitation.");
    }
    throw error;
  }

  await prisma.user.update({
    where: { email },
    data: {
      emailVerified: true,
      name: fullName,
      firstName: trimmedFirstName,
      lastName: trimmedLastName,
      role,
    },
  });

  await markInvitationAccepted(invitationId);

  return createdResponse({ message: "Invitation accepted." });
});
