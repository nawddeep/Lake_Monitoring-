"use client";

import { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { useOrganizations } from "./organizations-provider";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { organizationsApi } from "@/services/api/admin/organizationsApi";
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
import {
  type UpdateOrganizationBody,
  updateOrganizationSchema,
} from "@/app/api/admin/organizations/schema";

const formSchema = updateOrganizationSchema;

type FormValues = UpdateOrganizationBody;

function toSlug(value: string) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

export function UpdateOrganizationDialog() {
  const queryClient = useQueryClient();
  const { open, setOpen, currentOrganization, setCurrentOrganization } = useOrganizations();
  const slugManuallyEditedRef = useRef(false);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", slug: "" },
  });

  useEffect(() => {
    if (open === "edit" && currentOrganization) {
      form.reset({
        name: currentOrganization.name,
        slug: currentOrganization.slug ?? "",
      });
      slugManuallyEditedRef.current = Boolean(currentOrganization.slug);
    }
  }, [open, currentOrganization, form]);

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: async (values: FormValues) => {
      if (!currentOrganization) return;
      await organizationsApi.updateOrganization(currentOrganization.id, values);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "organizations"] });
      toast.success("Organization updated.");
      handleClose(false);
    },
  });

  const handleClose = (nextOpen: boolean) => {
    if (!nextOpen) {
      setOpen(null);
      setCurrentOrganization(null);
      form.reset();
      slugManuallyEditedRef.current = false;
    } else {
      setOpen("edit");
    }
  };

  return (
    <Dialog open={open === "edit"} onOpenChange={handleClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Update organization</DialogTitle>
          <DialogDescription>Modify the organization name or slug.</DialogDescription>
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
                      onChange={(event) => {
                        field.onChange(event);
                        if (!slugManuallyEditedRef.current) {
                          form.setValue("slug", toSlug(event.target.value), {
                            shouldValidate: true,
                          });
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
                      onChange={(event) => {
                        slugManuallyEditedRef.current = true;
                        field.onChange(event);
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
              fallback="Failed to update organization. Please try again."
            />

            <div className="flex justify-end gap-2">
              <PrimaryButton type="submit" isPending={isPending} pendingLabel="Saving...">
                Save changes
              </PrimaryButton>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
