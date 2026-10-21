"use client";

import { useMembers } from "./members-provider";
import type { Row } from "@tanstack/react-table";
import { ShieldCheck, UserMinus, UserSearch } from "lucide-react";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { User } from "@/types/user";

type DataTableRowActionsProps = {
  row: Row<User>;
};

export function DataTableRowActions({ row }: DataTableRowActionsProps) {
  const { setOpen, setCurrentRow, currentUserId } = useMembers();
  const { can } = useAdminPermissions();
  const isCurrentUser = row.original.id === currentUserId;
  const canChangeRole = can({ user: "set-role" });
  const canRevokeAccess = !isCurrentUser && canChangeRole;

  return (
    <RowActionsDropdown>
      <DropdownMenuItem
        onClick={() => {
          setCurrentRow(row.original);
          setOpen("view");
        }}
      >
        View details
        <UserSearch size={16} className="ml-auto" />
      </DropdownMenuItem>
      {(canChangeRole || canRevokeAccess) && <DropdownMenuSeparator />}
      {canChangeRole && (
        <DropdownMenuItem
          onClick={() => {
            setCurrentRow(row.original);
            setOpen("change-role");
          }}
        >
          Change role
          <ShieldCheck size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
      {canChangeRole && canRevokeAccess && <DropdownMenuSeparator />}
      {canRevokeAccess && (
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => {
            setCurrentRow(row.original);
            setOpen("revoke-access");
          }}
        >
          Revoke access
          <UserMinus size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
    </RowActionsDropdown>
  );
}
