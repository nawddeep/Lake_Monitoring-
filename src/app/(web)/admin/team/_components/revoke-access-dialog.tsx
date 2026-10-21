"use client";

import { useMembers } from "./members-provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { teamApi } from "@/services/api/admin/teamApi";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";

export function RevokeAccessDialog() {
  const { open, setOpen, currentRow, currentUserId } = useMembers();
  const queryClient = useQueryClient();

  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => teamApi.revokeAdminPortalAccess(currentRow!.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "team"] });
      toast.success("Admin portal access revoked.");
      setOpen(null);
    },
    onError: (error) => {
      toast.error(error.message || "Failed to revoke admin portal access.");
    },
  });

  if (!currentRow || currentRow.id === currentUserId) return null;

  return (
    <DeleteDialog
      open={open === "revoke-access"}
      onOpenChange={(value) => !value && setOpen(null)}
      title="Revoke admin portal access"
      description={`${currentRow.name} will lose access to the admin portal. Their user account and organization memberships will remain unchanged.`}
      onDelete={mutateAsync}
      isPending={isPending}
      confirmLabel="Revoke access"
      confirmPendingLabel="Revoking..."
    />
  );
}
