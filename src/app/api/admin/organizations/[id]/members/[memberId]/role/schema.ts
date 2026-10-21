import { z } from "zod";

export const updateMemberRoleSchema = z.object({
  role: z.enum(["owner", "admin", "member"]),
});

export type UpdateMemberRoleBody = z.infer<typeof updateMemberRoleSchema>;
