import type { Organization as PrismaOrganization } from "@generated/prisma/client";
import { Organization } from "@/types/organization";

export function serializeOrganization(organization: PrismaOrganization): Organization {
  return {
    id: organization.id,
    name: organization.name,
    slug: organization.slug,
    createdAt: organization.createdAt.toISOString(),
  };
}
