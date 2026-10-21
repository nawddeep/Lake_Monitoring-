import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const createCustomerPortalInvitationSchema = z.object({
  email: z.string().trim().email("Enter a valid email"),
  role: z.enum(["owner", "admin", "member"]),
});

export const listCustomerInvitationsSchema = listSchema.extend({
  sort: z.enum(["createdAt", "expiresAt"]).optional(),
  status: z.string().transform(parseCommaSeparatedList).optional(),
  organizationIds: z.string().transform(parseCommaSeparatedList).optional(),
});

export type CreateCustomerPortalInvitationBody = z.infer<
  typeof createCustomerPortalInvitationSchema
>;
export type ListCustomerInvitationsParams = z.infer<typeof listCustomerInvitationsSchema>;
export type ListOrganizationInvitationsParams = ListCustomerInvitationsParams;
