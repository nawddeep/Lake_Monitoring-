import { adminApiClient } from "@/services/api/client";
import type { ListParams } from "@/services/api/listParams";
import type { UpdateMemberRoleBody } from "@/app/api/admin/organizations/[id]/members/[memberId]/role/schema";
import type { ListOrganizationMembersParams } from "@/app/api/admin/organizations/[id]/members/schema";
import type { PaginationData } from "@/app/api/response";
import type { Member } from "@/types/member";

export const membersApi = {
  listOrganizationMembers(
    organizationId: string,
    params?: ListParams,
  ): Promise<{ data: Member[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<Member>(`/organizations/${organizationId}/members`, {
      search: params?.search,
      sort: params?.sort as ListOrganizationMembersParams["sort"],
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters: params?.filters,
    });
  },

  updateMemberRole(
    organizationId: string,
    memberId: string,
    body: UpdateMemberRoleBody,
  ): Promise<Member> {
    return adminApiClient.patch<Member>(
      `/organizations/${organizationId}/members/${memberId}/role`,
      body,
    );
  },

  deleteMember(organizationId: string, memberId: string): Promise<void> {
    return adminApiClient.delete(`/organizations/${organizationId}/members/${memberId}`);
  },
};
