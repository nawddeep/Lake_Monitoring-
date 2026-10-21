import { acceptAdminInvitationSchema } from "./schema";
import { prisma } from "@/lib/prisma";
import { findAdminInvitationById } from "@/repositories/auth/invitationRepository";
import { BaseValidator } from "@/validators/BaseValidator";

export type AcceptAdminInvitationData = {
  invitationId: string;
  trimmedFirstName: string;
  trimmedLastName: string;
  fullName: string;
  email: string;
  password: string;
  role: string;
};

export class AcceptAdminInvitationValidator extends BaseValidator<AcceptAdminInvitationData> {
  constructor(private body: unknown) {
    super();
  }

  async validate(): Promise<boolean> {
    const parsed = acceptAdminInvitationSchema.safeParse(this.body);
    if (!parsed.success) {
      this.mapZodErrors(parsed.error.issues);
      return false;
    }

    const { invitationId, firstName, lastName, password } = parsed.data;

    const invitation = await findAdminInvitationById(invitationId);
    if (!invitation) {
      this.errors.push({ path: ["invitationId"], message: "Invitation not found." });
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
    const fullName = `${trimmedFirstName} ${trimmedLastName}`.trim() || invitation.email;

    this.validatedData = {
      invitationId,
      trimmedFirstName,
      trimmedLastName,
      fullName,
      email,
      password,
      role: invitation.role,
    };

    return true;
  }
}
