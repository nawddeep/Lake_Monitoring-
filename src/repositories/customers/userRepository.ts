import { prisma } from "@/lib/prisma";

export async function findUserByEmail(email: string) {
  return prisma.user.findUnique({ where: { email } });
}

export async function updateUserProfileByEmail(
  email: string,
  data: {
    firstName: string;
    lastName: string;
    fullName: string;
  },
) {
  return prisma.user.update({
    where: { email },
    data: {
      firstName: data.firstName,
      lastName: data.lastName,
      name: data.fullName,
      emailVerified: true,
      role: null,
    },
  });
}
