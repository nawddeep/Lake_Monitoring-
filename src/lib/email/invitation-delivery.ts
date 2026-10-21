import type { Invitation } from "@/types/invitation";

// Email failure is recoverable: the invitation can still be shared directly.
export async function attemptInvitationEmail(
  send: () => Promise<void>,
): Promise<NonNullable<Invitation["emailStatus"]>> {
  if (process.env.INVITATION_EMAIL_ENABLED === "false" || !process.env.RESEND_API_KEY) {
    return "not_sent";
  }
  try {
    await send();
    return "sent";
  } catch (error) {
    console.error("[Invitation] Email delivery attempt failed:", error);
    return "failed";
  }
}
