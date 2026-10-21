"use client";

import { useUsers } from "./users-provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { usersApi } from "@/services/api/admin/usersApi";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";

export function DeleteUserDialog() {
  const { open, setOpen, currentUser, currentUserId } = useUsers();
  const queryClient = useQueryClient();

  const { mutateAsync, isPending } = useMutation({
    mutationFn: () => usersApi.deleteUser(currentUser!.id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      toast.success("User deleted.");
      setOpen(null);
    },
  });

  if (!currentUser || currentUser.id === currentUserId) return null;

  return (
    <DeleteDialog
      open={open === "delete"}
      onOpenChange={(value) => !value && setOpen(null)}
      title="Delete user"
      description={`This permanently deletes ${currentUser.name} and all associated access. This action cannot be undone.`}
      onDelete={mutateAsync}
      isPending={isPending}
      confirmLabel="Delete"
      confirmPendingLabel="Deleting..."
    />
  );
}
