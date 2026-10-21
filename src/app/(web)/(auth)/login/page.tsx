import { redirect } from "next/navigation";
import { fetchSession } from "@/lib/auth/session";
import { LoginForm } from "@/components/auth/login-form";
import { appConfig } from "@/config/app";

function safeCallbackUrl(callbackUrl?: string) {
  return callbackUrl?.startsWith("/") && !callbackUrl.startsWith("//")
    ? callbackUrl
    : "/admin/dashboard";
}

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{
    callbackUrl?: string | string[];
    email?: string | string[];
  }>;
}) {
  const { callbackUrl, email } = await searchParams;
  const redirectTo = safeCallbackUrl(typeof callbackUrl === "string" ? callbackUrl : undefined);
  const initialEmail = typeof email === "string" ? email : email?.[0];
  const session = await fetchSession();

  if (session?.session) {
    redirect(redirectTo);
  }

  return (
    <div className="flex min-h-screen">
      <div className="relative hidden w-1/2 flex-col bg-zinc-900 p-10 md:flex">
        <div className="text-white">
          <p className="mt-1 text-xl font-semibold">{appConfig.name}</p>
        </div>
      </div>

      <div className="flex w-full flex-col items-start justify-start px-16 pt-[30vh] md:w-1/2">
        <div className="w-full max-w-sm">
          <h1 className="mb-1 text-2xl font-semibold tracking-tight">Welcome back</h1>
          <p className="mb-8 text-sm text-muted-foreground">Sign in to access your dashboard.</p>
          <LoginForm callbackUrl={redirectTo} initialEmail={initialEmail} />
        </div>
      </div>
    </div>
  );
}
