import { customerApiClient } from "@/services/api/client";
import type { ListParams } from "@/services/api/listParams";
import type { UpdateMemberRoleBody } from "@/app/api/customer/members/[memberId]/role/schema";
import type { ListMembersParams } from "@/app/api/customer/members/schema";
import type { PaginationData } from "@/app/api/response";
import type { Member } from "@/types/member";

export const membersApi = {
  list(params?: ListParams): Promise<{ data: Member[]; pagination: PaginationData }> {
    return customerApiClient.getPaginated<Member>("/members", {
      search: params?.search,
      sort: params?.sort as ListMembersParams["sort"],
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters: params?.filters,
    });
  },

  updateRole(memberId: string, body: UpdateMemberRoleBody): Promise<Member> {
    return customerApiClient.patch<Member>(`/members/${memberId}/role`, body);
  },

  remove(memberId: string): Promise<void> {
    return customerApiClient.delete(`/members/${memberId}`);
  },
};
