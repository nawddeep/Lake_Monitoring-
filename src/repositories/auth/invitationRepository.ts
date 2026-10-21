import { prisma } from "@/lib/prisma";
import { Portal } from "@/config/portals";

export async function findAdminInvitationById(id: string) {
  return prisma.invitation.findFirst({
    where: {
      id,
      portal: Portal.admin,
    },
  });
}

export async function markInvitationAccepted(id: string) {
  return prisma.invitation.update({
    where: { id },
    data: { status: "accepted" },
  });
}

export async function acceptAdminInvitationForExistingUser({
  invitationId,
  userId,
  role,
}: {
  invitationId: string;
  userId: string;
  role: string;
}) {
  return prisma.$transaction(async (transaction) => {
    const { count } = await transaction.user.updateMany({
      where: { id: userId, role: null },
      data: { role },
    });
    if (count === 0) return false;

    await transaction.invitation.update({
      where: { id: invitationId },
      data: { status: "accepted" },
    });

    return true;
  });
}
