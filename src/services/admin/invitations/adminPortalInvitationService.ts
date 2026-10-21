import { sendAdminPortalInvitationEmail } from "@/lib/email";
import { attemptInvitationEmail } from "@/lib/email/invitation-delivery";
import { updateInvitationEmailStatus } from "@/repositories/admin/invitationRepository";
import { createAdminPortalInvitation } from "@/repositories/admin/invitationRepository";

const INVITATION_EXPIRES_IN_DAYS = 2;

type SendAdminPortalInvitationParams = {
  email: string;
  role: string;
  inviterId: string;
  inviterName: string;
};

export async function sendAdminPortalInvitation({
  email,
  role,
  inviterId,
  inviterName,
}: SendAdminPortalInvitationParams) {
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + INVITATION_EXPIRES_IN_DAYS);

  const invitation = await createAdminPortalInvitation({
    email,
    role,
    inviterId,
    expiresAt,
  });

  const emailStatus = await attemptInvitationEmail(() =>
    sendAdminPortalInvitationEmail({
      email,
      invitedBy: inviterName,
      inviteLink: `${process.env.APP_URL}/accept-invitation/admin-portal/${invitation.id}`,
    }),
  );

  return updateInvitationEmailStatus(invitation.id, emailStatus);
}
