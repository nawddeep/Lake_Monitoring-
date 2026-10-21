export const platformRoleOptions = [
  { value: "admin", label: "Admin" },
  { value: "user", label: "User" },
] as const;

export const orgRoleOptions = [
  { value: "owner", label: "Owner" },
  { value: "admin", label: "Admin" },
  { value: "member", label: "Member" },
] as const;

export type PlatformRole = (typeof platformRoleOptions)[number]["value"];
export type OrgRole = (typeof orgRoleOptions)[number]["value"];
