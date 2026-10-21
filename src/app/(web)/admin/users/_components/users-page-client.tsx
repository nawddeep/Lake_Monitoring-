"use client";

import { columns } from "../columns";
import { BanUserDialog } from "./ban-user-dialog";
import { DeleteUserDialog } from "./delete-user-dialog";
import { ImpersonateUserDialog } from "./impersonate-user-dialog";
import { UnbanUserDialog } from "./unban-user-dialog";
import { UserDetailsSheet } from "./user-details-sheet";
import { UsersProvider } from "./users-provider";
import { usersApi } from "@/services/api/admin/usersApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";
import type { ListUsersParams } from "@/app/api/admin/users/schema";

function UsersTable() {
  const { table } = useConnectedTable({
    queryKey: ["admin", "users"],
    queryFn: ({ sort, order, page, perPage, search, filters }) =>
      usersApi.listUsers({
        sort: sort as ListUsersParams["sort"],
        order,
        page,
        perPage,
        search,
        filters: filters as Record<string, string[]> | undefined,
      }),
    columns,
  });

  return (
    <DataTable
      table={table}
      showSearch
      searchPlaceholder="Search by name or email..."
      filters={[
        {
          columnId: "access",
          title: "Access",
          options: [
            { label: "Customer Portal", value: "customer" },
            { label: "Admin Portal", value: "admin" },
          ],
        },
        {
          columnId: "status",
          title: "Status",
          options: [
            { label: "Active", value: "active" },
            { label: "Banned", value: "banned" },
          ],
        },
      ]}
    />
  );
}

export function UsersPageClient({ currentUserId }: { currentUserId: string }) {
  return (
    <UsersProvider currentUserId={currentUserId}>
      <UsersTable />
      <UserDetailsSheet />
      <ImpersonateUserDialog />
      <BanUserDialog />
      <UnbanUserDialog />
      <DeleteUserDialog />
    </UsersProvider>
  );
}
