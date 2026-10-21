import type { Prisma } from "@generated/prisma/client";
import { randomUUID } from "crypto";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";

type MemberSortField = "createdAt" | "firstName" | "lastName" | "email" | "role" | "name";

type MemberFilters = {
  status?: string[];
  search?: string;
  roles?: string[];
};

export type ListOrganizationMembersParams = {
  options: BaseListOptions<MemberSortField>;
  filters?: MemberFilters;
};

export async function listOrganizationMembers(
  organizationId: string,
  { options, filters }: ListOrganizationMembersParams,
) {
  const { page, perPage, sort, order } = options;
  const { status, search, roles } = filters ?? {};
  const where = combineFilters<Prisma.MemberWhereInput>(
    { organizationId },
    statusFilter(status),
    rolesFilter(roles),
    searchFilter(search),
  );

  const [data, total] = await prisma.$transaction([
    prisma.member.findMany({
      where,
      include: { user: true },
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.member.count({ where }),
  ]);

  return { data, total };
}

export async function findOrganizationMember(organizationId: string, memberId: string) {
  return prisma.member.findFirst({
    where: { id: memberId, organizationId },
    include: { user: true },
  });
}

export async function findOrganizationMemberByUserId(organizationId: string, userId: string) {
  return prisma.member.findFirst({ where: { organizationId, userId } });
}

export async function createOrganizationMember({
  userId,
  organizationId,
  role,
}: {
  userId: string;
  organizationId: string;
  role: string;
}) {
  return prisma.member.create({
    data: {
      id: randomUUID(),
      userId,
      organizationId,
      role,
    },
  });
}

export async function countOrganizationOwners(organizationId: string) {
  return prisma.member.count({ where: { organizationId, role: "owner" } });
}

export async function updateMemberRole(id: string, role: string) {
  return prisma.member.update({
    where: { id },
    data: { role },
    include: { user: true },
  });
}

export async function deleteMember(id: string) {
  return prisma.member.delete({ where: { id } });
}

function statusFilter(status?: string[]): Prisma.MemberWhereInput | undefined {
  if (!status?.length) return undefined;

  const normalized = Array.from(
    new Set(status.map((value) => value.trim().toLowerCase()).filter(Boolean)),
  );
  if (normalized.length === 0) return undefined;

  const hasBanned = normalized.includes("banned");
  const hasActive = normalized.includes("active");

  if (hasBanned && hasActive) return undefined;

  if (hasBanned) {
    return { user: { is: { banned: true } } };
  }

  if (hasActive) {
    return { user: { is: { OR: [{ banned: false }, { banned: null }] } } };
  }

  return undefined;
}

function rolesFilter(roles?: string[]): Prisma.MemberWhereInput | undefined {
  if (!roles?.length) return undefined;

  const normalized = Array.from(
    new Set(roles.map((value) => value.trim().toLowerCase()).filter(Boolean)),
  );

  if (normalized.length === 0) return undefined;

  if (normalized.length === 1) {
    return { role: normalized[0] };
  }

  return { role: { in: normalized } };
}

function searchFilter(search?: string): Prisma.MemberWhereInput | undefined {
  const term = search?.trim();
  if (!term) return undefined;

  return {
    OR: [
      { role: { contains: term, mode: "insensitive" } },
      {
        user: {
          is: {
            OR: [
              { firstName: { contains: term, mode: "insensitive" } },
              { lastName: { contains: term, mode: "insensitive" } },
              { name: { contains: term, mode: "insensitive" } },
              { email: { contains: term, mode: "insensitive" } },
            ],
          },
        },
      },
    ],
  };
}

function buildOrderBy(
  sort: MemberSortField | undefined,
  order: SortOrder | undefined,
): Prisma.MemberOrderByWithRelationInput {
  const direction = order ?? "desc";

  switch (sort) {
    case "firstName":
      return { user: { firstName: direction } };
    case "lastName":
      return { user: { lastName: direction } };
    case "email":
      return { user: { email: direction } };
    case "role":
      return { role: direction };
    case "name":
      return { user: { name: direction } };
    default:
      return { createdAt: direction };
  }
}
