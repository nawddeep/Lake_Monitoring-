import type { Prisma } from "@generated/prisma/client";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";
import { Portal, type PortalValue } from "@/config/portals";

type InvitationSortField = "email" | "role" | "status" | "createdAt" | "expiresAt";

type StatusFilter = string[] | undefined;

type InvitationFilters = {
  portals?: PortalValue[];
  organizationIds?: string[];
  status?: StatusFilter;
};

export type ListInvitationsParams = {
  options: BaseListOptions<InvitationSortField>;
  filters?: InvitationFilters;
};

export async function listInvitations({ options, filters }: ListInvitationsParams) {
  const { page, perPage, sort, order } = options;

  const where = combineFilters<Prisma.InvitationWhereInput>(
    portalsFilter(filters?.portals),
    organizationIdsFilter(filters?.organizationIds),
    statusFilter(filters?.status),
  );

  const [data, total] = await prisma.$transaction([
    prisma.invitation.findMany({
      where,
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.invitation.count({ where }),
  ]);

  return { data, total };
}

export async function findPendingInvitation(email: string, organizationId: string) {
  return prisma.invitation.findFirst({
    where: { email, organizationId, status: "pending" },
  });
}

export async function findCustomerInvitationById(id: string, organizationId: string) {
  return prisma.invitation.findFirst({
    where: {
      id,
      organizationId,
      portal: Portal.customer,
    },
  });
}

export async function findInvitationById(id: string) {
  return prisma.invitation.findUnique({
    where: { id },
  });
}

export async function cancelPendingInvitation(id: string) {
  const { count } = await prisma.invitation.updateMany({
    where: { id, status: "pending" },
    data: { status: "canceled" },
  });
  return count > 0;
}

export async function createAdminPortalInvitation(params: {
  email: string;
  role: string;
  inviterId: string;
  expiresAt: Date;
}) {
  const { email, role, inviterId, expiresAt } = params;

  return prisma.invitation.create({
    data: {
      id: crypto.randomUUID(),
      email,
      role,
      portal: Portal.admin,
      organizationId: null,
      status: "pending",
      inviterId,
      expiresAt,
    },
  });
}

export async function createCustomerPortalInvitation(params: {
  email: string;
  role: string;
  organizationId: string;
  inviterId: string;
  expiresAt: Date;
}) {
  const { email, role, organizationId, inviterId, expiresAt } = params;

  return prisma.invitation.create({
    data: {
      id: crypto.randomUUID(),
      email,
      role,
      portal: Portal.customer,
      organizationId,
      status: "pending",
      inviterId,
      expiresAt,
    },
  });
}

function portalsFilter(portals?: PortalValue[]): Prisma.InvitationWhereInput | undefined {
  if (!portals?.length) return undefined;
  const unique = Array.from(new Set(portals.filter(Boolean)));
  if (unique.length === 0) return undefined;
  if (unique.length === 1) return { portal: unique[0] };
  return { portal: { in: unique } };
}

function organizationIdsFilter(
  organizationIds?: string[],
): Prisma.InvitationWhereInput | undefined {
  if (!organizationIds?.length) return undefined;
  const unique = Array.from(new Set(organizationIds.filter(Boolean)));
  if (unique.length === 0) return undefined;
  if (unique.length === 1) return { organizationId: unique[0] };
  return { organizationId: { in: unique } };
}

function statusFilter(status?: StatusFilter): Prisma.InvitationWhereInput | undefined {
  if (!status?.length) return undefined;
  const values = Array.from(new Set(status.filter(Boolean)));
  if (values.length === 0) return undefined;
  if (values.length === 1) return { status: values[0] };
  return { status: { in: values } };
}

function buildOrderBy(sort: InvitationSortField | undefined, order: SortOrder | undefined) {
  return { [sort ?? "createdAt"]: order ?? "desc" } as const;
}

export async function updateInvitationEmailStatus(
  id: string,
  emailStatus: "not_sent" | "sent" | "failed",
) {
  return prisma.invitation.update({ where: { id }, data: { emailStatus } });
}
