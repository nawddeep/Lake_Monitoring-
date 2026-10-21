"use client";

import { columns } from "./columns";
import { invitationsApi } from "@/services/api/customer/invitationsApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";
import type { ListInvitationsParams } from "@/app/api/customer/invitations/schema";

export function InvitationsTable() {
  const { table } = useConnectedTable({
    queryKey: ["customer", "invitations"],
    queryFn: ({ sort, order, page, perPage, filters }) =>
      invitationsApi.list({
        sort: sort as ListInvitationsParams["sort"],
        order,
        page,
        perPage,
        status: (filters?.status as string[] | undefined) ?? undefined,
      }),
    columns,
    initialFilters: [{ id: "status", value: ["pending"] }],
  });

  return (
    <DataTable
      table={table}
      filters={[
        {
          columnId: "status",
          title: "Status",
          options: [
            { label: "Pending", value: "pending" },
            { label: "Accepted", value: "accepted" },
            { label: "Rejected", value: "rejected" },
            { label: "Canceled", value: "canceled" },
          ],
        },
      ]}
    />
  );
}
