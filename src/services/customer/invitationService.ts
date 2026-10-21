import { APIError } from "better-auth";
import { auth } from "@/lib/auth/auth";
import { sendOrganizationInvitationEmail } from "@/lib/email";
import { attemptInvitationEmail } from "@/lib/email/invitation-delivery";
import { prisma } from "@/lib/prisma";
import { markInvitationAccepted } from "@/repositories/auth/invitationRepository";
import { updateInvitationEmailStatus } from "@/repositories/customers/invitationRepository";
import { createCustomerPortalInvitation } from "@/repositories/customers/invitationRepository";
import { createMember } from "@/repositories/customers/memberRepository";
import { updateUserProfileByEmail } from "@/repositories/customers/userRepository";

const invitationExpiresInDays = 2;

export type AcceptCustomerInvitationParams = {
  invitationId: string;
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: string;
  organizationId: string;
};

export class AcceptCustomerInvitationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AcceptCustomerInvitationError";
  }
}

export async function acceptCustomerInvitation({
  invitationId,
  email,
  password,
  firstName,
  lastName,
  role,
  organizationId,
}: AcceptCustomerInvitationParams) {
  const fullName = `${firstName} ${lastName}`.trim();

  try {
    await auth.api.signUpEmail({
      body: {
        name: fullName,
        email,
        password,
        firstName,
        lastName,
      },
    });
  } catch (error) {
    if (error instanceof APIError) {
      throw new AcceptCustomerInvitationError(
        error.body?.message ?? "Unable to complete the invitation.",
      );
    }
    throw error;
  }

  await updateUserProfileByEmail(email, {
    firstName,
    lastName,
    fullName,
  });

  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) {
    throw new AcceptCustomerInvitationError("User could not be created for this invitation.");
  }

  await createMember({ userId: user.id, organizationId, role });
  await markInvitationAccepted(invitationId);

  return { message: "Invitation accepted." };
}

type SendOrganizationInvitationParams = {
  email: string;
  role: string;
  organizationId: string;
  organizationName: string;
  inviterId: string;
  inviterName: string;
};

export async function sendOrganizationInvitation({
  email,
  role,
  organizationId,
  organizationName,
  inviterId,
  inviterName,
}: SendOrganizationInvitationParams) {
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + invitationExpiresInDays);

  const invitation = await createCustomerPortalInvitation({
    email,
    role,
    organizationId,
    inviterId,
    expiresAt,
  });

  const emailStatus = await attemptInvitationEmail(() =>
    sendOrganizationInvitationEmail({
      email,
      organizationName,
      invitedBy: inviterName,
      inviteLink: `${process.env.APP_URL}/accept-invitation/customer-portal/${invitation.id}`,
    }),
  );

  return updateInvitationEmailStatus(invitation.id, emailStatus);
}
