import type { Prisma } from "@generated/prisma/client";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";

type TeamSortField = "createdAt" | "role";

type TeamFilters = {
  status?: string[];
};

export type ListTeamMembersOptions = {
  params: BaseListOptions<TeamSortField>;
  filters?: TeamFilters;
};

function whereHasAdminPortalAccess(): Prisma.UserWhereInput {
  return { role: { not: null } };
}

export async function listTeamMembers({ params, filters }: ListTeamMembersOptions) {
  const { page, perPage, sort, order } = params;

  const where = combineFilters<Prisma.UserWhereInput>(
    whereHasAdminPortalAccess(),
    statusFilter(filters?.status),
  );

  const [data, total] = await prisma.$transaction([
    prisma.user.findMany({
      where,
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.user.count({ where }),
  ]);

  return { data, total };
}

export async function findUserByEmail(email: string) {
  return prisma.user.findUnique({ where: { email: email.toLowerCase() } });
}

export async function grantTeamMemberAccess(id: string, role: string) {
  return prisma.user.update({ where: { id }, data: { role } });
}

export async function updateTeamMemberRole(id: string, role: string) {
  const { count } = await prisma.user.updateMany({
    where: { id, ...whereHasAdminPortalAccess() },
    data: { role },
  });
  if (count === 0) return null;

  return prisma.user.findUnique({ where: { id } });
}

export async function findTeamMember(id: string) {
  return prisma.user.findFirst({ where: { id, ...whereHasAdminPortalAccess() } });
}

export async function revokeTeamMemberAccess(id: string) {
  return prisma.$transaction(async (transaction) => {
    const user = await transaction.user.findFirst({
      where: { id, ...whereHasAdminPortalAccess() },
      select: { role: true },
    });

    if (!user) return "not_found" as const;

    if (user.role === "admin") {
      const adminCount = await transaction.user.count({ where: { role: "admin" } });
      if (adminCount <= 1) return "last_admin" as const;
    }

    await transaction.user.update({
      where: { id },
      data: { role: null },
    });

    return "revoked" as const;
  });
}

function statusFilter(statuses?: string[]): Prisma.UserWhereInput | undefined {
  if (!statuses?.length) return undefined;

  const normalized = Array.from(
    new Set(statuses.map((value) => value.trim().toLowerCase()).filter(Boolean)),
  );

  if (normalized.length !== 1) return undefined;

  const [status] = normalized;

  if (status === "banned") {
    return { banned: true };
  }

  if (status === "active") {
    return { OR: [{ banned: false }, { banned: null }] };
  }

  return undefined;
}

function buildOrderBy(sort: TeamSortField | undefined, order: SortOrder | undefined) {
  return { [sort ?? "createdAt"]: order ?? "asc" } as const;
}
