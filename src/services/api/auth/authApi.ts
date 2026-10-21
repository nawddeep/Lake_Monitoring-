import type { SessionResult } from "@/lib/auth/session";
import { apiClient } from "@/services/api/client";
import type { UpdateAccountBody } from "@/app/api/auth/account/schema";
import type { AcceptExistingAdminInvitationBody } from "@/app/api/auth/admin/invitations/accept-existing/schema";
import type { AcceptAdminInvitationBody } from "@/app/api/auth/admin/invitations/accept/schema";
import type { ChangePasswordBody } from "@/app/api/auth/change-password/schema";
import type { AcceptCustomerInvitationBody } from "@/app/api/auth/customer/invitations/[invitationId]/accept/schema";
import type { LoginBody } from "@/app/api/auth/login/schema";
import type { CheckPermissionsBody } from "@/app/api/auth/permissions/check/schema";
import type { ResetPasswordBody } from "@/app/api/auth/reset-password/schema";
import type { SetActiveOrganizationBody } from "@/app/api/auth/session/active-organization/schema";
import type { Organization } from "@/types/organization";

export const authApi = {
  updateAccount: (body: UpdateAccountBody) => apiClient.patch<void>("/auth/account", body),
  signIn: (body: LoginBody) => apiClient.post<void>("/auth/login", body),
  signOut: () => apiClient.post<void>("/auth/logout", {}),
  stopImpersonating: () => apiClient.post<void>("/auth/impersonation/stop", {}),
  changePassword: (body: ChangePasswordBody) => apiClient.post<void>("/auth/change-password", body),
  resetPassword: (body: ResetPasswordBody) => apiClient.post<void>("/auth/reset-password", body),
  getSession: () => apiClient.get<SessionResult>("/auth/session"),
  listOrganizations: () => apiClient.get<Organization[]>("/auth/session/organizations"),
  setActiveOrganization: (body: SetActiveOrganizationBody) =>
    apiClient.patch<void>("/auth/session/active-organization", body),
  checkPermissions: (body: CheckPermissionsBody) =>
    apiClient.post<{ allowed: boolean }>("/auth/permissions/check", body),
  acceptAdminInvitation: (body: AcceptAdminInvitationBody) =>
    apiClient.post<{ message: string }>("/auth/admin/invitations/accept", body),
  acceptExistingAdminInvitation: (body: AcceptExistingAdminInvitationBody) =>
    apiClient.post<void>("/auth/admin/invitations/accept-existing", body),
  acceptCustomerInvitation: ({
    invitationId,
    ...body
  }: AcceptCustomerInvitationBody & { invitationId: string }) =>
    apiClient.post<{ message: string }>(`/auth/customer/invitations/${invitationId}/accept`, body),
};
