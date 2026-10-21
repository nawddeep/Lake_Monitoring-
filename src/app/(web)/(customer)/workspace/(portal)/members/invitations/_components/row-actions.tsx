"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { Row } from "@tanstack/react-table";
import { XCircle } from "lucide-react";
import { toast } from "sonner";
import { invitationsApi } from "@/services/api/customer/invitationsApi";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";
import { CopyInvitationLinkItem } from "@/components/invitations/invitation-link";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { useOrganizationPermissions } from "@/context/organization-permission-provider";
import type { Invitation } from "@/types/invitation";

export function InvitationRowActions({ row }: { row: Row<Invitation> }) {
  const { can } = useOrganizationPermissions();
  const invitation = row.original;
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();
  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => invitationsApi.cancel(invitation.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customer", "invitations"] });
      toast.success("Invitation canceled.");
    },
    onError: (error) => toast.error(error.message || "Failed to cancel invitation."),
  });

  if (invitation.status !== "pending") return null;

  return (
    <>
      <RowActionsDropdown>
        <CopyInvitationLinkItem invitation={invitation} />
        {can({ invitation: "cancel" }) && (
          <DropdownMenuItem variant="destructive" onClick={() => setOpen(true)}>
            Cancel invitation
            <XCircle className="ml-auto" />
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
        confirmLabel="Cancel invitation"
        confirmPendingLabel="Canceling..."
      />
    </>
  );
}
