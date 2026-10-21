"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { UserPlus } from "lucide-react";
import { toast } from "sonner";
import { invitationsApi } from "@/services/api/customer/invitationsApi";
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
import {
  type CreateInvitationBody,
  createInvitationSchema,
} from "@/app/api/customer/invitations/schema";
import { useOrganizationPermissions } from "@/context/organization-permission-provider";
import type { Invitation } from "@/types/invitation";

const roleOptions = [
  { value: "member", label: "Member" },
  { value: "admin", label: "Admin" },
  { value: "owner", label: "Owner" },
] as const;

export function InviteMemberModal() {
  const { can } = useOrganizationPermissions();
  const [open, setOpen] = useState(false);
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const queryClient = useQueryClient();
  const form = useForm<CreateInvitationBody>({
    resolver: zodResolver(createInvitationSchema),
    defaultValues: { email: "", role: "member" },
  });

  const handleOpenChange = (nextOpen: boolean) => {
    setOpen(nextOpen);
    if (!nextOpen) setInvitation(null);
    if (!nextOpen) form.reset();
  };

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: CreateInvitationBody) => invitationsApi.create(values),
    onSuccess: (createdInvitation) => {
      setInvitation(createdInvitation);
      void queryClient.invalidateQueries({ queryKey: ["customer", "invitations"] });
      toast.success("Invitation created.");
    },
  });

  if (!can({ invitation: "create" })) {
    return null;
  }

  return (
    <>
      <Button onClick={() => handleOpenChange(true)}>
        <UserPlus />
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
                  fallback="Failed to send the invitation."
                />
                <div className="flex justify-end">
                  <PrimaryButton type="submit" isPending={isPending} pendingLabel="Sending...">
                    Send invitation
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
