import { z } from "zod";

export const setActiveOrganizationSchema = z.object({
  organizationId: z.string().min(1, "Organization is required."),
});

export type SetActiveOrganizationBody = z.infer<typeof setActiveOrganizationSchema>;
