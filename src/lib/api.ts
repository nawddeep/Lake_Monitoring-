import type { z } from "zod";

export function validateQuery<T>(request: Request, schema: z.ZodType<T>): T {
  const { searchParams } = new URL(request.url);
  return schema.parse(Object.fromEntries(searchParams));
}

export function parseCommaSeparatedList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
