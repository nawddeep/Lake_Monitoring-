export type SortOrder = "asc" | "desc";

export type BaseListOptions<SortOption extends string> = {
  page: number;
  perPage: number;
  order?: SortOrder;
  sort?: SortOption;
};
