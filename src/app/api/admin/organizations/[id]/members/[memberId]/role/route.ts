import { updateMemberRoleSchema } from "./schema";
import {
  countOrganizationOwners,
  findOrganizationMember,
  updateMemberRole,
} from "@/repositories/admin/memberRepository";
import { serializeMember } from "@/serializers/memberSerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import {
  conflictResponse,
  detailResponse,
  forbiddenResponse,
  notFoundResponse,
} from "@/app/api/response";

export const PATCH = withAdmin(
  async (request, { params }, { user }) => {
    const { id: organizationId, memberId } = await params;

    const existing = await findOrganizationMember(organizationId, memberId);
    if (!existing) return notFoundResponse();
    if (existing.userId === user.id) {
      return forbiddenResponse("You cannot change your own organization role.");
    }

    const body = updateMemberRoleSchema.parse(await request.json());
    if (
      existing.role === "owner" &&
      body.role !== "owner" &&
      (await countOrganizationOwners(organizationId)) <= 1
    ) {
      return conflictResponse("You cannot change the role of the organization's final owner.");
    }

    const updated = await updateMemberRole(memberId, body.role);

    return detailResponse(serializeMember(updated));
  },
  { member: ["update"] },
);
