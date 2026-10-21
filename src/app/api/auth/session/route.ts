import { auth } from "@/lib/auth/auth";
import { type SessionResult } from "@/lib/auth/session";
import { detailResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export const GET = withErrorHandler(async (request) => {
  const session = await auth.api.getSession({ headers: request.headers });

  let data: SessionResult;

  if (!session || ("error" in session && session.error)) {
    data = null;
  } else {
    data = {
      user: session.user,
      session: session.session,
    } as SessionResult;
  }

  return detailResponse(data);
});
