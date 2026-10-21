import { requirePermission } from "@/lib/adminAuthorization";
import { CreateApiKeyButton } from "@/components/admin/create-api-key-button";
import { ContentLayout } from "@/components/platform/content-layout";
import {
  API_KEYS_QUERY_KEY,
  ApiKeysTable,
} from "@/app/(web)/admin/api-keys/_components/api-keys-table";

export default async function ApiKeysPage() {
  await requirePermission({ apiKey: ["read:any"] });

  return (
    <ContentLayout
      title="API Keys"
      description="Manage API keys for programmatic access."
      actions={<CreateApiKeyButton queryKey={API_KEYS_QUERY_KEY} />}
    >
      <ApiKeysTable />
    </ContentLayout>
  );
}
