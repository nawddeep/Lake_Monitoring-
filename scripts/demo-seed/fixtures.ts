export const demoPassword = "Demo1234!";

export const organizationFixtures = [
  { key: "acme", name: "Acme Corporation", slug: "acme-corporation" },
  { key: "globex", name: "Globex Corporation", slug: "globex-corporation" },
  { key: "initech", name: "Initech", slug: "initech" },
] as const;

export type OrganizationFixtureKey = (typeof organizationFixtures)[number]["key"];
export type OrganizationMemberRole = "owner" | "admin" | "member";
export type PlatformRole = "admin" | "user" | null;

type MembershipFixture = {
  organization: OrganizationFixtureKey;
  role: OrganizationMemberRole;
};

export type UserFixture = {
  firstName: string;
  lastName: string;
  email: string;
  platformRole: PlatformRole;
  banned?: boolean;
  memberships: readonly MembershipFixture[];
};

export const userFixtures: readonly UserFixture[] = [
  {
    firstName: "Alex",
    lastName: "Admin",
    email: "admin@example.test",
    platformRole: "admin",
    memberships: [],
  },
  {
    firstName: "Sam",
    lastName: "Support",
    email: "support@example.test",
    platformRole: "user",
    memberships: [],
  },
  {
    firstName: "Olivia",
    lastName: "Owner",
    email: "owner@acme.test",
    platformRole: null,
    memberships: [{ organization: "acme", role: "owner" }],
  },
  {
    firstName: "Amelia",
    lastName: "Manager",
    email: "manager@acme.test",
    platformRole: null,
    memberships: [{ organization: "acme", role: "admin" }],
  },
  {
    firstName: "Morgan",
    lastName: "Multi",
    email: "multi@example.test",
    platformRole: null,
    memberships: [
      { organization: "acme", role: "member" },
      { organization: "globex", role: "admin" },
      { organization: "initech", role: "member" },
    ],
  },
  {
    firstName: "Harper",
    lastName: "Hybrid",
    email: "hybrid@example.test",
    platformRole: "user",
    memberships: [{ organization: "globex", role: "owner" }],
  },
  {
    firstName: "Ian",
    lastName: "Owner",
    email: "owner@initech.test",
    platformRole: null,
    memberships: [{ organization: "initech", role: "owner" }],
  },
  {
    firstName: "Bailey",
    lastName: "Banned",
    email: "banned@example.test",
    platformRole: null,
    banned: true,
    memberships: [{ organization: "globex", role: "member" }],
  },
];
