import type { Member, Session, User } from "@generated/prisma/client";
import { auth } from "@/lib/auth/auth";
import type { OrganizationPermissions } from "@/lib/auth/organization-permissions";
import { findMemberByOrganizationAndUser } from "@/repositories/customers/memberRepository";
import { forbiddenResponse, unauthorizedResponse } from "@/app/api/response";
import { withErrorHandler } from "@/app/api/with-error-handler";

export type CustomerContext = {
  user: User;
  session: Session;
  membership: Member;
  organizationId: string;
};

type RouteContext = { params: Promise<Record<string, string>> };
type CustomerHandler = (
  request: Request,
  context: RouteContext,
  customerContext: CustomerContext,
) => Promise<Response>;

export function withCustomer(handler: CustomerHandler, permissions?: OrganizationPermissions) {
  return withErrorHandler(async (request, context) => {
    const session = await auth.api.getSession({ headers: request.headers });
    if (!session || ("error" in session && session.error)) {
      return unauthorizedResponse();
    }

    const organizationId = session.session.activeOrganizationId;
    if (!organizationId) {
      return forbiddenResponse("Select an organization to continue.");
    }

    const membership = await findMemberByOrganizationAndUser(organizationId, session.user.id);
    if (!membership) {
      return forbiddenResponse("You do not have access to this organization.");
    }

    if (permissions) {
      const { success } = await auth.api.hasPermission({
        body: {
          organizationId,
          permissions: permissions as Record<string, string[]>,
        },
        headers: request.headers,
      });

      if (!success) {
        return forbiddenResponse();
      }
    }

    return handler(request, context, {
      user: session.user as User,
      session: session.session as Session,
      membership,
      organizationId,
    });
  });
}
