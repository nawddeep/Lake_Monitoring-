import type { Prisma } from "@generated/prisma/client";
import { randomUUID } from "crypto";
import { prisma } from "@/lib/prisma";
import type { BaseListOptions, SortOrder } from "@/repositories/types";

type CreateOrganizationInput = {
  name: string;
  slug: string;
};

export async function createOrganization({ name, slug }: CreateOrganizationInput) {
  return prisma.organization.create({
    data: {
      id: randomUUID(),
      name,
      slug,
    },
  });
}

export async function findById(id: string) {
  return prisma.organization.findUnique({
    where: { id },
  });
}

export async function findBySlug(slug: string) {
  return prisma.organization.findUnique({ where: { slug } });
}

type OrganizationSortField = "name" | "slug" | "createdAt";

type OrganizationFilters = {
  search?: string;
};

export type ListOrganizationsParams = {
  options: BaseListOptions<OrganizationSortField>;
  filters?: OrganizationFilters;
};

export async function listOrganizations({ options, filters }: ListOrganizationsParams) {
  const { page, perPage, sort, order } = options;
  const where = searchFilter(filters?.search);

  const [data, total] = await prisma.$transaction([
    prisma.organization.findMany({
      where,
      orderBy: buildOrderBy(sort, order),
      skip: (page - 1) * perPage,
      take: perPage,
    }),
    prisma.organization.count({ where }),
  ]);

  return { data, total };
}

export async function listUserOrganizations(userId: string) {
  return prisma.organization.findMany({
    where: {
      members: {
        some: {
          userId,
        },
      },
    },
    orderBy: {
      name: "asc",
    },
  });
}

export async function updateOrganization(id: string, data: { name: string; slug: string }) {
  return prisma.organization.update({
    where: { id },
    data,
  });
}

export async function deleteOrganization(id: string) {
  return prisma.organization.delete({ where: { id } });
}

function buildOrderBy(sort: OrganizationSortField | undefined, order: SortOrder | undefined) {
  return { [sort ?? "name"]: order ?? "asc" } as const;
}

function searchFilter(search?: string): Prisma.OrganizationWhereInput | undefined {
  const term = search?.trim();
  if (!term) return undefined;

  return {
    OR: [
      { name: { contains: term, mode: "insensitive" } },
      { slug: { contains: term, mode: "insensitive" } },
    ],
  };
}
