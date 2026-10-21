import {
  countOrganizationOwners,
  deleteMember,
  findOrganizationMember,
} from "@/repositories/customers/memberRepository";
import { withCustomer } from "@/app/api/customer/with-customer";
import {
  conflictResponse,
  forbiddenResponse,
  noContentResponse,
  notFoundResponse,
} from "@/app/api/response";

export const DELETE = withCustomer(
  async (_request, { params }, { organizationId, user }) => {
    const { memberId } = await params;
    const member = await findOrganizationMember(organizationId, memberId);
    if (!member) return notFoundResponse("Member not found.");
    if (member.userId === user.id) {
      return forbiddenResponse("You cannot remove your own membership.");
    }
    if (member.role === "owner" && (await countOrganizationOwners(organizationId)) <= 1) {
      return conflictResponse("You cannot remove the organization's final owner.");
    }

    await deleteMember(memberId);
    return noContentResponse();
  },
  { member: ["delete"] },
);
