import { disableApiKeyById, findApiKeyById } from "@/repositories/admin/apiKeyRepository";
import { withAdmin } from "@/app/api/admin/with-admin";
import { noContentResponse, notFoundResponse } from "@/app/api/response";

export const DELETE = withAdmin(
  async (_request, { params }) => {
    const { id } = await params;
    const apiKey = await findApiKeyById(id);

    if (!apiKey) {
      return notFoundResponse("API key not found.");
    }

    await disableApiKeyById(apiKey.id);
    return noContentResponse();
  },
  { apiKey: ["delete:any"] },
);
