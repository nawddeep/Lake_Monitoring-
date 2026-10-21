"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { authApi } from "@/services/api/auth/authApi";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import { Button } from "@/components/ui/button";

type AcceptExistingAdminInvitationProps = {
  invitationId: string;
  email: string;
  isSignedInAsInvitee: boolean;
  hasSession: boolean;
};

export function AcceptExistingAdminInvitation({
  invitationId,
  email,
  isSignedInAsInvitee,
  hasSession,
}: AcceptExistingAdminInvitationProps) {
  const router = useRouter();
  const callbackUrl = `/accept-invitation/admin-portal/${invitationId}`;
  const loginUrl = `/login?callbackUrl=${encodeURIComponent(callbackUrl)}`;

  const acceptMutation = useMutation({
    mutationFn: () => authApi.acceptExistingAdminInvitation({ invitationId }),
    onSuccess: () => {
      router.push("/admin/dashboard");
      router.refresh();
    },
  });

  const signOutMutation = useMutation({
    mutationFn: () => authApi.signOut(),
    onSuccess: () => router.push(loginUrl),
  });

  if (!isSignedInAsInvitee) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Sign in with {email} to accept this invitation using your existing account.
        </p>
        {hasSession ? (
          <PrimaryButton
            onClick={() => signOutMutation.mutate()}
            isPending={signOutMutation.isPending}
            pendingLabel="Signing out..."
          >
            Sign in with another account
          </PrimaryButton>
        ) : (
          <Button asChild>
            <Link href={loginUrl}>Sign in to accept</Link>
          </Button>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-muted-foreground">
        Accept this invitation to add Admin Portal access to your existing account.
      </p>
      <MutationError
        isError={acceptMutation.isError}
        error={acceptMutation.error}
        fallback="Unable to accept the invitation. Please try again."
      />
      <PrimaryButton
        onClick={() => acceptMutation.mutate()}
        isPending={acceptMutation.isPending}
        pendingLabel="Joining..."
      >
        Join the admin portal
      </PrimaryButton>
    </div>
  );
}
