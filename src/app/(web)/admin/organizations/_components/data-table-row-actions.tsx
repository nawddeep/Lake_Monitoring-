"use client";

import { useRouter } from "next/navigation";
import { useOrganizations } from "./organizations-provider";
import type { Row } from "@tanstack/react-table";
import { Eye, Pencil, Trash2 } from "lucide-react";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { Organization } from "@/types/organization";

type DataTableRowActionsProps = {
  row: Row<Organization>;
};

export function DataTableRowActions({ row }: DataTableRowActionsProps) {
  const { setOpen, setCurrentOrganization } = useOrganizations();
  const { can } = useAdminPermissions();
  const router = useRouter();
  const canUpdate = can({ organization: "update" });
  const canDelete = can({ organization: "delete" });

  return (
    <RowActionsDropdown>
      <DropdownMenuItem
        onClick={() => {
          router.push(`/admin/organizations/${row.original.id}`);
        }}
      >
        View
        <Eye size={16} className="ml-auto" />
      </DropdownMenuItem>
      {(canUpdate || canDelete) && <DropdownMenuSeparator />}
      {canUpdate && (
        <DropdownMenuItem
          onClick={() => {
            setCurrentOrganization(row.original);
            setOpen("edit");
          }}
        >
          Edit
          <Pencil size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
      {canUpdate && canDelete && <DropdownMenuSeparator />}
      {canDelete && (
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => {
            setCurrentOrganization(row.original);
            setOpen("delete");
          }}
        >
          Delete
          <Trash2 size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
    </RowActionsDropdown>
  );
}
