"use client";

import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
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
import { type LoginBody, loginSchema } from "@/app/api/auth/login/schema";

type LoginFormProps = {
  callbackUrl?: string;
  initialEmail?: string;
};

export function LoginForm({ callbackUrl = "/admin/dashboard", initialEmail = "" }: LoginFormProps) {
  const router = useRouter();

  const form = useForm<LoginBody>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: initialEmail, password: "" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: LoginBody) => authApi.signIn(values),
    onSuccess: () => router.push(callbackUrl),
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
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" autoComplete="email" placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" autoComplete="current-password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <MutationError
          isError={isError}
          error={error}
          fallback="Unable to sign in. Please try again."
        />

        <PrimaryButton
          className="w-full"
          type="submit"
          isPending={isPending}
          pendingLabel="Signing in..."
        >
          Sign in
        </PrimaryButton>
      </form>
    </Form>
  );
}
