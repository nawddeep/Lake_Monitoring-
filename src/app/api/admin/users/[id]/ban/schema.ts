import { z } from "zod";

export const banUserSchema = z.object({
  banReason: z.string().trim().max(255, "Reason must be 255 characters or fewer").optional(),
});

export type BanUserBody = z.infer<typeof banUserSchema>;
