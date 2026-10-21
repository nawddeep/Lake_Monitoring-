import { adminApiClient } from "@/services/api/client";
import type { ListParams } from "@/services/api/listParams";
import type { ListOrganizationInvitationsParams } from "@/app/api/admin/organizations/[id]/invitations/schema";
import type { ListOrganizationMembersParams } from "@/app/api/admin/organizations/[id]/members/schema";
import type { UpdateOrganizationBody } from "@/app/api/admin/organizations/schema";
import type { PaginationData } from "@/app/api/response";
import type { Invitation } from "@/types/invitation";
import type { Member } from "@/types/member";
import type { Organization } from "@/types/organization";

export const organizationsApi = {
  listOrganizations(
    params?: ListParams,
  ): Promise<{ data: Organization[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<Organization>("/organizations", params);
  },

  getOrganization(id: string): Promise<Organization> {
    return adminApiClient.get<Organization>(`/organizations/${id}`);
  },

  updateOrganization(id: string, body: UpdateOrganizationBody): Promise<Organization> {
    return adminApiClient.patch<Organization>(`/organizations/${id}`, body);
  },

  deleteOrganization(id: string): Promise<void> {
    return adminApiClient.delete(`/organizations/${id}`);
  },

  listOrganizationMembers(
    id: string,
    params?: ListParams & Partial<ListOrganizationMembersParams>,
  ): Promise<{ data: Member[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<Member>(`/organizations/${id}/members`, {
      search: params?.search,
      sort: params?.sort,
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters:
        params?.filters ??
        (params?.status && params.status.length > 0 ? { status: params.status } : undefined),
    });
  },

  listOrganizationInvitations(
    id: string,
    params?: ListParams & Partial<ListOrganizationInvitationsParams>,
  ): Promise<{ data: Invitation[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<Invitation>(`/organizations/${id}/invitations`, {
      sort: params?.sort,
      order: params?.order,
      page: params?.page ?? 1,
      perPage: params?.perPage ?? 10,
      filters:
        params?.filters ??
        (params?.status && params.status.length > 0 ? { status: params.status } : undefined),
    });
  },
};
