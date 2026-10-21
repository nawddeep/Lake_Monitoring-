"use client";

import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import type { Invitation } from "@/types/invitation";

async function copyInvitationLink(invitation: Invitation) {
  try {
    await navigator.clipboard.writeText(
      new URL(invitation.invitationUrl, window.location.origin).href,
    );
    toast.success("Invitation link copied.");
  } catch {
    toast.error("Unable to copy the invitation link. Please try again.");
  }
}

export function CopyInvitationLinkItem({ invitation }: { invitation: Invitation }) {
  if (invitation.status !== "pending" || new Date(invitation.expiresAt) <= new Date()) return null;
  return (
    <DropdownMenuItem onClick={() => void copyInvitationLink(invitation)}>
      Copy invitation link
    </DropdownMenuItem>
  );
}

export function getInvitationCreatedDescription(invitation: Invitation) {
  if (invitation.emailStatus === "sent") {
    return "Invitation email sent. You can also copy this link and share it directly.";
  }
  if (invitation.emailStatus === "failed") {
    return "We couldn’t send the email. Copy this link and share it directly.";
  }
  if (invitation.emailStatus === "not_sent") {
    return "No email was sent to the user. Copy this link and share it directly.";
  }
  return "Copy this link and share it directly.";
}

export function InvitationLink({ invitation }: { invitation: Invitation }) {
  return (
    <div className="space-y-6">
      <dl className="grid grid-cols-[auto_minmax(0,1fr)] gap-x-6 gap-y-3 text-sm">
        <dt className="text-muted-foreground">Recipient</dt>
        <dd className="break-all font-medium">{invitation.email}</dd>
        <dt className="text-muted-foreground">Expires</dt>
        <dd>{new Date(invitation.expiresAt).toLocaleString()}</dd>
      </dl>
      <Button className="w-full" onClick={() => void copyInvitationLink(invitation)}>
        Copy invitation link
      </Button>
    </div>
  );
}
