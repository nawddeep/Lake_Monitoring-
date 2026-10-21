import { adminApiClient } from "@/services/api/client";
import type { ListParams } from "@/services/api/listParams";
import type { PaginationData } from "@/app/api/response";
import type { ApiKey } from "@/types/apiKey";

export const apiKeysApi = {
  listApiKeys(params?: ListParams): Promise<{ data: ApiKey[]; pagination: PaginationData }> {
    return adminApiClient.getPaginated<ApiKey>("/api-keys", params);
  },

  deleteApiKey(id: string): Promise<void> {
    return adminApiClient.delete(`/api-keys/${id}`);
  },
};
