import type { Prisma } from "@generated/prisma/client";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";
import { combineFilters } from "@/repositories/utils";

type SortField = "name" | "createdAt" | "expiresAt";

type Filters = {
  enabled?: string[];
  search?: string;
  users?: string[];
};

export type ListApiKeysParams = {
  options: BaseListOptions<SortField>;
  filters?: Filters;
};

export async function listApiKeys({ options, filters }: ListApiKeysParams) {
  const { page, perPage, sort, order } = options;
  const { enabled, search, users } = filters ?? {};
  const where = combineFilters<Prisma.ApikeyWhereInput>(
    enabledFilter(enabled),
    searchFilter(search),
    usersFilter(users),
  );

  const [data, total] = await prisma.$transaction([
    prisma.apikey.findMany({
      where,
      include: { user: true },
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.apikey.count({ where }),
  ]);

  return { data, total };
}

export async function findApiKeyById(id: string) {
  return prisma.apikey.findUnique({ where: { id } });
}

export async function disableApiKeyById(id: string) {
  return prisma.apikey.update({
    where: { id },
    data: { enabled: false },
  });
}

export async function updateApiKeyNameForUser(id: string, userId: string, name: string) {
  return prisma.$transaction(async (transaction) => {
    const { count } = await transaction.apikey.updateMany({
      where: { id, referenceId: userId },
      data: { name },
    });
    if (count === 0) return null;

    return transaction.apikey.findUnique({ where: { id } });
  });
}

export async function disableApiKeyForUser(id: string, userId: string) {
  const { count } = await prisma.apikey.updateMany({
    where: { id, referenceId: userId },
    data: { enabled: false },
  });
  return count > 0;
}

function enabledFilter(enabled?: string[]): Prisma.ApikeyWhereInput | undefined {
  const hasTrue = enabled?.includes("true") ?? false;
  const hasFalse = enabled?.includes("false") ?? false;

  if (hasTrue && !hasFalse) return { enabled: true };
  if (hasFalse && !hasTrue) return { enabled: false };
  return undefined;
}

function searchFilter(search?: string): Prisma.ApikeyWhereInput | undefined {
  if (!search) return undefined;
  return {
    OR: [
      { name: { contains: search, mode: "insensitive" as const } },
      { start: { contains: search, mode: "insensitive" as const } },
    ],
  };
}

function usersFilter(users?: string[]): Prisma.ApikeyWhereInput | undefined {
  if (!users?.length) return undefined;
  if (users.length === 1) return { referenceId: users[0] };
  return { referenceId: { in: users } };
}

function buildOrderBy(sort: SortField | undefined, order: SortOrder | undefined) {
  return { [sort ?? "createdAt"]: order ?? "desc" } as const;
}
