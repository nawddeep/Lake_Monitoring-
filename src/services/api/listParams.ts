export interface ListParams {
  search?: string;
  filters?: Record<string, unknown>;
  sort?: string;
  order?: "asc" | "desc";
  page: number;
  perPage: number;
}
