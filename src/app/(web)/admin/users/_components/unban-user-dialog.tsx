"use client";

import { useUsers } from "./users-provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { usersApi } from "@/services/api/admin/usersApi";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";

export function UnbanUserDialog() {
  const { open, setOpen, currentUser, currentUserId } = useUsers();
  const queryClient = useQueryClient();

  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => usersApi.unbanUser(currentUser!.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      toast.success("User unbanned.");
      setOpen(null);
    },
  });

  if (!currentUser || currentUser.id === currentUserId) return null;

  return (
    <DeleteDialog
      open={open === "unban"}
      onOpenChange={(value) => !value && setOpen(null)}
      title="Unban user"
      description={`${currentUser.name} will be able to sign in again.`}
      onDelete={async () => {
        await mutateAsync();
      }}
      isPending={isPending}
      confirmLabel="Unban"
      confirmPendingLabel="Unbanning..."
    />
  );
}
