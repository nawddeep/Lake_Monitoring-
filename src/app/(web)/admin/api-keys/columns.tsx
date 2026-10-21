"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/components/data-table/column-header";
import { DeleteApiKeyButton } from "@/app/(web)/admin/api-keys/_components/delete-api-key-button";
import type { ApiKey } from "@/types/apiKey";

export const columns: ColumnDef<ApiKey>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
    cell: ({ row }) => row.original.name ?? <span className="text-muted-foreground">—</span>,
  },
  {
    accessorKey: "start",
    header: "Key",
    enableSorting: false,
    cell: ({ row }) => {
      const { prefix, start } = row.original;
      const display = [prefix, start].filter(Boolean).join("") + "••••••••";
      return <span className="font-mono text-sm text-muted-foreground">{display}</span>;
    },
  },
  {
    accessorKey: "user",
    header: "Owner",
    enableSorting: false,
    cell: ({ row }) => row.original.user?.name ?? <span className="text-muted-foreground">—</span>,
  },
  {
    accessorKey: "enabled",
    header: "Status",
    enableSorting: false,
    cell: ({ row }) =>
      row.original.enabled === false ? (
        <span className="text-destructive text-sm">Disabled</span>
      ) : (
        <span className="text-sm text-muted-foreground">Active</span>
      ),
  },
  {
    accessorKey: "lastRequest",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Last Request" />,
    cell: ({ row }) =>
      row.original.lastRequest ? (
        <span className="text-muted-foreground">
          {new Date(row.original.lastRequest).toLocaleDateString()}
        </span>
      ) : (
        <span className="text-muted-foreground">Never</span>
      ),
  },
  {
    accessorKey: "expiresAt",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Expires" />,
    cell: ({ row }) =>
      row.original.expiresAt ? (
        new Date(row.original.expiresAt).toLocaleDateString()
      ) : (
        <span className="text-muted-foreground">Never</span>
      ),
  },
  {
    accessorKey: "createdAt",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Created" />,
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {new Date(row.original.createdAt).toLocaleDateString()}
      </span>
    ),
  },
  {
    id: "actions",
    enableSorting: false,
    cell: ({ row }) => <DeleteApiKeyButton id={row.original.id} />,
  },
];
