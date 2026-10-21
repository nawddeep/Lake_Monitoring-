import {
  cancelPendingInvitation,
  findOrganizationInvitation,
} from "@/repositories/customers/invitationRepository";
import { withCustomer } from "@/app/api/customer/with-customer";
import { conflictResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

export const DELETE = withCustomer(
  async (_request, { params }, { organizationId }) => {
    const { invitationId } = await params;
    const invitation = await findOrganizationInvitation(organizationId, invitationId);
    if (!invitation) return notFoundResponse("Invitation not found.");

    const canceled = await cancelPendingInvitation(invitationId);
    if (!canceled) {
      return conflictResponse("Only pending invitations can be canceled.");
    }

    return noContentResponse();
  },
  { invitation: ["cancel"] },
);
