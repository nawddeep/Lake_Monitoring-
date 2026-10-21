"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/components/data-table/column-header";
import { DataTableRowActions } from "@/app/(web)/admin/organizations/_components/data-table-row-actions";
import type { Organization } from "@/types/organization";

export const columns: ColumnDef<Organization>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
  },
  {
    accessorKey: "slug",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Slug" />,
    cell: ({ row }) => <span className="text-muted-foreground">{row.original.slug ?? "—"}</span>,
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
    header: () => null,
    cell: (context) => <DataTableRowActions row={context.row} />,
    enableSorting: false,
    enableHiding: false,
    meta: {
      className: "w-[72px] text-right",
      tdClassName: "text-right",
    },
  },
];
