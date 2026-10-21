import { EMAIL_FROM, getResend } from "@/lib/email/client";
import { appConfig } from "@/config/app";

export type OrganizationInvitationPayload = {
  email: string;
  organizationName: string;
  invitedBy?: string;
  inviteLink: string;
};

export async function sendOrganizationInvitationEmail({
  email,
  organizationName,
  invitedBy,
  inviteLink,
}: OrganizationInvitationPayload) {
  if (!email || !inviteLink) {
    throw new Error("Organization invitation email requires email and inviteLink.");
  }

  const inviterText = invitedBy ? `${invitedBy} has invited you` : "You've been invited";

  const { error } = await getResend().emails.send({
    from: EMAIL_FROM,
    to: email,
    subject: `You've been invited to join ${organizationName} on ${appConfig.name}`,
    html: `
      <p>${inviterText} to join <strong>${organizationName}</strong> on the ${appConfig.name} platform.</p>
      <p>Click the link below to accept your invitation.</p>
      <p><a href="${inviteLink}">Accept invitation</a></p>
      <p>If you weren't expecting this email, you can safely ignore it.</p>
    `,
  });

  if (error) {
    console.error("[Resend] Failed to send organization invitation email:", error);
    throw new Error(error.message);
  }
}
