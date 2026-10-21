"use client";

import { useOrganizations } from "./organizations-provider";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { organizationsApi } from "@/services/api/admin/organizationsApi";
import { DeleteDialog } from "@/components/dialogs/delete-dialog";

export function DeleteOrganizationDialog() {
  const { open, setOpen, currentOrganization, setCurrentOrganization } = useOrganizations();
  const queryClient = useQueryClient();

  const { mutateAsync, isPending } = useMutation({
    mutationFn: async () => {
      if (!currentOrganization) return;
      await organizationsApi.deleteOrganization(currentOrganization.id);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["admin", "organizations"] });
      toast.success("Organization deleted.");
      setCurrentOrganization(null);
      setOpen(null);
    },
  });

  if (!currentOrganization) return null;

  return (
    <DeleteDialog
      open={open === "delete"}
      onOpenChange={(nextOpen) => {
        if (!nextOpen) {
          setOpen(null);
          setCurrentOrganization(null);
        }
      }}
      title="Delete organization"
      description={`This will permanently delete ${currentOrganization.name}. This action cannot be undone.`}
      onDelete={() => mutateAsync()}
      isPending={isPending}
      confirmLabel="Delete"
      confirmPendingLabel="Deleting..."
    />
  );
}
