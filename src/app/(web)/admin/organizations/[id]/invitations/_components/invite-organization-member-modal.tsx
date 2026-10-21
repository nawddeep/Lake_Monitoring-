"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { UserPlus } from "lucide-react";
import { toast } from "sonner";
import { z } from "zod";
import { invitationsApi } from "@/services/api/admin/invitationsApi";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { createCustomerPortalInvitationSchema } from "@/app/api/admin/organizations/[id]/invitations/schema";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { Invitation } from "@/types/invitation";

type FormValues = z.infer<typeof createCustomerPortalInvitationSchema>;

const roleOptions = [
  { value: "member", label: "Member" },
  { value: "admin", label: "Admin" },
  { value: "owner", label: "Owner" },
] as const;

export function InviteOrganizationMemberModal({ organizationId }: { organizationId: string }) {
  const { can } = useAdminPermissions();
  const [open, setOpen] = useState(false);
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const queryClient = useQueryClient();

  const form = useForm<FormValues>({
    resolver: zodResolver(createCustomerPortalInvitationSchema),
    defaultValues: { email: "", role: "member" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: FormValues) => invitationsApi.sendInvitation(organizationId, values),
    onSuccess: (createdInvitation) => {
      setInvitation(createdInvitation);
      toast.success("Invitation created.");
      void queryClient.invalidateQueries({
        queryKey: ["admin", "organizations", organizationId, "invitations"],
      });
    },
  });

  const handleOpenChange = (nextOpen: boolean) => {
    setOpen(nextOpen);
    if (!nextOpen) setInvitation(null);
    if (!nextOpen) {
      form.reset();
    }
  };

  if (!can({ invitation: "create" })) {
    return null;
  }

  return (
    <>
      <Button onClick={() => handleOpenChange(true)}>
        <UserPlus className="h-4 w-4" />
        Invite member
      </Button>

      <Dialog open={open} onOpenChange={handleOpenChange}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{invitation ? "Invitation created" : "Invite a member"}</DialogTitle>
            <DialogDescription>
              {invitation
                ? getInvitationCreatedDescription(invitation)
                : "Send an invitation to join this organization."}
            </DialogDescription>
          </DialogHeader>

          {invitation ? (
            <InvitationLink invitation={invitation} />
          ) : (
            <Form {...form}>
              <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
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

                <FormField
                  control={form.control}
                  name="role"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Organization role</FormLabel>
                      <Select value={field.value} onValueChange={field.onChange}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select role" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {roleOptions.map((option) => (
                            <SelectItem key={option.value} value={option.value}>
                              {option.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <MutationError
                  isError={isError}
                  error={error}
                  fallback="Failed to send invite. Please try again."
                />

                <div className="flex items-center justify-between gap-4">
                  <p className="flex-1 text-sm text-muted-foreground">
                    After creating the invitation, you can copy a link to share directly.
                  </p>
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
