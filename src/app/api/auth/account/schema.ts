import { z } from "zod";

export const updateAccountSchema = z.object({
  firstName: z.string().trim().min(1, "First name is required.").max(60),
  lastName: z.string().trim().min(1, "Last name is required.").max(60),
});

export type UpdateAccountBody = z.infer<typeof updateAccountSchema>;
