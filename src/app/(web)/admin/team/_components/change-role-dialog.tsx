"use client";

import { useForm } from "react-hook-form";
import { useMembers } from "./members-provider";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { z } from "zod";
import { teamApi } from "@/services/api/admin/teamApi";
import { CancelButton } from "@/components/buttons/cancel-button";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import { RoleSelectField } from "@/components/forms/role-select-field";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Form } from "@/components/ui/form";

const PLATFORM_ROLES = [
  { value: "admin", label: "Admin" },
  { value: "user", label: "User" },
] as const;

const changeRoleSchema = z.object({
  role: z.enum(["admin", "user"]),
});

type ChangeRoleValues = z.infer<typeof changeRoleSchema>;

export function ChangeRoleDialog() {
  const { open, setOpen, currentRow } = useMembers();
  const queryClient = useQueryClient();

  const form = useForm<ChangeRoleValues>({
    resolver: zodResolver(changeRoleSchema),
    values: { role: (currentRow?.role as "admin" | "user") ?? "user" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: ChangeRoleValues) => teamApi.changeRole(currentRow!.id, values.role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "team"] });
      toast.success("Role updated.");
      setOpen(null);
    },
  });

  return (
    <Dialog open={open === "change-role"} onOpenChange={(val) => !val && setOpen(null)}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Change role</DialogTitle>
          <DialogDescription>
            Update the admin portal role for {currentRow?.name}.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
            <RoleSelectField
              control={form.control}
              name="role"
              label="Role"
              options={PLATFORM_ROLES}
            />
            <MutationError isError={isError} error={error} fallback="Failed to update role." />
            <div className="flex justify-end gap-2">
              <CancelButton onClick={() => setOpen(null)} disabled={isPending} />
              <PrimaryButton type="submit" isPending={isPending} pendingLabel="Saving...">
                Save
              </PrimaryButton>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
