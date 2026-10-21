"use client";

import { ChangeMemberRoleDialog } from "./change-member-role-dialog";
import { columns } from "./columns";
import { MemberDetailsSheet } from "./member-details-sheet";
import { MembersProvider } from "./members-provider";
import { RemoveMembershipDialog } from "./remove-membership-dialog";
import { membersApi } from "@/services/api/customer/membersApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";

const roleOptions = [
  { label: "Member", value: "member" },
  { label: "Owner", value: "owner" },
  { label: "Admin", value: "admin" },
];

function ConnectedMembersTable() {
  const { table } = useConnectedTable({
    queryKey: ["customer", "members"],
    queryFn: (params) => membersApi.list(params),
    columns,
  });

  return (
    <DataTable
      table={table}
      showSearch
      searchPlaceholder="Search by name or email..."
      filters={[{ columnId: "role", title: "Role", options: roleOptions }]}
    />
  );
}

export function MembersTable({ currentUserId }: { currentUserId: string }) {
  return (
    <MembersProvider currentUserId={currentUserId}>
      <ConnectedMembersTable />
      <MemberDetailsSheet />
      <ChangeMemberRoleDialog />
      <RemoveMembershipDialog />
    </MembersProvider>
  );
}
