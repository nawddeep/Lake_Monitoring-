import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const listUsersSchema = listSchema.extend({
  search: z.string().trim().optional(),
  sort: z.enum(["name", "email", "createdAt"]).optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
  access: z.string().transform(parseCommaSeparatedList).optional(),
});

export type ListUsersParams = z.infer<typeof listUsersSchema>;
