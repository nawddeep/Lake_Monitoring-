import { createAdminPortalInvitationSchema, listAdminPortalInvitationsSchema } from "./schema";
import { validateQuery } from "@/lib/api";
import { sendAdminPortalInvitation } from "@/services/admin/invitations/adminPortalInvitationService";
import { listInvitations } from "@/repositories/admin/invitationRepository";
import { findUserByEmail } from "@/repositories/admin/teamRepository";
import { serializeInvitation } from "@/serializers/invitationSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { conflictResponse, createdResponse, paginatedResponse } from "@/app/api/response";
import { Portal } from "@/config/portals";

export const GET = withAdmin(async (request) => {
  const parsed = validateQuery(request, listAdminPortalInvitationsSchema);
  const { page, perPage, order, sort, status } = parsed;

  const { data, total } = await listInvitations({
    options: { page, perPage, order, sort },
    filters: { status, portals: [Portal.admin] },
  });

  return paginatedResponse(data.map(serializeInvitation), {
    page,
    perPage,
    total,
  });
});

export const POST = withAdmin(
  async (request, _context, { user }) => {
    const { email, role } = createAdminPortalInvitationSchema.parse(await request.json());

    const existingUser = await findUserByEmail(email);
    if (existingUser?.role) {
      return conflictResponse("This user already has access to the admin portal.");
    }

    const invitation = await sendAdminPortalInvitation({
      email,
      role,
      inviterId: user.id,
      inviterName: user.name,
    });

    return createdResponse(serializeInvitation(invitation));
  },
  { invitation: ["create"] },
);
