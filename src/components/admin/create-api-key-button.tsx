"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { KeyRound } from "lucide-react";
import { accountApiKeysApi } from "@/services/api/admin/account/apiKeysApi";
import { CopyButton } from "@/components/buttons/copy-button";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
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
import { type CreateApiKeyBody, createApiKeySchema } from "@/app/api/admin/api-keys/schema";

export function CreateApiKeyButton({ queryKey }: { queryKey: string[] }) {
  const [open, setOpen] = useState(false);
  const [createdKey, setCreatedKey] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const form = useForm<CreateApiKeyBody>({
    resolver: zodResolver(createApiKeySchema),
    defaultValues: { name: "" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: CreateApiKeyBody) => accountApiKeysApi.createApiKey(values),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey });
      setCreatedKey(result.key);
    },
  });

  const handleClose = (val: boolean) => {
    setOpen(val);
    if (!val) {
      form.reset();
      setCreatedKey(null);
    }
  };

  return (
    <>
      <PrimaryButton onClick={() => setOpen(true)}>
        <KeyRound className="h-4 w-4" />
        Create API key
      </PrimaryButton>

      <Dialog open={open} onOpenChange={handleClose}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{createdKey ? "API key created" : "Create API key"}</DialogTitle>
            <DialogDescription>
              {createdKey
                ? "Copy your key now and store it somewhere safely — it won't be shown again."
                : "This API key will be owned by you and tied to your account. Keep it secret and do not share it with others."}
            </DialogDescription>
          </DialogHeader>

          {createdKey ? (
            <div className="space-y-4">
              <div className="flex items-center gap-2 rounded-md border bg-muted px-3 py-2">
                <code className="flex-1 break-all text-sm">{createdKey}</code>
                <CopyButton value={createdKey} />
              </div>
              <PrimaryButton className="w-full" onClick={() => handleClose(false)}>
                Done
              </PrimaryButton>
            </div>
          ) : (
            <Form {...form}>
              <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Name</FormLabel>
                      <FormControl>
                        <Input placeholder="e.g. Production" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <MutationError
                  isError={isError}
                  error={error}
                  fallback="Unable to create API key. Please try again."
                />

                <div className="flex justify-end">
                  <PrimaryButton type="submit" isPending={isPending} pendingLabel="Creating...">
                    Create key
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
