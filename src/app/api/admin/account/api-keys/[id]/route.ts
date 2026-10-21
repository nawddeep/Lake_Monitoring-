import { z } from "zod";
import {
  disableApiKeyForUser,
  updateApiKeyNameForUser,
} from "@/repositories/admin/apiKeyRepository";
import { serializeApiKey } from "@/serializers/apiKeySerializer";
import { withAdmin } from "@/app/api/admin/with-admin";
import { detailResponse, noContentResponse, notFoundResponse } from "@/app/api/response";

const updateApiKeySchema = z.object({
  name: z.string().trim().min(1, "Name is required"),
});

export const PATCH = withAdmin(async (request, { params }, { user }) => {
  const { id } = await params;
  const { name } = updateApiKeySchema.parse(await request.json());

  const updated = await updateApiKeyNameForUser(id, user.id, name);
  if (!updated) return notFoundResponse("API key not found.");

  return detailResponse(serializeApiKey(updated));
});

export const DELETE = withAdmin(async (_request, { params }, { user }) => {
  const { id } = await params;

  const disabled = await disableApiKeyForUser(id, user.id);
  if (!disabled) return notFoundResponse("API key not found.");

  return noContentResponse();
});
