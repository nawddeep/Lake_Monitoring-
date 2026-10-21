import {
  cancelPendingInvitation,
  findCustomerInvitationById,
} from "@/repositories/admin/invitationRepository";
import { withAdmin } from "@/app/api/admin/with-admin";
import { conflictResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

export const DELETE = withAdmin(
  async (_request, { params }) => {
    const { id: organizationId, invitationId } = await params;

    const invitation = await findCustomerInvitationById(invitationId, organizationId);
    if (!invitation) return notFoundResponse("Invitation not found.");

    const canceled = await cancelPendingInvitation(invitationId);
    if (!canceled) {
      return conflictResponse("Only pending invitations can be canceled.");
    }

    return noContentResponse();
  },
  { invitation: ["cancel"] },
);
