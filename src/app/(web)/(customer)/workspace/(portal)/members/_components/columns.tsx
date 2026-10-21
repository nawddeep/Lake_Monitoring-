"use client";

import { MemberRowActions } from "./member-row-actions";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/components/data-table/column-header";
import type { Member } from "@/types/member";

export const columns: ColumnDef<Member>[] = [
  {
    id: "name",
    accessorFn: (member) =>
      [member.user.firstName, member.user.lastName].filter(Boolean).join(" ") || member.user.name,
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
    cell: ({ row }) => {
      const { firstName, lastName, name } = row.original.user;
      return (
        <span className="font-medium">
          {[firstName, lastName].filter(Boolean).join(" ") || name}
        </span>
      );
    },
  },
  {
    id: "email",
    accessorFn: (member) => member.user.email,
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email" />,
    cell: ({ row }) => <span className="text-muted-foreground">{row.original.user.email}</span>,
  },
  {
    accessorKey: "role",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Role" />,
    cell: ({ row }) => (
      <span className="capitalize text-muted-foreground">{row.original.role}</span>
    ),
  },
  {
    accessorKey: "createdAt",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Joined" />,
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {new Date(row.original.createdAt).toLocaleDateString()}
      </span>
    ),
  },
  {
    id: "actions",
    enableSorting: false,
    cell: ({ row }) => <MemberRowActions row={row} />,
  },
];
