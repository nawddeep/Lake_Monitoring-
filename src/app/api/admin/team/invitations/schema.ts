import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const listAdminPortalInvitationsSchema = listSchema.extend({
  sort: z.enum(["email", "role", "status", "createdAt", "expiresAt"]).optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
});

export const createAdminPortalInvitationSchema = z.object({
  email: z.string().trim().toLowerCase().email("Enter a valid email"),
  role: z.enum(["admin", "user"]),
});

export type ListAdminPortalInvitationsParams = z.infer<typeof listAdminPortalInvitationsSchema>;
export type CreateAdminPortalInvitationBody = z.infer<typeof createAdminPortalInvitationSchema>;
