import { headers } from "next/headers";
import { redirect } from "next/navigation";
import type { Session, User } from "@generated/prisma/client";
import { auth } from "@/lib/auth/auth";

export type SessionResult = {
  user: User;
  session: Session;
} | null;

export type AuthenticatedSession = NonNullable<SessionResult>;

export async function requireSession(redirectTo = "/login"): Promise<AuthenticatedSession> {
  const session = await fetchSession();
  if (!session) {
    redirect(redirectTo);
  }
  return session;
}

export async function fetchSession(): Promise<SessionResult> {
  try {
    const result = await auth.api.getSession({ headers: await headers() });

    if (!result || ("error" in result && result.error)) {
      return null;
    }

    return {
      user: result.user as User,
      session: result.session as Session,
    };
  } catch {
    return null;
  }
}
