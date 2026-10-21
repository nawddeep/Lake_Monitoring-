import type { Prisma } from "@generated/prisma/client";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";
import { Portal } from "@/config/portals";

type InvitationSortField = "createdAt" | "expiresAt";

export type ListOrganizationInvitationsParams = {
  options: BaseListOptions<InvitationSortField>;
  filters?: { status?: string[] };
};

export async function findCustomerInvitationById(id: string) {
  return prisma.invitation.findFirst({
    where: {
      id,
      portal: Portal.customer,
    },
    include: {
      organization: true,
    },
  });
}

export async function listOrganizationInvitations(
  organizationId: string,
  { options, filters }: ListOrganizationInvitationsParams,
) {
  const { page, perPage, sort, order } = options;
  const where = combineFilters<Prisma.InvitationWhereInput>(
    { organizationId, portal: Portal.customer },
    statusFilter(filters?.status),
  );

  const [data, total] = await prisma.$transaction([
    prisma.invitation.findMany({
      where,
      orderBy: { [sort ?? "createdAt"]: order ?? "desc" },
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.invitation.count({ where }),
  ]);

  return { data, total };
}

export async function findPendingInvitation(email: string, organizationId: string) {
  return prisma.invitation.findFirst({
    where: { email: email.toLowerCase(), organizationId, status: "pending" },
  });
}

export async function findOrganizationInvitation(organizationId: string, invitationId: string) {
  return prisma.invitation.findFirst({
    where: { id: invitationId, organizationId, portal: Portal.customer },
  });
}

export async function cancelPendingInvitation(invitationId: string) {
  const { count } = await prisma.invitation.updateMany({
    where: { id: invitationId, status: "pending" },
    data: { status: "canceled" },
  });
  return count > 0;
}

export async function createCustomerPortalInvitation(params: {
  email: string;
  role: string;
  organizationId: string;
  inviterId: string;
  expiresAt: Date;
}) {
  return prisma.invitation.create({
    data: {
      id: crypto.randomUUID(),
      email: params.email.toLowerCase(),
      role: params.role,
      portal: Portal.customer,
      organizationId: params.organizationId,
      status: "pending",
      inviterId: params.inviterId,
      expiresAt: params.expiresAt,
    },
  });
}

function statusFilter(statuses?: string[]): Prisma.InvitationWhereInput | undefined {
  if (!statuses?.length) return undefined;
  const values = Array.from(new Set(statuses.filter(Boolean)));
  if (values.length === 0) return undefined;
  return values.length === 1 ? { status: values[0] } : { status: { in: values } };
}

export async function updateInvitationEmailStatus(
  id: string,
  emailStatus: "not_sent" | "sent" | "failed",
) {
  return prisma.invitation.update({ where: { id }, data: { emailStatus } });
}
