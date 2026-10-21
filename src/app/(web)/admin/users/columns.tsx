"use client";

import { UserRowActions } from "./_components/user-row-actions";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/components/data-table/column-header";
import { Badge } from "@/components/ui/badge";
import type { UserAccess, UserWithAccess } from "@/types/user";

function AccessBadges({ access }: { access: UserAccess }) {
  if (access === "both") {
    return (
      <div className="flex gap-1">
        <Badge variant="secondary">Admin</Badge>
        <Badge variant="secondary">Customer</Badge>
      </div>
    );
  }

  if (access === "admin_only") return <Badge variant="secondary">Admin</Badge>;
  if (access === "customer_only") return <Badge variant="secondary">Customer</Badge>;
  return <Badge variant="outline">None</Badge>;
}

export const columns: ColumnDef<UserWithAccess>[] = [
  {
    id: "name",
    accessorFn: (user) => [user.firstName, user.lastName].filter(Boolean).join(" ") || user.name,
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
    cell: ({ row }) => (
      <span className="font-medium">
        {[row.original.firstName, row.original.lastName].filter(Boolean).join(" ") ||
          row.original.name}
      </span>
    ),
  },
  {
    accessorKey: "email",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email" />,
  },
  {
    accessorKey: "emailVerified",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email Verified" />,
    cell: ({ row }) => (
      <Badge variant={row.original.emailVerified ? "secondary" : "outline"}>
        {row.original.emailVerified ? "Yes" : "No"}
      </Badge>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "access",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Portal Access" />,
    cell: ({ row }) => <AccessBadges access={row.original.access} />,
    enableSorting: false,
  },
  {
    id: "status",
    accessorFn: (user) => user.banned,
    header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
    cell: ({ row }) =>
      row.original.banned ? (
        <Badge variant="destructive">Banned</Badge>
      ) : (
        <Badge variant="secondary">Active</Badge>
      ),
    enableSorting: false,
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
    cell: ({ row }) => <UserRowActions row={row} />,
  },
];
