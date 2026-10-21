"use client";

import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { z } from "zod";
import { authApi } from "@/services/api/auth/authApi";
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
import { acceptAdminInvitationSchema } from "@/app/api/auth/admin/invitations/accept/schema";

const formSchema = acceptAdminInvitationSchema.omit({ invitationId: true });

type AcceptAdminInvitationFormValues = z.infer<typeof formSchema>;

type AcceptAdminInvitationFormProps = {
  invitationId: string;
  email: string;
};

export function AcceptAdminInvitationForm({ invitationId, email }: AcceptAdminInvitationFormProps) {
  const router = useRouter();

  const form = useForm<AcceptAdminInvitationFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { firstName: "", lastName: "", password: "" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: AcceptAdminInvitationFormValues) =>
      authApi.acceptAdminInvitation({ ...values, invitationId }),
    onSuccess: () => {
      router.push("/admin/dashboard");
    },
  });

  return (
    <Form {...form}>
      <form
        className="space-y-5"
        noValidate
        onSubmit={form.handleSubmit((values) => mutate(values))}
      >
        <p className="text-sm text-muted-foreground">Accepting invitation for {email}</p>

        <div className="grid gap-4 md:grid-cols-2">
          <FormField
            control={form.control}
            name="firstName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>First name</FormLabel>
                <FormControl>
                  <Input autoComplete="given-name" placeholder="Jane" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="lastName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Last name</FormLabel>
                <FormControl>
                  <Input autoComplete="family-name" placeholder="Smith" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  autoComplete="new-password"
                  placeholder="Create a secure password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <MutationError
          isError={isError}
          error={error}
          fallback="Unable to accept the invitation. Please try again."
        />

        <PrimaryButton type="submit" isPending={isPending} pendingLabel="Joining...">
          Join the admin portal
        </PrimaryButton>
      </form>
    </Form>
  );
}
