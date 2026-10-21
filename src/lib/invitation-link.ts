import { Portal } from "@/config/portals";

export function getInvitationPath(invitation: { id: string; portal: string }) {
  const portalPath = invitation.portal === Portal.admin ? "admin-portal" : "customer-portal";
  return `/accept-invitation/${portalPath}/${encodeURIComponent(invitation.id)}`;
}
