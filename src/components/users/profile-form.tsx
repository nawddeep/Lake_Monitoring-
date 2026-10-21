"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { authApi } from "@/services/api/auth/authApi";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { type UpdateAccountBody, updateAccountSchema } from "@/app/api/auth/account/schema";
import type { User } from "@/types/user";

export function ProfileForm({ user }: { user: User }) {
  const form = useForm<UpdateAccountBody>({
    resolver: zodResolver(updateAccountSchema),
    defaultValues: {
      firstName: user.firstName,
      lastName: user.lastName,
    },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: UpdateAccountBody) => authApi.updateAccount(values),
    onSuccess: () => toast.success("Profile updated."),
  });

  return (
    <Card className="max-w-xl">
      <CardHeader>
        <CardTitle>Profile</CardTitle>
        <CardDescription>Update your name and profile details</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
            <div className="space-y-1">
              <label className="text-sm font-medium leading-none">Email</label>
              <Input value={user.email} disabled />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="firstName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>First name</FormLabel>
                    <FormControl>
                      <Input placeholder="Jane" {...field} />
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
                      <Input placeholder="Smith" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <MutationError
              isError={isError}
              error={error}
              fallback="Failed to update profile. Please try again."
            />

            <div className="flex justify-end">
              <PrimaryButton type="submit" isPending={isPending} pendingLabel="Saving...">
                Save changes
              </PrimaryButton>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
