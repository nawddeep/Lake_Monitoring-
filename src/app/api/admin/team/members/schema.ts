import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const listTeamMembersSchema = listSchema.extend({
  sort: z.enum(["createdAt", "role"]).optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
});

export type ListTeamMembersParams = z.infer<typeof listTeamMembersSchema>;
