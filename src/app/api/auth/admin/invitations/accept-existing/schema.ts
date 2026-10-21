import { z } from "zod";

export const acceptExistingAdminInvitationSchema = z.object({
  invitationId: z.string().min(1, "Invitation is required"),
});

export type AcceptExistingAdminInvitationBody = z.infer<typeof acceptExistingAdminInvitationSchema>;
