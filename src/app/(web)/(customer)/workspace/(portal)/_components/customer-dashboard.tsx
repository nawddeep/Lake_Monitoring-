import Link from "next/link";
import { ArrowUpRight, Building2, MailPlus, Users } from "lucide-react";

const workspaceCapabilities = [
  {
    title: "Members",
    description: "Review the people in your organization and manage their workspace roles.",
    href: "/workspace/members",
    icon: Users,
  },
  {
    title: "Invitations",
    description: "Track pending invitations and manage access before someone joins your team.",
    href: "/workspace/members/invitations",
    icon: MailPlus,
  },
  {
    title: "Organization details",
    description: "View the core information associated with the organization in this workspace.",
    href: "/workspace/organization",
    icon: Building2,
  },
] as const;

export function CustomerDashboard() {
  return (
    <section aria-labelledby="workspace-capabilities-heading">
      <div className="mb-4">
        <h2 id="workspace-capabilities-heading" className="text-lg font-semibold">
          Workspace capabilities
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Everything you need to manage your organization and the people who can access it.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {workspaceCapabilities.map(({ title, description, href, icon: Icon }) => (
          <Link
            key={title}
            href={href}
            className="group flex min-h-40 flex-col justify-between rounded-xl border bg-card p-5 transition-colors hover:border-foreground/20 hover:bg-muted/30"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <Icon className="size-5" />
              </div>
              <ArrowUpRight className="size-4 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-foreground" />
            </div>
            <div className="mt-6">
              <h3 className="font-semibold">{title}</h3>
              <p className="mt-1 text-sm leading-6 text-muted-foreground">{description}</p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
