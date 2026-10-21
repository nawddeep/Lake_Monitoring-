export function combineFilters<TWhere extends object>(
  ...filters: Array<TWhere | undefined | null | false>
): TWhere {
  const active = filters.filter(Boolean) as TWhere[];
  if (active.length === 0) {
    return {} as TWhere;
  }
  if (active.length === 1) {
    return active[0];
  }
  return { AND: active } as TWhere;
}
