import { z } from "zod";
import { parseCommaSeparatedList } from "@/lib/api";
import { listSchema } from "@/app/api/schemas";

export const listApiKeysSchema = listSchema.extend({
  search: z.string().optional(),
  enabled: z
    .string()
    .transform(parseCommaSeparatedList)
    .pipe(z.array(z.enum(["true", "false"])))
    .optional(),
  sort: z.enum(["name", "createdAt", "expiresAt"]).optional(),
});

export const createApiKeySchema = z.object({
  name: z.string().min(1, "Name is required"),
});

export type CreateApiKeyBody = z.infer<typeof createApiKeySchema>;
