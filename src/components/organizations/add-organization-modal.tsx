"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { type QueryKey, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus } from "lucide-react";
import { toast } from "sonner";
import { adminApiClient } from "@/services/api/client";
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
  type CreateOrganizationBody,
  createOrganizationSchema,
} from "@/app/api/admin/organizations/schema";

const formSchema = createOrganizationSchema;

type FormValues = CreateOrganizationBody;

function toSlug(value: string) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

export function AddOrganizationModal({
  queryKey = ["admin", "organizations"],
}: {
  queryKey?: QueryKey;
}) {
  const [open, setOpen] = useState(false);
  const [slugManuallyEdited, setSlugManuallyEdited] = useState(false);
  const queryClient = useQueryClient();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", slug: "" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: async (values: FormValues) => {
      await adminApiClient.post<{ message: string }>("/organizations", values);
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey });
      toast.success("Organization created.");
      handleClose(false);
    },
  });

  const handleClose = (val: boolean) => {
    setOpen(val);
    if (!val) {
      form.reset();
      setSlugManuallyEdited(false);
    }
  };

  return (
    <>
      <Button onClick={() => setOpen(true)}>
        <Plus className="h-4 w-4" />
        Add organization
      </Button>

      <Dialog open={open} onOpenChange={handleClose}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add organization</DialogTitle>
            <DialogDescription>
              Create a new customer organization on the platform.
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form className="space-y-5" onSubmit={form.handleSubmit((values) => mutate(values))}>
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Acme Inc."
                        {...field}
                        onChange={(e) => {
                          field.onChange(e);
                          if (!slugManuallyEdited) {
                            form.setValue("slug", toSlug(e.target.value), { shouldValidate: true });
                          }
                        }}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="slug"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Slug</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="acme-inc"
                        {...field}
                        onChange={(e) => {
                          setSlugManuallyEdited(true);
                          field.onChange(e);
                        }}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <MutationError
                isError={isError}
                error={error}
                fallback="Failed to create organization. Please try again."
              />

              <div className="flex justify-end">
                <PrimaryButton type="submit" isPending={isPending} pendingLabel="Creating...">
                  Create organization
                </PrimaryButton>
              </div>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </>
  );
}
