import { acceptExistingAdminInvitationSchema } from "./schema";
import { auth } from "@/lib/auth/auth";
import {
  acceptAdminInvitationForExistingUser,
  findAdminInvitationById,
} from "@/repositories/auth/invitationRepository";
import {
  conflictResponse,
  forbiddenResponse,
  noContentResponse,
  notFoundResponse,
  unauthorizedResponse,
} from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const POST = withErrorHandler(async (request) => {
  const { invitationId } = acceptExistingAdminInvitationSchema.parse(await request.json());
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session || ("error" in session && session.error)) {
    return unauthorizedResponse("Sign in to accept this invitation.");
  }

  const invitation = await findAdminInvitationById(invitationId);
  if (!invitation) return notFoundResponse("Invitation not found.");
  if (invitation.status === "accepted") {
    return conflictResponse("This invitation has already been accepted.");
  }
  if (invitation.status === "canceled") {
    return conflictResponse("This invitation has been canceled.");
  }
  if (invitation.expiresAt < new Date()) {
    return conflictResponse("This invitation has expired.");
  }
  if (session.user.email.toLowerCase() !== invitation.email.toLowerCase()) {
    return forbiddenResponse("Sign in with the email address that received this invitation.");
  }
  if (session.user.role) {
    return conflictResponse("You already have access to the admin portal.");
  }

  const accepted = await acceptAdminInvitationForExistingUser({
    invitationId,
    userId: session.user.id,
    role: invitation.role,
  });
  if (!accepted) {
    return conflictResponse("You already have access to the admin portal.");
  }

  return noContentResponse();
});
