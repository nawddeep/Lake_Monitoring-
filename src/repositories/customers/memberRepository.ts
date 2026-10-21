import type { Prisma } from "@generated/prisma/client";
import { randomUUID } from "crypto";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";

type MemberSortField = "createdAt" | "firstName" | "lastName" | "email" | "role" | "name";

type MemberFilters = {
  search?: string;
  roles?: string[];
};

export type ListOrganizationMembersParams = {
  options: BaseListOptions<MemberSortField>;
  filters?: MemberFilters;
};

export async function createMember({
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

export async function findMemberByOrganizationAndUser(organizationId: string, userId: string) {
  return prisma.member.findFirst({
    where: {
      organizationId,
      userId,
    },
  });
}

export async function listOrganizationMembers(
  organizationId: string,
  { options, filters }: ListOrganizationMembersParams,
) {
  const { page, perPage, sort, order } = options;
  const where = combineFilters<Prisma.MemberWhereInput>(
    { organizationId },
    rolesFilter(filters?.roles),
    searchFilter(filters?.search),
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

export async function countOrganizationOwners(organizationId: string) {
  return prisma.member.count({ where: { organizationId, role: "owner" } });
}

export async function findOrganizationMemberByEmail(organizationId: string, email: string) {
  return prisma.member.findFirst({
    where: { organizationId, user: { is: { email: email.toLowerCase() } } },
  });
}

export async function updateMemberRole(memberId: string, role: string) {
  return prisma.member.update({
    where: { id: memberId },
    data: { role },
    include: { user: true },
  });
}

export async function deleteMember(memberId: string) {
  return prisma.member.delete({ where: { id: memberId } });
}

function rolesFilter(roles?: string[]): Prisma.MemberWhereInput | undefined {
  if (!roles?.length) return undefined;

  const values = Array.from(
    new Set(roles.map((role) => role.trim().toLowerCase()).filter(Boolean)),
  );
  if (values.length === 0) return undefined;
  return values.length === 1 ? { role: values[0] } : { role: { in: values } };
}

function searchFilter(search?: string): Prisma.MemberWhereInput | undefined {
  const term = search?.trim();
  if (!term) return undefined;

  return {
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
