import { prisma } from "@/lib/prisma";

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

export async function findOrganizationById(organizationId: string) {
  return prisma.organization.findUnique({
    where: { id: organizationId },
  });
}
