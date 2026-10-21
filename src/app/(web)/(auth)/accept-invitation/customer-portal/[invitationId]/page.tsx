import Link from "next/link";
import type { ReactNode } from "react";
import { markInvitationAccepted } from "@/repositories/auth/invitationRepository";
import { findCustomerInvitationById } from "@/repositories/customers/invitationRepository";
import {
  createMember,
  findMemberByOrganizationAndUser,
} from "@/repositories/customers/memberRepository";
import { findUserByEmail } from "@/repositories/customers/userRepository";
import { AcceptCustomerInvitationForm } from "@/components/auth/accept-customer-invitation-form";
import { Button } from "@/components/ui/button";
import { appConfig } from "@/config/app";

export default async function AcceptCustomerInvitationPage({
  params,
}: {
  params: Promise<{ invitationId: string }>;
}) {
  const { invitationId } = await params;
  const invitation = await findCustomerInvitationById(invitationId);
  const now = new Date();

  let content: ReactNode;

  if (!invitation) {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invalid invitation</h1>
        <p className="text-sm text-muted-foreground">
          This invitation link is invalid. Ask the organization owner to send you a new invitation.
        </p>
      </>
    );
  } else if (!invitation.organization) {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invalid invitation</h1>
        <p className="text-sm text-muted-foreground">
          This invitation is missing organization details. Ask the organization owner to send you a
          new invitation.
        </p>
      </>
    );
  } else if (invitation.status === "canceled") {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invitation canceled</h1>
        <p className="text-sm text-muted-foreground">
          This invitation was canceled. Ask the organization owner for a new invitation if you still
          need access.
        </p>
      </>
    );
  } else if (invitation.expiresAt < now) {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invitation expired</h1>
        <p className="text-sm text-muted-foreground">
          This invitation has expired. Ask the organization owner to send you a new invitation.
        </p>
      </>
    );
  } else if (invitation.status === "accepted") {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Already joined</h1>
        <p className="text-sm text-muted-foreground">
          This invitation has already been accepted. You can{" "}
          <Link className="font-medium text-primary" href="/login">
            sign in here
          </Link>
          .
        </p>
      </>
    );
  } else {
    const email = invitation.email.toLowerCase();
    const existingUser = await findUserByEmail(email);

    if (existingUser && invitation.organizationId) {
      const existingMember = await findMemberByOrganizationAndUser(
        invitation.organizationId,
        existingUser.id,
      );

      if (!existingMember) {
        await createMember({
          userId: existingUser.id,
          organizationId: invitation.organizationId,
          role: invitation.role,
        });
      }

      if (invitation.status !== "accepted") {
        await markInvitationAccepted(invitationId);
      }

      content = (
        <>
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invitation accepted</h1>
          <p className="mb-6 text-sm text-muted-foreground">
            You now have access to {invitation.organization.name}. Continue to the workspace when
            you’re ready.
          </p>
          <Button asChild>
            <Link href="/workspace">Go to workspace</Link>
          </Button>
          <p className="mt-4 text-xs text-muted-foreground">
            Use your existing account ({invitation.email}) to sign in if prompted.
          </p>
        </>
      );
    } else {
      content = (
        <>
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">
            Join {invitation.organization.name}
          </h1>
          <p className="mb-8 text-sm text-muted-foreground">
            Set your profile details and password to finish setting up your access.
          </p>
          <AcceptCustomerInvitationForm invitationId={invitationId} email={invitation.email} />
        </>
      );
    }
  }

  return (
    <div className="flex min-h-screen">
      <div className="relative hidden w-1/2 flex-col bg-zinc-900 p-10 md:flex">
        <div className="text-white">
          <p className="mt-1 text-xl font-semibold">{appConfig.name}</p>
          <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
            {new Date().getFullYear()} {appConfig.name}
          </p>
        </div>
      </div>

      <div className="flex w-full flex-col items-start justify-start px-16 pt-[20vh] md:w-1/2">
        <div className="w-full max-w-sm space-y-6">{content}</div>
      </div>
    </div>
  );
}
