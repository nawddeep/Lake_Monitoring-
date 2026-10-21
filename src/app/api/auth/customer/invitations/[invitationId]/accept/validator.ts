import { acceptCustomerInvitationSchema } from "./schema";
import { prisma } from "@/lib/prisma";
import { findCustomerInvitationById } from "@/repositories/customers/invitationRepository";
import { BaseValidator } from "@/validators/BaseValidator";

export type AcceptCustomerInvitationData = {
  invitationId: string;
  firstName: string;
  lastName: string;
  fullName: string;
  email: string;
  password: string;
  role: string;
  organizationId: string;
};

export class AcceptCustomerInvitationValidator extends BaseValidator<AcceptCustomerInvitationData> {
  constructor(
    private invitationId: string,
    private body: unknown,
  ) {
    super();
  }

  async validate(): Promise<boolean> {
    const parsed = acceptCustomerInvitationSchema.safeParse(this.body);
    if (!parsed.success) {
      this.mapZodErrors(parsed.error.issues);
      return false;
    }

    const { firstName, lastName, password } = parsed.data;
    const invitation = await findCustomerInvitationById(this.invitationId);

    if (!invitation) {
      this.errors.push({ path: ["invitationId"], message: "Invitation not found." });
      return false;
    }

    if (!invitation.organizationId) {
      this.errors.push({
        path: ["invitationId"],
        message: "This invitation is not associated with an organization.",
      });
      return false;
    }

    if (invitation.status === "accepted") {
      this.errors.push({
        path: ["invitationId"],
        message: "This invitation has already been accepted.",
      });
      return false;
    }

    if (invitation.status === "canceled") {
      this.errors.push({ path: ["invitationId"], message: "This invitation has been canceled." });
      return false;
    }

    if (invitation.expiresAt < new Date()) {
      this.errors.push({ path: ["invitationId"], message: "This invitation has expired." });
      return false;
    }

    const email = invitation.email.toLowerCase();
    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
      this.errors.push({ path: ["email"], message: "An account already exists for this email." });
      return false;
    }

    const trimmedFirstName = firstName.trim();
    const trimmedLastName = lastName.trim();
    const fullName = `${trimmedFirstName} ${trimmedLastName}`.trim();

    this.validatedData = {
      invitationId: this.invitationId,
      firstName: trimmedFirstName,
      lastName: trimmedLastName,
      fullName,
      email,
      password,
      role: invitation.role,
      organizationId: invitation.organizationId,
    };

    return true;
  }
}
