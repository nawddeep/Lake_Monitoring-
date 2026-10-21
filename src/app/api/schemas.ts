import { z } from "zod";

export const listSchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  perPage: z.coerce.number().int().positive().optional().default(10),
  order: z.enum(["asc", "desc"]).optional(),
});
