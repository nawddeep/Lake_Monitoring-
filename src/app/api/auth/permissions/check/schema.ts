import { z } from "zod";

export const checkPermissionsSchema = z.object({
  permissions: z.record(z.string(), z.array(z.string())),
});

export type CheckPermissionsBody = z.infer<typeof checkPermissionsSchema>;
