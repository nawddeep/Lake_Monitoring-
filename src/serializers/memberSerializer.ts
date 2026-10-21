import type { Member as PrismaMember, User as PrismaUser } from "@generated/prisma/client";
import { serializeUser } from "@/serializers/userSerializer";
import type { Member } from "@/types/member";

type MemberWithUser = PrismaMember & {
  user: PrismaUser;
};

export function serializeMember(member: MemberWithUser): Member {
  return {
    id: member.id,
    role: member.role,
    platformRole: member.user.role,
    user: serializeUser(member.user),
    createdAt: member.createdAt.toISOString(),
  };
}
