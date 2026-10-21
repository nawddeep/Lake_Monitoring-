"use client";

import { InvitationRowActions } from "./row-actions";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/components/data-table/column-header";
import { Badge } from "@/components/ui/badge";
import type { Invitation } from "@/types/invitation";

const statusVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  pending: "default",
  accepted: "secondary",
  canceled: "destructive",
  rejected: "outline",
};

export const columns: ColumnDef<Invitation>[] = [
  {
    accessorKey: "email",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email" />,
    enableSorting: false,
  },
  {
    accessorKey: "role",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Role" />,
    cell: ({ row }) => (
      <span className="capitalize text-muted-foreground">{row.original.role}</span>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "status",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
    cell: ({ row }) => (
      <Badge variant={statusVariant[row.original.status] ?? "outline"} className="capitalize">
        {row.original.status}
      </Badge>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "emailStatus",
    header: "Email delivery",
    enableSorting: false,
    cell: ({ row }) => (
      <Badge variant={row.original.emailStatus === "failed" ? "destructive" : "outline"}>
        {row.original.emailStatus === "sent"
          ? "Sent"
          : row.original.emailStatus === "failed"
            ? "Failed"
            : row.original.emailStatus === "not_sent"
              ? "Not sent"
              : "Unknown"}
      </Badge>
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
    accessorKey: "expiresAt",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Expires" />,
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {new Date(row.original.expiresAt).toLocaleDateString()}
      </span>
    ),
  },
  {
    id: "actions",
    enableSorting: false,
    cell: ({ row }) => <InvitationRowActions row={row} />,
  },
];
