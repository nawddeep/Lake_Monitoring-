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

const roleOptions = [
  { value: "member", label: "Member" },
  { value: "admin", label: "Admin" },
  { value: "owner", label: "Owner" },
] as const;

const formSchema = z.object({
  email: z.string().email("Enter a valid email"),
  role: z.enum(["owner", "admin", "member"]),
});

type FormValues = z.infer<typeof formSchema>;

export function InviteUserModal({ organizationId }: { organizationId: string }) {
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", role: "member" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: FormValues) => invitationsApi.sendInvitation(organizationId, values),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "invitations"] });
      toast.success("Invitation sent.");
      handleClose(false);
    },
  });

  const handleClose = (val: boolean) => {
    setOpen(val);
    if (!val) form.reset();
  };

  return (
    <>
      <Button onClick={() => setOpen(true)}>
        <UserPlus className="h-4 w-4" />
        Invite user
      </Button>

      <Dialog open={open} onOpenChange={handleClose}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite a user</DialogTitle>
            <DialogDescription>Send an invitation to join this organization.</DialogDescription>
          </DialogHeader>

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
                    <FormLabel>Role</FormLabel>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue />
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
                  The recipient will receive an email invitation to join.
                </p>
                <PrimaryButton type="submit" isPending={isPending} pendingLabel="Sending...">
                  Send invite
                </PrimaryButton>
              </div>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </>
  );
}
