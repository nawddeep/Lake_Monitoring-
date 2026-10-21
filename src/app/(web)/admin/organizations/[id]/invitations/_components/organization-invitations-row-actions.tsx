"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { Row } from "@tanstack/react-table";
import { XCircle } from "lucide-react";
import { toast } from "sonner";
import { invitationsApi } from "@/services/api/admin/invitationsApi";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";
import { CopyInvitationLinkItem } from "@/components/invitations/invitation-link";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { Invitation } from "@/types/invitation";

export function OrganizationInvitationRowActions({
  organizationId,
  row,
}: {
  organizationId: string;
  row: Row<Invitation>;
}) {
  const { can } = useAdminPermissions();
  const invitation = row.original;
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();

  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => invitationsApi.cancelOrganizationInvitation(organizationId, invitation.id),
    onSuccess: () => {
      toast.success("Invitation canceled.");
      void queryClient.invalidateQueries({
        queryKey: ["admin", "organizations", organizationId, "invitations"],
      });
    },
    onError: (err) => {
      const message = err instanceof Error ? err.message : "Failed to cancel invitation.";
      toast.error(message);
    },
  });

  if (invitation.status !== "pending") {
    return null;
  }

  return (
    <>
      <RowActionsDropdown>
        <CopyInvitationLinkItem invitation={invitation} />
        {can({ invitation: "cancel" }) && (
          <DropdownMenuItem
            className="text-destructive focus:text-destructive"
            onClick={() => setOpen(true)}
          >
            Cancel invitation
            <XCircle size={16} className="ml-auto" />
          </DropdownMenuItem>
        )}
      </RowActionsDropdown>

      <DeleteDialog
        open={open}
        onOpenChange={setOpen}
        title="Cancel invitation"
        description={`Are you sure you want to cancel the invitation for ${invitation.email}?`}
        onDelete={() => mutateAsync()}
        isPending={isPending}
        confirmLabel="Cancel invite"
        confirmPendingLabel="Canceling..."
      />
    </>
  );
}
