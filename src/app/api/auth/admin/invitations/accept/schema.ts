import { z } from "zod";

export const acceptAdminInvitationSchema = z.object({
  invitationId: z.string().min(1, "Invitation is required"),
  firstName: z.string().trim().min(1, "First name is required"),
  lastName: z.string().trim().min(1, "Last name is required"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(72, "Password must be 72 characters or fewer"),
});

export type AcceptAdminInvitationBody = z.infer<typeof acceptAdminInvitationSchema>;
