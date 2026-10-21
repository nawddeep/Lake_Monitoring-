import type { Prisma } from "@generated/prisma/client";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";

type UserSortField = "name" | "email" | "createdAt";

type UserFilters = {
  search?: string;
  status?: string[];
  access?: string[];
};

export type ListUsersParams = {
  options: BaseListOptions<UserSortField>;
  filters?: UserFilters;
};

export async function listUsers({ options, filters }: ListUsersParams) {
  const { page, perPage, sort, order } = options;
  const where = combineFilters<Prisma.UserWhereInput>(
    searchFilter(filters?.search),
    statusFilter(filters?.status),
    accessFilter(filters?.access),
  );

  const [data, total] = await prisma.$transaction([
    prisma.user.findMany({
      where,
      include: {
        _count: {
          select: { members: true },
        },
      },
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.user.count({ where }),
  ]);

  return { data, total };
}

export async function findUserById(id: string) {
  return prisma.user.findUnique({ where: { id } });
}

export async function deleteUser(id: string) {
  const { count } = await prisma.user.deleteMany({ where: { id } });
  return count > 0;
}

export async function banUser(id: string, { banReason }: { banReason?: string }) {
  return prisma.$transaction(async (transaction) => {
    const { count } = await transaction.user.updateMany({
      where: { id },
      data: {
        banned: true,
        banReason: banReason || null,
        banExpires: null,
      },
    });
    if (count === 0) return null;

    await transaction.session.deleteMany({ where: { userId: id } });
    return transaction.user.findUnique({ where: { id } });
  });
}

export async function unbanUser(id: string) {
  const { count } = await prisma.user.updateMany({
    where: { id },
    data: {
      banned: false,
      banReason: null,
      banExpires: null,
    },
  });
  if (count === 0) return null;

  return prisma.user.findUnique({ where: { id } });
}

function searchFilter(search?: string): Prisma.UserWhereInput | undefined {
  const term = search?.trim();
  if (!term) return undefined;

  return {
    OR: [
      { name: { contains: term, mode: "insensitive" } },
      { firstName: { contains: term, mode: "insensitive" } },
      { lastName: { contains: term, mode: "insensitive" } },
      { email: { contains: term, mode: "insensitive" } },
    ],
  };
}

function statusFilter(statuses?: string[]): Prisma.UserWhereInput | undefined {
  if (!statuses?.length) return undefined;

  const normalized = Array.from(
    new Set(statuses.map((value) => value.trim().toLowerCase()).filter(Boolean)),
  );

  if (normalized.length !== 1) return undefined;
  return normalized[0] === "banned"
    ? { banned: true }
    : normalized[0] === "active"
      ? { OR: [{ banned: false }, { banned: null }] }
      : undefined;
}

function accessFilter(accessValues?: string[]): Prisma.UserWhereInput | undefined {
  const accessFilters = Array.from(
    new Set(accessValues?.map((value) => value.trim().toLowerCase()).filter(Boolean)),
  )
    .map(accessCategoryFilter)
    .filter((filter): filter is Prisma.UserWhereInput => Boolean(filter));

  return accessFilters.length ? { OR: accessFilters } : undefined;
}

function accessCategoryFilter(access: string): Prisma.UserWhereInput | undefined {
  if (access === "admin") {
    return { role: { not: null } };
  }

  if (access === "customer") {
    return { members: { some: {} } };
  }

  return undefined;
}

function buildOrderBy(sort: UserSortField | undefined, order: SortOrder | undefined) {
  return { [sort ?? "createdAt"]: order ?? "desc" } as const;
}
