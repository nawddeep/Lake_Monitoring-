import Link from "next/link";
import { redirect } from "next/navigation";
import { requireSession } from "@/lib/auth/session";
import { listUserOrganizations } from "@/repositories/customers/organizationRepository";
import { ContentLayout } from "@/components/platform/content-layout";

export default async function NoOrganizationPage() {
  const session = await requireSession();
  const organizations = await listUserOrganizations(session.user.id);

  if (organizations.length > 0) {
    redirect("/workspace");
  }

  return (
    <ContentLayout
      title="No organization access"
      description="Your account hasn’t been added to an organization yet."
    >
      <div className="space-y-4 text-sm text-muted-foreground">
        <p>
          You’ll need to be invited to an organization before you can use the customer portal. If
          you were expecting access, reach out to your administrator and ask them to send you an
          invitation.
        </p>
        <p>
          In the meantime, you can return to the{" "}
          <Link className="font-medium text-primary" href="/login">
            sign-in page
          </Link>
          .
        </p>
      </div>
    </ContentLayout>
  );
}
