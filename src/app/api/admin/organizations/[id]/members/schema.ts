import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const listMembersSchema = listSchema.extend({
  search: z.string().optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
  role: z.string().transform(parseCommaSeparatedList).optional(),
  sort: z.enum(["createdAt", "firstName", "lastName", "email", "role", "name"]).optional(),
});

export type ListOrganizationMembersParams = z.infer<typeof listMembersSchema>;
