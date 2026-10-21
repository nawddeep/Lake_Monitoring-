import type { Prisma, User as PrismaUser } from "@generated/prisma/client";
import type { User, UserAccess, UserWithAccess } from "@/types/user";

export function serializeUser(user: PrismaUser): User {
  return {
    id: user.id,
    name: user.name,
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.email,
    emailVerified: user.emailVerified,
    image: user.image,
    role: user.role,
    banned: user.banned,
    banReason: user.banReason,
    banExpires: user.banExpires?.toISOString() ?? null,
    createdAt: user.createdAt.toISOString(),
    updatedAt: user.updatedAt.toISOString(),
  };
}

type PrismaUserWithMemberCount = Prisma.UserGetPayload<{
  include: { _count: { select: { members: true } } };
}>;

export function serializeUserWithAccess(user: PrismaUserWithMemberCount): UserWithAccess {
  return {
    ...serializeUser(user),
    access: getUserAccess(user.role, user._count.members),
  };
}

function getUserAccess(role: string | null, membershipCount: number): UserAccess {
  const hasAdminAccess = role !== null;
  const hasCustomerAccess = membershipCount > 0;

  if (hasAdminAccess && hasCustomerAccess) return "both";
  if (hasAdminAccess) return "admin_only";
  if (hasCustomerAccess) return "customer_only";
  return "none";
}
