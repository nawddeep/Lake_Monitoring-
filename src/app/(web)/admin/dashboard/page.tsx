import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowUpRight,
  Building2,
  KeyRound,
  MailPlus,
  ShieldCheck,
  UserCog,
  Users,
} from "lucide-react";
import { getAdminPermissions } from "@/lib/auth/admin-permissions";
import { requireSession } from "@/lib/auth/session";
import { ContentLayout } from "@/components/platform/content-layout";

export const metadata: Metadata = {
  title: "Dashboard",
};

const capabilities = [
  {
    title: "Organizations",
    description:
      "Create and manage the tenants that make up your application, including their members and invitations.",
    href: "/admin/organizations",
    icon: Building2,
  },
  {
    title: "Admin team",
    description:
      "Invite platform operators, assign their roles, and control access to the administrative portal.",
    href: "/admin/team",
    icon: UserCog,
  },
  {
    title: "User management",
    description:
      "Review users across the platform, inspect their access, impersonate accounts for support, and manage account-level restrictions.",
    href: "/admin/users",
    icon: Users,
  },
  {
    title: "Invitation management",
    description:
      "Track pending access and manage invitations in the team or organization where they belong.",
    href: "/admin/team/invitations",
    icon: MailPlus,
  },
] as const;

export default async function DashboardPage() {
  const session = await requireSession();
  const rawName = session.user.name ?? "";
  const userName = rawName
    ? rawName
        .split(/\s+/)
        .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
        .join(" ")
    : "there";
  const permissions = getAdminPermissions(session.user.role);
  const canViewApiKeys = permissions.apiKey?.includes("read:any") ?? false;

  const visibleCapabilities = canViewApiKeys
    ? [
        ...capabilities,
        {
          title: "API access",
          description:
            "Create credentials for programmatic access and revoke keys across the platform when needed.",
          href: "/admin/api-keys",
          icon: KeyRound,
        },
      ]
    : capabilities;

  return (
    <ContentLayout
      title={`Welcome back, ${userName}`}
      description="Manage the people, organizations, access, and credentials behind your multi-tenant application."
    >
      <div className="space-y-10">
        <section aria-labelledby="capabilities-heading">
          <div className="mb-4">
            <h2 id="capabilities-heading" className="text-lg font-semibold">
              Admin portal capabilities
            </h2>
            <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
              The core operational workflows are ready to use, giving you a practical foundation for
              managing a B2B SaaS platform from day one.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {visibleCapabilities.map(({ title, description, href, icon: Icon }) => (
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

        <section className="rounded-xl bg-muted/40 p-6" aria-labelledby="foundation-heading">
          <div className="flex items-start gap-4">
            <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-background text-foreground shadow-sm ring-1 ring-border">
              <ShieldCheck className="size-5" />
            </div>
            <div>
              <h2 id="foundation-heading" className="font-semibold">
                A foundation for your application
              </h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-muted-foreground">
                Authentication, tenant boundaries, roles, invitations, and platform administration
                are already in place. From here, your product can stay focused on the workflows that
                are specific to your customers. Billing and subscription automation can be added
                when the business needs it, without being required by the foundation.
              </p>
            </div>
          </div>
        </section>
      </div>
    </ContentLayout>
  );
}
