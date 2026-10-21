import type { Organization } from "@/types/organization";

const DETAILS: Array<{ label: string; getValue: (org: Organization) => string }> = [
  {
    label: "Slug",
    getValue: (org) => org.slug ?? "—",
  },
  {
    label: "Created",
    getValue: (org) => new Date(org.createdAt).toLocaleDateString(),
  },
];

export function OrganizationSummary({ organization }: { organization: Organization }) {
  return (
    <div className="space-y-3 text-sm">
      <dl className="space-y-2">
        {DETAILS.map(({ label, getValue }) => (
          <div key={label} className="flex items-center gap-2">
            <dt className="w-28 shrink-0 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {label}
            </dt>
            <dd className="text-sm text-foreground">{getValue(organization)}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
