"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { z } from "zod";
import { invitationsApi } from "@/services/api/admin/invitationsApi";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
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
  organizationId: z.string().min(1, "Organization is required"),
});

type FormValues = z.infer<typeof formSchema>;
type Organization = { id: string; name: string };

export function InviteUserForm({
  organizations,
  onSuccess,
}: {
  organizations: Organization[];
  onSuccess?: () => void;
}) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      role: "member",
      organizationId: organizations[0]?.id ?? "",
    },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: async (values: FormValues) => {
      await invitationsApi.sendInvitation(values.organizationId, {
        email: values.email,
        role: values.role,
      });
    },
    onSuccess: () => {
      toast.success("Invitation sent.");
      form.reset();
      onSuccess?.();
    },
  });

  return (
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
          name="organizationId"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Organization</FormLabel>
              <Select value={field.value} onValueChange={field.onChange}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {organizations.map((org) => (
                    <SelectItem key={org.id} value={org.id}>
                      {org.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
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
          fallback="Failed to send invitation. Please try again."
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
  );
}
