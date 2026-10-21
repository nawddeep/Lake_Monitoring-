import { demoPassword, userFixtures } from "./fixtures";
import { config } from "dotenv";
import process from "node:process";

config();

async function main() {
  if (process.env.NODE_ENV === "production") {
    throw new Error("Demo data cannot be seeded in production.");
  }

  const [{ seedDemoData }, { prisma }] = await Promise.all([
    import("./seed"),
    import("@/lib/prisma"),
  ]);

  try {
    const result = await seedDemoData();

    console.log("Demo data is ready.");
    console.table(result);
    console.log(`Password for newly created demo users: ${demoPassword}`);
    console.table(
      userFixtures.map(({ email, platformRole, banned, memberships }) => ({
        email,
        adminPortalRole: platformRole ?? "none",
        organizations: memberships
          .map(({ organization, role }) => `${organization}:${role}`)
          .join(", "),
        banned: banned ?? false,
      })),
    );
    console.log("Existing users retain their current passwords.");
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((error) => {
  console.error("Failed to seed demo data.");
  console.error(error);
  process.exitCode = 1;
});
