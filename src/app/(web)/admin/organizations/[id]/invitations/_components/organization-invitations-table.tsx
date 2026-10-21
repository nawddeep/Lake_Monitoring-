"use client";

import { invitationColumns } from "./invitations-columns";
import { organizationsApi } from "@/services/api/admin/organizationsApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";
import type { ListOrganizationInvitationsParams } from "@/app/api/admin/organizations/[id]/invitations/schema";

export function OrganizationInvitationsTable({ organizationId }: { organizationId: string }) {
  const { table } = useConnectedTable({
    queryKey: ["admin", "organizations", organizationId, "invitations"],
    queryFn: ({ sort, order, page, perPage, filters }) =>
      organizationsApi.listOrganizationInvitations(organizationId, {
        sort: sort as ListOrganizationInvitationsParams["sort"],
        order,
        page,
        perPage,
        status: (filters?.status as string[] | undefined) ?? undefined,
      }),
    columns: invitationColumns(organizationId),
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
            { label: "Canceled", value: "canceled" },
            { label: "Rejected", value: "rejected" },
          ],
        },
      ]}
    />
  );
}
