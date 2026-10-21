import { createInvitationSchema, listInvitationsSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { sendOrganizationInvitation } from "@/services/customer/invitationService";
import {
  findPendingInvitation,
  listOrganizationInvitations,
} from "@/repositories/customers/invitationRepository";
import { findOrganizationMemberByEmail } from "@/repositories/customers/memberRepository";
import { findOrganizationById } from "@/repositories/customers/organizationRepository";
import { serializeInvitation } from "@/serializers/invitationSerializer";
import { withCustomer } from "@/app/api/customer/with-customer";
import { conflictResponse, createdResponse, paginatedResponse } from "@/app/api/response";

export const GET = withCustomer(async (request, _context, { organizationId }) => {
  const { page, perPage, order, sort, status } = validateQuery(request, listInvitationsSchema);
  const { data, total } = await listOrganizationInvitations(organizationId, {
    options: { page, perPage, order, sort },
    filters: { status: status?.length ? status : undefined },
  });

  return paginatedResponse(data.map(serializeInvitation), { page, perPage, total });
});

export const POST = withCustomer(
  async (request, _context, { organizationId, user }) => {
    const { email, role } = createInvitationSchema.parse(await request.json());

    const existingMember = await findOrganizationMemberByEmail(organizationId, email);
    if (existingMember) {
      return conflictResponse("This person is already a member of the organization.");
    }

    const existingInvitation = await findPendingInvitation(email, organizationId);
    if (existingInvitation) {
      return conflictResponse("This person already has a pending invitation.");
    }

    const organization = await findOrganizationById(organizationId);
    if (!organization) {
      throw new Error("The active organization could not be found.");
    }

    const invitation = await sendOrganizationInvitation({
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
