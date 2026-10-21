"use client";

import { useForm } from "react-hook-form";
import { useMembers } from "./members-provider";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { membersApi } from "@/services/api/customer/membersApi";
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
import {
  type UpdateMemberRoleBody,
  updateMemberRoleSchema,
} from "@/app/api/customer/members/[memberId]/role/schema";

const roleOptions = [
  { value: "owner", label: "Owner" },
  { value: "admin", label: "Admin" },
  { value: "member", label: "Member" },
] as const;

export function ChangeMemberRoleDialog() {
  const { open, setOpen, currentMember, currentUserId } = useMembers();
  const queryClient = useQueryClient();
  const form = useForm<UpdateMemberRoleBody>({
    resolver: zodResolver(updateMemberRoleSchema),
    values: { role: (currentMember?.role as UpdateMemberRoleBody["role"]) ?? "member" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: UpdateMemberRoleBody) => membersApi.updateRole(currentMember!.id, values),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customer", "members"] });
      toast.success("Membership role updated.");
      setOpen(null);
    },
  });

  if (!currentMember || currentMember.user.id === currentUserId) return null;

  return (
    <Dialog open={open === "change-role"} onOpenChange={(value) => !value && setOpen(null)}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Change role</DialogTitle>
          <DialogDescription>
            Update the organization role for {currentMember.user.name}.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
            <RoleSelectField
              control={form.control}
              name="role"
              label="Role"
              options={roleOptions}
            />
            <MutationError
              isError={isError}
              error={error}
              fallback="Failed to update membership role."
            />
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
