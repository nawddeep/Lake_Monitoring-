"use client";

import { apiKeysApi } from "@/services/api/admin/apiKeysApi";
import { DataTable } from "@/components/data-table/data-table";
import { useConnectedTable } from "@/hooks/use-connected-table";
import { columns } from "@/app/(web)/admin/api-keys/columns";

export const API_KEYS_QUERY_KEY: string[] = ["admin", "api-keys"];

export function ApiKeysTable() {
  const { table } = useConnectedTable({
    queryKey: API_KEYS_QUERY_KEY,
    queryFn: (params) => apiKeysApi.listApiKeys(params),
    columns,
    initialFilters: [{ id: "enabled", value: ["true"] }],
  });

  return (
    <DataTable
      table={table}

      showSearch
      searchPlaceholder="Search by name or key..."
      filters={[
        {
          columnId: "enabled",
          title: "Status",
          options: [
            { label: "Active", value: "true" },
            { label: "Disabled", value: "false" },
          ],
        },
      ]}
    />
  );
}
