import { EMAIL_FROM, getResend } from "@/lib/email/client";
import { appConfig } from "@/config/app";

export type AdminPortalInvitationEmailPayload = {
  email: string;
  invitedBy?: string;
  inviteLink: string;
};

export async function sendAdminPortalInvitationEmail({
  email,
  invitedBy,
  inviteLink,
}: AdminPortalInvitationEmailPayload) {
  if (!email || !inviteLink) {
    throw new Error("Admin portal invitation email requires email and inviteLink.");
  }

  const inviterText = invitedBy ? `${invitedBy} has invited you` : "You've been invited";

  const { error } = await getResend().emails.send({
    from: EMAIL_FROM,
    to: email,
    subject: `You've been invited to join the ${appConfig.name} Admin Portal`,
    html: `
      <p>${inviterText} to join the ${appConfig.name} Admin Portal.</p>
      <p>Click the link below to accept your invitation.</p>
      <p><a href="${inviteLink}">Accept invitation</a></p>
      <p>If you weren't expecting this email, you can safely ignore it.</p>
    `,
  });

  if (error) {
    console.error("[Resend] Failed to send admin portal invitation email:", error);
    throw new Error(error.message);
  }
}
