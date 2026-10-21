import { adminApiClient } from "@/services/api/client";
import type { CreateCustomerPortalInvitationBody } from "@/app/api/admin/organizations/[id]/invitations/schema";
import type { ListAdminPortalInvitationsParams } from "@/app/api/admin/team/invitations/schema";
import type { PaginationData } from "@/app/api/response";
import type { Invitation } from "@/types/invitation";

export const invitationsApi = {
  listAdminPortalInvitations(
    params?: ListAdminPortalInvitationsParams,
  ): Promise<{ data: Invitation[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<Invitation>("/team/invitations", {
      sort: params?.sort,
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters: params?.status && params.status.length > 0 ? { status: params.status } : undefined,
    });
  },

  sendInvitation(organizationId: string, params: CreateCustomerPortalInvitationBody) {
    return adminApiClient.post<Invitation>(`/organizations/${organizationId}/invitations`, params);
  },

  cancelOrganizationInvitation(organizationId: string, invitationId: string) {
    return adminApiClient.delete(`/organizations/${organizationId}/invitations/${invitationId}`);
  },

  cancelAdminTeamInvitation(invitationId: string) {
    return adminApiClient.delete(`/team/invitations/${invitationId}`);
  },
};
