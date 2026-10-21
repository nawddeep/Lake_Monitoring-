"use client";

import { columns } from "./columns";
import { invitationsApi } from "@/services/api/admin/invitationsApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";
import type { ListAdminPortalInvitationsParams } from "@/app/api/admin/team/invitations/schema";

function InvitationsTable() {
  const { table } = useConnectedTable({
    queryKey: ["admin", "team", "invitations"],
    queryFn: ({ sort, order, page, perPage, filters }) =>
      invitationsApi.listAdminPortalInvitations({
        sort: sort as ListAdminPortalInvitationsParams["sort"],
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

export default function InvitationsPage() {
  return <InvitationsTable />;
}
