import { ResetPasswordForm } from "@/components/auth/reset-password-form";
import { appConfig } from "@/config/app";

export default async function ResetPasswordPage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string; error?: string }>;
}) {
  const { token } = await searchParams;

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

      <div className="flex w-full flex-col items-start justify-start px-16 pt-[30vh] md:w-1/2">
        <div className="w-full max-w-sm">
          {token ? (
            <>
              <h1 className="mb-1 text-2xl font-semibold tracking-tight">Set your password</h1>
              <p className="mb-8 text-sm text-muted-foreground">
                Choose a password to finish setting up your account.
              </p>
              <ResetPasswordForm token={token} />
            </>
          ) : (
            <>
              <h1 className="mb-1 text-2xl font-semibold tracking-tight">Invalid link</h1>
              <p className="mb-8 text-sm text-muted-foreground">
                This password reset link is invalid or has expired. Ask an admin to send you a new
                invitation.
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
