"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useUsers } from "./users-provider";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { usersApi } from "@/services/api/admin/usersApi";
import { CancelButton } from "@/components/buttons/cancel-button";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { type BanUserBody, banUserSchema } from "@/app/api/admin/users/[id]/ban/schema";

export function BanUserDialog() {
  const { open, setOpen, currentUser, currentUserId } = useUsers();
  const queryClient = useQueryClient();
  const form = useForm<BanUserBody>({
    resolver: zodResolver(banUserSchema),
    defaultValues: { banReason: "" },
  });

  useEffect(() => {
    if (open === "ban") form.reset({ banReason: "" });
  }, [open, form]);

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: BanUserBody) => usersApi.banUser(currentUser!.id, values),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      toast.success("User banned.");
      setOpen(null);
    },
  });

  if (!currentUser || currentUser.id === currentUserId) return null;

  return (
    <Dialog open={open === "ban"} onOpenChange={(value) => !value && setOpen(null)}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Ban user</DialogTitle>
          <DialogDescription>
            Prevent {currentUser.name} from signing in. You can optionally provide a reason.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
            <FormField
              control={form.control}
              name="banReason"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Reason (optional)</FormLabel>
                  <FormControl>
                    <Textarea placeholder="Reason for banning the user" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <MutationError
              isError={isError}
              error={error}
              fallback="Failed to ban user. Please try again."
            />
            <div className="flex justify-end gap-2">
              <CancelButton onClick={() => setOpen(null)} disabled={isPending} />
              <PrimaryButton type="submit" isPending={isPending} pendingLabel="Banning...">
                Ban user
              </PrimaryButton>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
