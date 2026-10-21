import type { Invitation as PrismaInvitation } from "@generated/prisma/client";
import { getInvitationPath } from "@/lib/invitation-link";
import type { Invitation } from "@/types/invitation";

export function serializeInvitation(invitation: PrismaInvitation): Invitation {
  return {
    id: invitation.id,
    email: invitation.email,
    role: invitation.role,
    portal: invitation.portal,
    status: invitation.status,
    emailStatus: invitation.emailStatus as Invitation["emailStatus"],
    invitationUrl: getInvitationPath(invitation),
    createdAt: invitation.createdAt.toISOString(),
    expiresAt: invitation.expiresAt.toISOString(),
  };
}
