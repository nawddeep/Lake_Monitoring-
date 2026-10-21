import { createAccessControl } from "better-auth/plugins/access";
import {
  adminAc as defaultAdminRole,
  memberAc as defaultMemberRole,
  ownerAc as defaultOwnerRole,
  defaultStatements,
} from "better-auth/plugins/organization/access";

export const organizationAccessControl = createAccessControl({
  ...defaultStatements,
});

export const organizationOwnerRole = organizationAccessControl.newRole({
  ...defaultOwnerRole.statements,
  organization: ["update"],
});

export const organizationAdminRole = organizationAccessControl.newRole({
  ...defaultAdminRole.statements,
});

export const organizationMemberRole = organizationAccessControl.newRole({
  ...defaultMemberRole.statements,
});

export type OrganizationPermissions = {
  [
    K in keyof typeof organizationAccessControl.statements
  ]?: (typeof organizationAccessControl.statements)[K][number][];
};

export type OrganizationPermissionCheck = {
  [K in keyof typeof organizationAccessControl.statements]?:
    | (typeof organizationAccessControl.statements)[K][number]
    | (typeof organizationAccessControl.statements)[K][number][];
};

const organizationRoles = {
  owner: organizationOwnerRole,
  admin: organizationAdminRole,
  member: organizationMemberRole,
} as const;

export function getOrganizationPermissions(role: string | null): OrganizationPermissions {
  if (role === null) {
    return {};
  }

  const assignedRole = organizationRoles[role as keyof typeof organizationRoles];

  if (!assignedRole) {
    throw new Error(`Unknown organization role: ${role}`);
  }

  return assignedRole.statements as unknown as OrganizationPermissions;
}
