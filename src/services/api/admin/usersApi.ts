import { adminApiClient } from "@/services/api/client";
import type { BanUserBody } from "@/app/api/admin/users/[id]/ban/schema";
import type { ListUsersParams } from "@/app/api/admin/users/schema";
import type { PaginationData } from "@/app/api/response";
import type { User, UserWithAccess } from "@/types/user";

export const usersApi = {
  listUsers(
    params?: ListUsersParams & { filters?: Record<string, string[]> },
  ): Promise<{ data: UserWithAccess[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<UserWithAccess>("/users", params);
  },

  deleteUser(id: string): Promise<void> {
    return adminApiClient.delete(`/users/${id}`);
  },

  banUser(id: string, body: BanUserBody): Promise<User> {
    return adminApiClient.post<User>(`/users/${id}/ban`, body);
  },

  unbanUser(id: string): Promise<User> {
    return adminApiClient.post<User>(`/users/${id}/unban`, {});
  },

  impersonateUser(id: string): Promise<void> {
    return adminApiClient.post<void>(`/users/${id}/impersonate`, {});
  },
};
