import Link from "next/link";
import type { ReactNode } from "react";
import { fetchSession } from "@/lib/auth/session";
import { findAdminInvitationById } from "@/repositories/auth/invitationRepository";
import { findUserByEmail } from "@/repositories/auth/userRepository";
import { AcceptAdminInvitationForm } from "@/components/auth/accept-admin-invitation-form";
import { AcceptExistingAdminInvitation } from "@/components/auth/accept-existing-admin-invitation";
import { appConfig } from "@/config/app";

export default async function AcceptAdminInvitationPage({
  params,
}: {
  params: Promise<{ invitationId: string }>;
}) {
  const { invitationId } = await params;
  const invitation = await findAdminInvitationById(invitationId);
  const now = new Date();

  let content: ReactNode;

  if (!invitation) {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invalid invitation</h1>
        <p className="text-sm text-muted-foreground">
          This invitation link is invalid. Ask an admin to send you a new invitation.
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
  } else if (invitation.status === "canceled") {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invitation canceled</h1>
        <p className="text-sm text-muted-foreground">
          This invitation was canceled. Ask an admin for a new invitation if you still need access.
        </p>
      </>
    );
  } else if (invitation.expiresAt < now) {
    content = (
      <>
        <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invitation expired</h1>
        <p className="text-sm text-muted-foreground">
          This invitation has expired. Ask an admin to send you a new invitation.
        </p>
      </>
    );
  } else {
    const existingUser = await findUserByEmail(invitation.email);

    if (existingUser?.role) {
      content = (
        <>
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">Access already granted</h1>
          <p className="text-sm text-muted-foreground">
            This account already has access to the Admin Portal.
          </p>
        </>
      );
    } else if (existingUser) {
      const session = await fetchSession();
      content = (
        <>
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">Join the Admin Portal</h1>
          <AcceptExistingAdminInvitation
            invitationId={invitationId}
            email={invitation.email}
            hasSession={Boolean(session)}
            isSignedInAsInvitee={
              session?.user.email.toLowerCase() === invitation.email.toLowerCase()
            }
          />
        </>
      );
    } else {
      content = (
        <>
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">Join the Admin Portal</h1>
          <p className="mb-8 text-sm text-muted-foreground">
            Set your profile details and password to finish setting up your account.
          </p>
          <AcceptAdminInvitationForm invitationId={invitationId} email={invitation.email} />
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
