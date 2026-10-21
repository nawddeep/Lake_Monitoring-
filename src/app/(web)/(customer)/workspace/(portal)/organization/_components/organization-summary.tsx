import type { Organization } from "@/types/organization";

const details: Array<{ label: string; getValue: (organization: Organization) => string }> = [
  {
    label: "Name",
    getValue: (organization) => organization.name,
  },
  {
    label: "Slug",
    getValue: (organization) => organization.slug ?? "—",
  },
  {
    label: "Created",
    getValue: (organization) => new Date(organization.createdAt).toLocaleDateString(),
  },
];

export function OrganizationSummary({ organization }: { organization: Organization }) {
  return (
    <dl className="space-y-3">
      {details.map(({ label, getValue }) => (
        <div key={label} className="flex items-center gap-2">
          <dt className="w-28 shrink-0 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {label}
          </dt>
          <dd className="text-sm text-foreground">{getValue(organization)}</dd>
        </div>
      ))}
    </dl>
  );
}
