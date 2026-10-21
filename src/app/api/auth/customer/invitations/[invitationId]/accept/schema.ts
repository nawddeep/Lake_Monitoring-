import { z } from "zod";

export const acceptCustomerInvitationSchema = z.object({
  firstName: z.string().trim().min(1, "First name is required"),
  lastName: z.string().trim().min(1, "Last name is required"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(72, "Password must be 72 characters or fewer"),
});

export type AcceptCustomerInvitationBody = z.infer<typeof acceptCustomerInvitationSchema>;
