"use client";

import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
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
import { type ResetPasswordBody, resetPasswordSchema } from "@/app/api/auth/reset-password/schema";

export function ResetPasswordForm({ token }: { token: string }) {
  const router = useRouter();

  const form = useForm<ResetPasswordBody>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { token, newPassword: "" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: ResetPasswordBody) => authApi.resetPassword(values),
    onSuccess: () => {
      toast.success("Password set. You can now sign in.");
      router.push("/login");
    },
  });

  return (
    <Form {...form}>
      <form
        className="space-y-4"
        noValidate
        onSubmit={form.handleSubmit((values) => mutate(values))}
      >
        <FormField
          control={form.control}
          name="newPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>New password</FormLabel>
              <FormControl>
                <Input type="password" autoComplete="new-password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <MutationError
          isError={isError}
          error={error}
          fallback="Unable to set password. The link may have expired."
        />

        <PrimaryButton
          className="w-full"
          type="submit"
          isPending={isPending}
          pendingLabel="Setting password..."
        >
          Set password
        </PrimaryButton>
      </form>
    </Form>
  );
}
