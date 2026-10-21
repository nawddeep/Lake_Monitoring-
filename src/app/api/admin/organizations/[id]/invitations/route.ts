import { createCustomerPortalInvitationSchema, listCustomerInvitationsSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { sendCustomerPortalInvitation } from "@/services/admin/invitations/customerPortalInvitationService";
import { findPendingInvitation, listInvitations } from "@/repositories/admin/invitationRepository";
import { findById } from "@/repositories/admin/organizationRepository";
import { serializeInvitation } from "@/serializers/invitationSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import {
  conflictResponse,
  createdResponse,
  notFoundResponse,
  paginatedResponse,
} from "@/app/api/response";
import { Portal } from "@/config/portals";

export const GET = withAdmin(async (request, { params }) => {
  const { id: organizationId } = await params;
  const parsed = validateQuery(request, listCustomerInvitationsSchema);
  const { page, perPage, order, sort, status } = parsed;

  const { data, total } = await listInvitations({
    options: { page, perPage, order, sort },
    filters: {
      status,
      portals: [Portal.customer],
      organizationIds: [organizationId],
    },
  });

  return paginatedResponse(data.map(serializeInvitation), {
    page,
    perPage,
    total,
  });
});

export const POST = withAdmin(
  async (request, { params }, { user }) => {
    const { id: organizationId } = await params;
    const { email, role } = createCustomerPortalInvitationSchema.parse(await request.json());

    const organization = await findById(organizationId);
    if (!organization) return notFoundResponse("Organization not found.");

    const existingInvitation = await findPendingInvitation(email, organizationId);
    if (existingInvitation) {
      return conflictResponse("This person already has a pending invitation.");
    }

    const invitation = await sendCustomerPortalInvitation({
      email,
      role,
      organizationId,
      organizationName: organization.name,
      inviterId: user.id,
      inviterName: user.name,
    });

    return createdResponse(serializeInvitation(invitation));
  },
  { invitation: ["create"] },
);
