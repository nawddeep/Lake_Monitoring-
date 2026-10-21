import {
  type OrganizationFixtureKey,
  type PlatformRole,
  type UserFixture,
  demoPassword,
  organizationFixtures,
  userFixtures,
} from "./fixtures";
import type { User } from "@generated/prisma/client";
import { auth } from "@/lib/auth/auth";
import {
  createOrganizationMember,
  findOrganizationMemberByUserId,
  updateMemberRole,
} from "@/repositories/admin/memberRepository";
import {
  createOrganization,
  findBySlug,
  updateOrganization,
} from "@/repositories/admin/organizationRepository";
import {
  findUserByEmail,
  grantTeamMemberAccess,
  revokeTeamMemberAccess,
} from "@/repositories/admin/teamRepository";
import { banUser, unbanUser } from "@/repositories/admin/userRepository";
import { updateUser } from "@/repositories/auth/userRepository";

type OrganizationIds = Map<OrganizationFixtureKey, string>;

export type DemoSeedResult = {
  organizationsCreated: number;
  organizationsUpdated: number;
  usersCreated: number;
  usersUpdated: number;
  membershipsCreated: number;
  membershipsUpdated: number;
};

const result: DemoSeedResult = {
  organizationsCreated: 0,
  organizationsUpdated: 0,
  usersCreated: 0,
  usersUpdated: 0,
  membershipsCreated: 0,
  membershipsUpdated: 0,
};

async function seedOrganizations(): Promise<OrganizationIds> {
  const organizationIds: OrganizationIds = new Map();

  for (const fixture of organizationFixtures) {
    const existingOrganization = await findBySlug(fixture.slug);
    const organization = existingOrganization
      ? await updateOrganization(existingOrganization.id, {
          name: fixture.name,
          slug: fixture.slug,
        })
      : await createOrganization({ name: fixture.name, slug: fixture.slug });

    organizationIds.set(fixture.key, organization.id);
    if (existingOrganization) {
      result.organizationsUpdated++;
    } else {
      result.organizationsCreated++;
    }
  }

  return organizationIds;
}

async function findOrCreateUser(fixture: UserFixture) {
  const existingUser = await findUserByEmail(fixture.email);

  if (existingUser) {
    result.usersUpdated++;
    return updateUser(existingUser.id, {
      firstName: fixture.firstName,
      lastName: fixture.lastName,
    });
  }

  const name = `${fixture.firstName} ${fixture.lastName}`;
  const createdUser = await auth.api.createUser({
    body: {
      name,
      email: fixture.email,
      password: demoPassword,
      role: fixture.platformRole ?? "user",
      data: {
        firstName: fixture.firstName,
        lastName: fixture.lastName,
        emailVerified: true,
      },
    },
  });

  result.usersCreated++;
  return createdUser.user as User;
}

async function setPlatformRole(user: User, platformRole: PlatformRole) {
  if (platformRole !== null) {
    if (user.role !== platformRole) {
      await grantTeamMemberAccess(user.id, platformRole);
    }
    return;
  }

  if (user.role !== null) {
    const revokeResult = await revokeTeamMemberAccess(user.id);
    if (revokeResult !== "revoked") {
      throw new Error(`Could not remove admin portal access from ${user.email}.`);
    }
  }
}

async function setBannedStatus(user: User, banned: boolean) {
  if (banned && !user.banned) {
    await banUser(user.id, { banReason: "Demo account for testing banned-user behavior." });
  } else if (!banned && user.banned) {
    await unbanUser(user.id);
  }
}

async function seedMemberships(user: User, fixture: UserFixture, organizationIds: OrganizationIds) {
  for (const membershipFixture of fixture.memberships) {
    const organizationId = organizationIds.get(membershipFixture.organization);
    if (!organizationId) {
      throw new Error(`Unknown organization fixture: ${membershipFixture.organization}`);
    }

    const membership = await findOrganizationMemberByUserId(organizationId, user.id);
    if (!membership) {
      await createOrganizationMember({
        userId: user.id,
        organizationId,
        role: membershipFixture.role,
      });
      result.membershipsCreated++;
    } else if (membership.role !== membershipFixture.role) {
      await updateMemberRole(membership.id, membershipFixture.role);
      result.membershipsUpdated++;
    }
  }
}

export async function seedDemoData(): Promise<DemoSeedResult> {
  const organizationIds = await seedOrganizations();

  for (const fixture of userFixtures) {
    const user = await findOrCreateUser(fixture);
    await setPlatformRole(user, fixture.platformRole);
    await setBannedStatus(user, fixture.banned ?? false);
    await seedMemberships(user, fixture, organizationIds);
  }

  return result;
}
