import { adminApiClient } from "@/services/api/client";
import type { CreateAdminPortalInvitationBody } from "@/app/api/admin/team/invitations/schema";
import { ListTeamMembersParams } from "@/app/api/admin/team/members/schema";
import type { PaginationData } from "@/app/api/response";
import type { Invitation } from "@/types/invitation";
import type { User } from "@/types/user";

export const teamApi = {
  listTeamMembers(
    params?: ListTeamMembersParams & { filters?: Record<string, string[]> },
  ): Promise<{ data: User[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<User>("/team/members", params);
  },

  inviteMember(body: CreateAdminPortalInvitationBody): Promise<Invitation> {
    return adminApiClient.post<Invitation>("/team/invitations", body);
  },

  revokeAdminPortalAccess(id: string): Promise<void> {
    return adminApiClient.delete(`/team/members/${id}`);
  },

  changeRole(id: string, role: "admin" | "user"): Promise<User> {
    return adminApiClient.patch<User>(`/team/members/${id}/role`, { role });
  },
};
