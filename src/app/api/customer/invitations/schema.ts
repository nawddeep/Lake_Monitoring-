import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const createInvitationSchema = z.object({
  email: z.string().trim().email("Enter a valid email address."),
  role: z.enum(["owner", "admin", "member"]),
});

export const listInvitationsSchema = listSchema.extend({
  sort: z.enum(["createdAt", "expiresAt"]).optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
});

export type CreateInvitationBody = z.infer<typeof createInvitationSchema>;
export type ListInvitationsParams = z.infer<typeof listInvitationsSchema>;
