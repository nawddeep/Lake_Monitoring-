import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import type {
  ColumnDef,
  ColumnFiltersState,
  PaginationState,
  SortingState,
} from "@tanstack/react-table";
import {
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { ListParams } from "@/services/api/listParams";
import type { PaginationData } from "@/app/api/response";

export type { ListParams };

interface UseConnectedTableOptions<TData> {
  queryKey: unknown[];
  queryFn: (params: ListParams) => Promise<{ data: TData[]; pagination: PaginationData }>;
  columns: ColumnDef<TData>[];
  pageSize?: number;
  initialFilters?: ColumnFiltersState;
}

function toListParams(
  sorting: SortingState,
  pagination: PaginationState,
  columnFilters: ColumnFiltersState,
  globalFilter: string,
): ListParams {
  const sort = sorting[0];
  const filters = columnFilters.length
    ? Object.fromEntries(columnFilters.map((f) => [f.id, f.value as string[]]))
    : undefined;
  return {
    search: globalFilter || undefined,
    sort: sort?.id,
    order: sort ? (sort.desc ? "desc" : "asc") : undefined,
    page: pagination.pageIndex + 1,
    perPage: pagination.pageSize,
    filters,
  };
}

export function useConnectedTable<TData>({
  queryKey,
  queryFn,
  columns,
  pageSize = 10,
  initialFilters = [],
}: UseConnectedTableOptions<TData>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [pagination, setPagination] = React.useState<PaginationState>({ pageIndex: 0, pageSize });
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(initialFilters);
  const [globalFilter, setGlobalFilter] = React.useState<string>("");

  const params = toListParams(sorting, pagination, columnFilters, globalFilter);

  const queryResult = useQuery({
    queryKey: [...queryKey, params],
    queryFn: () => queryFn(params),
  });

  const isPending = queryResult.isPending;

  const table = useReactTable({
    data: queryResult.data?.data ?? [],
    columns,
    state: { sorting, pagination, columnFilters, globalFilter },
    onSortingChange: (updater) => {
      setSorting(updater);
      setPagination((p) => ({ ...p, pageIndex: 0 }));
    },
    onPaginationChange: setPagination,
    onColumnFiltersChange: (updater) => {
      setColumnFilters(updater);
      setPagination((p) => ({ ...p, pageIndex: 0 }));
    },
    onGlobalFilterChange: (updater) => {
      setGlobalFilter(updater);
      setPagination((p) => ({ ...p, pageIndex: 0 }));
    },
    manualSorting: true,
    manualPagination: true,
    manualFiltering: true,
    rowCount: queryResult.data?.pagination.total_results ?? 0,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return { table: { instance: table, isPending } };
}
