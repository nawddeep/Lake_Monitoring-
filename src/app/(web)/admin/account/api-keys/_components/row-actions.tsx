"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Pencil, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { z } from "zod";
import { accountApiKeysApi } from "@/services/api/admin/account/apiKeysApi";
import { CancelButton } from "@/components/buttons/cancel-button";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";
import { MutationError } from "@/components/feedback/mutation-error";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const editSchema = z.object({ name: z.string().trim().min(1, "Name is required") });
type EditFormValues = z.infer<typeof editSchema>;

const QUERY_KEY = ["admin", "account", "api-keys"];

export function ApiKeyRowActions({ id, name }: { id: string; name: string | null }) {
  const [dialog, setDialog] = useState<"edit" | "delete" | null>(null);
  const queryClient = useQueryClient();

  const form = useForm<EditFormValues>({
    resolver: zodResolver(editSchema),
    values: { name: name ?? "" },
  });

  const editMutation = useMutation({
    mutationFn: (values: EditFormValues) => accountApiKeysApi.updateApiKey(id, values),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
      toast.success("API key updated.");
      setDialog(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => accountApiKeysApi.deleteApiKey(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
      toast.success("API key revoked.");
      setDialog(null);
    },
  });

  return (
    <>
      <RowActionsDropdown>
        <DropdownMenuItem onClick={() => setDialog("edit")}>
          Edit name
          <Pencil size={16} className="ml-auto" />
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => setDialog("delete")}
        >
          Revoke
          <Trash2 size={16} className="ml-auto" />
        </DropdownMenuItem>
      </RowActionsDropdown>

      <Dialog open={dialog === "edit"} onOpenChange={(val) => !val && setDialog(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit API key name</DialogTitle>
            <DialogDescription>Update the name for this API key.</DialogDescription>
          </DialogHeader>
          <Form {...form}>
            <form
              className="space-y-4"
              onSubmit={form.handleSubmit((values) => editMutation.mutate(values))}
            >
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <MutationError
                isError={editMutation.isError}
                error={editMutation.error}
                fallback="Failed to update. Please try again."
              />

              <div className="flex justify-end gap-2">
                <CancelButton onClick={() => setDialog(null)} disabled={editMutation.isPending} />
                <PrimaryButton
                  type="submit"
                  isPending={editMutation.isPending}
                  pendingLabel="Saving..."
                >
                  Save
                </PrimaryButton>
              </div>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      <DeleteDialog
        open={dialog === "delete"}
        onOpenChange={(val) => !val && setDialog(null)}
        title="Revoke API key"
        description="This API key will immediately be disabled. API requests made using this key will be rejected, which could cause any systems still depending on it to break. Once revoked, you'll no longer be able to view or modify this API key."
        onDelete={() => deleteMutation.mutate()}
        isPending={deleteMutation.isPending}
        confirmLabel="Revoke"
        confirmPendingLabel="Revoking..."
      />
    </>
  );
}
