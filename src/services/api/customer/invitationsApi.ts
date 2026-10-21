import { customerApiClient } from "@/services/api/client";
import type {
  CreateInvitationBody,
  ListInvitationsParams,
} from "@/app/api/customer/invitations/schema";
import type { PaginationData } from "@/app/api/response";
import type { Invitation } from "@/types/invitation";

export const invitationsApi = {
  list(
    params?: ListInvitationsParams,
  ): Promise<{ data: Invitation[]; pagination: PaginationData }> {
    return customerApiClient.getPaginated<Invitation>("/invitations", {
      sort: params?.sort,
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters: params?.status?.length ? { status: params.status } : undefined,
    });
  },

  create(body: CreateInvitationBody): Promise<Invitation> {
    return customerApiClient.post<Invitation>("/invitations", body);
  },

  cancel(invitationId: string): Promise<void> {
    return customerApiClient.delete(`/invitations/${invitationId}`);
  },
};
