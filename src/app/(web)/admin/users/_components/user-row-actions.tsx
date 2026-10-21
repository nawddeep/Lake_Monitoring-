"use client";

import { useUsers } from "./users-provider";
import type { Row } from "@tanstack/react-table";
import { Ban, RotateCcw, Trash2, UserRoundCog, UserSearch } from "lucide-react";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { UserWithAccess } from "@/types/user";

export function UserRowActions({ row }: { row: Row<UserWithAccess> }) {
  const { setOpen, setCurrentUser, currentUserId } = useUsers();
  const { can } = useAdminPermissions();
  const user = row.original;
  const isCurrentUser = user.id === currentUserId;
  const isAdmin = user.role === "admin";
  const canImpersonate = !isCurrentUser && !isAdmin && !user.banned && can({ user: "impersonate" });
  const canBan = !isCurrentUser && can({ user: "ban" });
  const canDelete = !isCurrentUser && can({ user: "delete" });

  const openDialog = (dialog: "view" | "impersonate" | "ban" | "unban" | "delete") => {
    setCurrentUser(user);
    setOpen(dialog);
  };

  return (
    <RowActionsDropdown>
      <DropdownMenuItem onClick={() => openDialog("view")}>
        View details
        <UserSearch size={16} className="ml-auto" />
      </DropdownMenuItem>
      {canImpersonate && (
        <DropdownMenuItem onClick={() => openDialog("impersonate")}>
          Impersonate user
          <UserRoundCog size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
      {(canBan || canDelete) && <DropdownMenuSeparator />}
      {canBan &&
        (user.banned ? (
          <DropdownMenuItem onClick={() => openDialog("unban")}>
            Unban user
            <RotateCcw size={16} className="ml-auto" />
          </DropdownMenuItem>
        ) : (
          <DropdownMenuItem
            className="text-destructive focus:text-destructive"
            onClick={() => openDialog("ban")}
          >
            Ban user
            <Ban size={16} className="ml-auto" />
          </DropdownMenuItem>
        ))}
      {canBan && canDelete && <DropdownMenuSeparator />}
      {canDelete && (
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => openDialog("delete")}
        >
          Delete user
          <Trash2 size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
    </RowActionsDropdown>
  );
}
