import { cancelPendingInvitation } from "@/repositories/admin/invitationRepository";
import { findAdminInvitationById } from "@/repositories/auth/invitationRepository";
import { withAdmin } from "@/app/api/admin/with-admin";
import { conflictResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

export const DELETE = withAdmin(
  async (_request, { params }) => {
    const { id } = await params;

    const invitation = await findAdminInvitationById(id);
    if (!invitation) return notFoundResponse("Invitation not found.");

    const canceled = await cancelPendingInvitation(id);
    if (!canceled) {
      return conflictResponse("Only pending invitations can be canceled.");
    }

    return noContentResponse();
  },
  { invitation: ["cancel"] },
);
