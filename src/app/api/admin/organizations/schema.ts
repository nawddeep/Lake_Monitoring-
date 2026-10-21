import { z } from "zod";
import { listSchema } from "@/app/api/schemas";

export const listOrganizationsSchema = listSchema.extend({
  search: z.string().optional(),
  sort: z.enum(["name", "slug", "createdAt"]).optional(),
});

const organizationPayloadSchema = z.object({
  name: z.string().trim().min(1, "Name is required").max(100),
  slug: z
    .string()
    .trim()
    .min(1, "Slug is required")
    .max(100)
    .regex(
      /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
      "Slug must be lowercase letters, numbers, and hyphens only",
    ),
});

export const createOrganizationSchema = organizationPayloadSchema;
export const updateOrganizationSchema = organizationPayloadSchema;

export type CreateOrganizationBody = z.infer<typeof createOrganizationSchema>;
export type UpdateOrganizationBody = z.infer<typeof updateOrganizationSchema>;
