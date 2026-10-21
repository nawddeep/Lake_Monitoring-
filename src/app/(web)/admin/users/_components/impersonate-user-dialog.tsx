"use client";

import { useUsers } from "./users-provider";
import { useMutation } from "@tanstack/react-query";
import { usersApi } from "@/services/api/admin/usersApi";
import { CancelButton } from "@/components/buttons/cancel-button";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export function ImpersonateUserDialog() {
  const { open, setOpen, currentUser, currentUserId } = useUsers();
  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: () => usersApi.impersonateUser(currentUser!.id),
    onSuccess: () => {
      const hasAdminPortalAccess = currentUser!.role !== null;
      const destination = hasAdminPortalAccess ? "/admin/dashboard" : "/workspace";
      window.location.assign(destination);
    },
  });

  if (!currentUser || currentUser.id === currentUserId) return null;

  return (
    <Dialog open={open === "impersonate"} onOpenChange={(value) => !value && setOpen(null)}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Impersonate user</DialogTitle>
          <DialogDescription>
            Continue as {currentUser.name} to see the application with their account and access. You
            can stop impersonating at any time to return to your admin session.
          </DialogDescription>
        </DialogHeader>
        <MutationError
          isError={isError}
          error={error}
          fallback="Failed to impersonate this user. Please try again."
        />
        <DialogFooter>
          <CancelButton onClick={() => setOpen(null)} disabled={isPending} />
          <PrimaryButton onClick={() => mutate()} isPending={isPending} pendingLabel="Starting...">
            Start impersonating
          </PrimaryButton>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
