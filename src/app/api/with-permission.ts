import { type AdminPermissions } from "@/lib/auth/admin-permissions";
import { auth } from "@/lib/auth/auth";
import { forbiddenResponse } from "@/app/api/response";

type RouteHandler = (
  request: Request,
  context: { params: Promise<Record<string, string>> },
) => Promise<Response>;

export function withPermission(permissions: AdminPermissions) {
  return (handler: RouteHandler): RouteHandler =>
    async (request, context) => {
      const session = await auth.api.getSession({ headers: request.headers });
      const { success } = await auth.api.userHasPermission({
        body: {
          userId: session?.user.id,
          permissions: permissions as Record<string, string[]>,
        },
      });

      if (!success) {
        return forbiddenResponse();
      }

      return handler(request, context);
    };
}
