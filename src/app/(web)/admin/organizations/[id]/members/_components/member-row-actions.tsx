"use client";

import { useOrganizationMembers } from "./organization-members-provider";
import type { Row } from "@tanstack/react-table";
import { ShieldCheck, UserMinus, UserSearch } from "lucide-react";
import { RowActionsDropdown } from "@/components/data-table/row-actions-dropdown";
import { DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { Member } from "@/types/member";

export function MemberRowActions({ row }: { row: Row<Member> }) {
  const { setOpen, setCurrentMember, currentUserId } = useOrganizationMembers();
  const { can } = useAdminPermissions();
  const member = row.original;
  const isCurrentUser = member.user.id === currentUserId;
  const canChangeRole = !isCurrentUser && can({ member: "update" });
  const canRemoveMembership = !isCurrentUser && can({ member: "delete" });

  const openDialog = (dialog: "view" | "change-role" | "remove") => {
    setCurrentMember(member);
    setOpen(dialog);
  };

  return (
    <RowActionsDropdown>
      <DropdownMenuItem onClick={() => openDialog("view")}>
        View details
        <UserSearch size={16} className="ml-auto" />
      </DropdownMenuItem>
      {(canChangeRole || canRemoveMembership) && <DropdownMenuSeparator />}
      {canChangeRole && (
        <DropdownMenuItem onClick={() => openDialog("change-role")}>
          Change role
          <ShieldCheck size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
      {canChangeRole && canRemoveMembership && <DropdownMenuSeparator />}
      {canRemoveMembership && (
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => openDialog("remove")}
        >
          Remove membership
          <UserMinus size={16} className="ml-auto" />
        </DropdownMenuItem>
      )}
    </RowActionsDropdown>
  );
}
