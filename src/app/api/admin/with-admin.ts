import type { Session, User } from "@generated/prisma/client";
import { type AdminPermissions } from "@/lib/auth/admin-permissions";
import { fetchSession } from "@/lib/auth/session";
import { forbiddenResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";
import { withPermission } from "@/app/api/with-permission";

export type AdminContext = {
  user: User;
  session: Session;
};

type RouteContext = { params: Promise<Record<string, string>> };

type AdminHandler = (
  request: Request,
  context: RouteContext,
  adminContext: AdminContext,
) => Promise<Response>;

export function withAdmin(handler: AdminHandler, permissions?: AdminPermissions) {
  return withErrorHandler(async (request, context) => {
    const result = await fetchSession();

    if (!result?.user) {
      return unauthorizedResponse();
    }

    const { user, session } = result;

    if (!user.role) {
      return forbiddenResponse();
    }

    const adminContext: AdminContext = { user, session };

    if (permissions) {
      return withPermission(permissions)((req, ctx) => handler(req, ctx, adminContext))(
        request,
        context,
      );
    }

    return handler(request, context, adminContext);
  });
}
