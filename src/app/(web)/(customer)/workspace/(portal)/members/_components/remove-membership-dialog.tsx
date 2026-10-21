"use client";

import { useMembers } from "./members-provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { membersApi } from "@/services/api/customer/membersApi";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";

export function RemoveMembershipDialog() {
  const { open, setOpen, currentMember, currentUserId } = useMembers();
  const queryClient = useQueryClient();
  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => membersApi.remove(currentMember!.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customer", "members"] });
      toast.success("Membership removed.");
      setOpen(null);
    },
    onError: (error) => toast.error(error.message || "Failed to remove membership."),
  });

  if (!currentMember || currentMember.user.id === currentUserId) return null;

  return (
    <DeleteDialog
      open={open === "remove"}
      onOpenChange={(value) => !value && setOpen(null)}
      title="Remove membership"
      description={`${currentMember.user.name} will lose access to this organization. Their user account and other organization memberships will remain unchanged.`}
      onDelete={() => mutateAsync()}
      isPending={isPending}
      confirmLabel="Remove membership"
      confirmPendingLabel="Removing..."
    />
  );
}
