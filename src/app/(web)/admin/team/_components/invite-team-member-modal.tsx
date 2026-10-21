"use client";

import { useState } from "react";
import { useInviteTeamMemberForm } from "./use-invite-team-member-form";
import { UserPlus } from "lucide-react";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import { RoleSelectField } from "@/components/forms/role-select-field";
import {
  InvitationLink,
  getInvitationCreatedDescription,
} from "@/components/invitations/invitation-link";
import { Button } from "@/components/ui/button";
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
import { Input } from "@/components/ui/input";
import { platformRoleOptions } from "@/constants/roles";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { Invitation } from "@/types/invitation";

export function InviteTeamMemberModal() {
  const { can } = useAdminPermissions();
  const [open, setOpen] = useState(false);
  const [invitation, setInvitation] = useState<Invitation | null>(null);

  const handleClose = () => {
    setOpen(false);
    setInvitation(null);
  };

  const { form, mutate, isPending, isError, error } = useInviteTeamMemberForm(setInvitation);

  if (!can({ invitation: "create" })) {
    return null;
  }

  return (
    <>
      <Button onClick={() => setOpen(true)}>
        <UserPlus className="h-4 w-4" />
        Invite team members
      </Button>

      <Dialog
        open={open}
        onOpenChange={(val) => {
          if (!val) handleClose();
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{invitation ? "Invitation created" : "Invite a team member"}</DialogTitle>
            <DialogDescription>
              {invitation
                ? getInvitationCreatedDescription(invitation)
                : "Create an invitation to join the admin portal."}
            </DialogDescription>
          </DialogHeader>

          {invitation ? (
            <InvitationLink invitation={invitation} />
          ) : (
            <Form {...form}>
              <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
                <p className="text-sm text-muted-foreground">
                  Invitees will add their profile details while accepting the invitation.
                </p>

                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="jane@example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <RoleSelectField
                  control={form.control}
                  name="role"
                  label="Role"
                  description="The role the user will have when accessing the admin portal."
                  options={platformRoleOptions}
                />

                <MutationError
                  isError={isError}
                  error={error}
                  fallback="Failed to send invite. Please try again."
                />

                <div className="flex justify-end">
                  <PrimaryButton type="submit" isPending={isPending} pendingLabel="Sending...">
                    Send invite
                  </PrimaryButton>
                </div>
              </form>
            </Form>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
