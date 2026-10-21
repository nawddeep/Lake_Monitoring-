import { cancel, intro, isCancel, outro, password, text } from "@clack/prompts";
import { APIError } from "better-auth/api";
import "dotenv/config";
import process from "node:process";
import { auth } from "@/lib/auth/auth";
import { prisma } from "@/lib/prisma";
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
import { findUserByEmail, grantTeamMemberAccess } from "@/repositories/admin/teamRepository";
import { updateUser } from "@/repositories/auth/userRepository";

const minimumPasswordLength = 8;

class SeedCancelledError extends Error {}

async function promptOrCancel<T>(prompt: Promise<T | symbol>): Promise<T> {
  const value = await prompt;

  if (isCancel(value)) {
    cancel("Seed cancelled.");
    throw new SeedCancelledError();
  }

  return value;
}

function createSlug(name: string) {
  return name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

async function promptForAdmin() {
  intro("Create seed admin");

  const firstName = await promptOrCancel(
    text({
      message: "First name",
      validate: (value) => (!value?.trim() ? "First name is required" : undefined),
    }),
  );

  const lastName = await promptOrCancel(
    text({
      message: "Last name",
      validate: (value) => (!value?.trim() ? "Last name is required" : undefined),
    }),
  );

  const email = await promptOrCancel(
    text({
      message: "Email",
      validate: (value) => {
        if (!value?.trim()) return "Email is required";
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Enter a valid email";
        return undefined;
      },
    }),
  );

  const enteredPassword = await promptOrCancel(
    password({
      message: `Password (minimum ${minimumPasswordLength} characters)`,
      validate: (value) => {
        if (!value) return "Password is required";
        if (value.length < minimumPasswordLength) {
          return `Password must be at least ${minimumPasswordLength} characters.`;
        }
        return undefined;
      },
    }),
  );

  await promptOrCancel(
    password({
      message: "Confirm password",
      validate: (value) => (value !== enteredPassword ? "Passwords do not match" : undefined),
    }),
  );

  const organizationName = await promptOrCancel(
    text({
      message: "Organization name",
      validate: (value) => (!value?.trim() ? "Organization name is required" : undefined),
    }),
  );

  const organizationSlug = await promptOrCancel(
    text({
      message: "Organization slug",
      initialValue: createSlug(organizationName),
      validate: (value) => {
        if (!value?.trim()) return "Organization slug is required";
        if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value)) {
          return "Slug must contain lowercase letters, numbers, and hyphens only";
        }
        return undefined;
      },
    }),
  );

  const normalizedFirstName = String(firstName).trim();
  const normalizedLastName = String(lastName).trim();

  return {
    firstName: normalizedFirstName,
    lastName: normalizedLastName,
    name: `${normalizedFirstName} ${normalizedLastName}`,
    email: String(email).trim().toLowerCase(),
    password: String(enteredPassword),
    organizationName: String(organizationName).trim(),
    organizationSlug: String(organizationSlug).trim().toLowerCase(),
  };
}

async function findOrCreateAdmin({
  firstName,
  lastName,
  name,
  email,
  password: userPassword,
}: {
  firstName: string;
  lastName: string;
  name: string;
  email: string;
  password: string;
}) {
  const existingUser = await findUserByEmail(email);

  if (existingUser) {
    await updateUser(existingUser.id, { firstName, lastName });
    return {
      user: await grantTeamMemberAccess(existingUser.id, "admin"),
      created: false,
    };
  }

  const createdUser = await auth.api.createUser({
    body: {
      name,
      email,
      password: userPassword,
      role: "admin",
      data: {
        firstName,
        lastName,
        emailVerified: true,
      },
    },
  });

  return { user: createdUser.user, created: true };
}

async function findOrCreateOrganization({ name, slug }: { name: string; slug: string }) {
  const existingOrganization = await findBySlug(slug);
  if (existingOrganization) {
    return updateOrganization(existingOrganization.id, { name, slug });
  }

  return createOrganization({ name, slug });
}

async function ensureOrganizationOwner(userId: string, organizationId: string) {
  const membership = await findOrganizationMemberByUserId(organizationId, userId);

  if (membership) {
    if (membership.role !== "owner") {
      await updateMemberRole(membership.id, "owner");
    }
    return;
  }

  await createOrganizationMember({ userId, organizationId, role: "owner" });
}

async function main() {
  try {
    const answers = await promptForAdmin();

    const { user, created } = await findOrCreateAdmin(answers);
    const organization = await findOrCreateOrganization({
      name: answers.organizationName,
      slug: answers.organizationSlug,
    });
    await ensureOrganizationOwner(user.id, organization.id);

    const userResult = created ? "created" : "updated (existing password retained)";
    outro(
      `Admin ${user.email} ${userResult}. Organization "${organization.name}" is ready and the admin is its owner.`,
    );
  } catch (error) {
    if (error instanceof SeedCancelledError) {
      process.exitCode = 1;
    } else if (error instanceof APIError) {
      cancel(`Better Auth API error (${error.status}): ${error.message}`);
    } else {
      cancel("Unexpected error creating the seed admin. Check the logs for details.");
      console.error(error);
    }
    process.exitCode = 1;
  } finally {
    await prisma.$disconnect();
  }
}

void main();
