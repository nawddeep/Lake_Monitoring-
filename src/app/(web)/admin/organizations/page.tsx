"use client";

import { organizationsApi } from "@/services/api/admin/organizationsApi";
import { DataTable } from "@/components/data-table/data-table";
import { AddOrganizationModal } from "@/components/organizations/add-organization-modal";
import { ContentLayout } from "@/components/platform/content-layout";
import { useConnectedTable } from "@/hooks/use-connected-table";
import { DeleteOrganizationDialog } from "@/app/(web)/admin/organizations/_components/delete-organization-dialog";
import { OrganizationsProvider } from "@/app/(web)/admin/organizations/_components/organizations-provider";
import { UpdateOrganizationDialog } from "@/app/(web)/admin/organizations/_components/update-organization-dialog";
import { columns } from "@/app/(web)/admin/organizations/columns";
import { useAdminPermissions } from "@/context/admin-permission-provider";

const ORGANIZATIONS_QUERY_KEY = ["admin", "organizations"];

export default function OrganizationsPage() {
  const { can } = useAdminPermissions();
  const { table } = useConnectedTable({
    queryKey: ORGANIZATIONS_QUERY_KEY,
    queryFn: (params) => organizationsApi.listOrganizations(params),
    columns,
  });

  return (
    <OrganizationsProvider>
      <ContentLayout
        title="Organizations"
        description="Manage organizations and members"
        actions={
          can({ organization: "create" }) ? (
            <AddOrganizationModal queryKey={ORGANIZATIONS_QUERY_KEY} />
          ) : undefined
        }
      >
        <DataTable table={table} showSearch searchPlaceholder="Search by name or slug..." />
      </ContentLayout>

      <UpdateOrganizationDialog />
      <DeleteOrganizationDialog />
    </OrganizationsProvider>
  );
}
