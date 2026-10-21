import { Resend } from "resend";

let resend: Resend | undefined;

export function getResend() {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    throw new Error("RESEND_API_KEY is required to send email.");
  }

  resend ??= new Resend(apiKey);
  return resend;
}

export const EMAIL_FROM = process.env.EMAIL_FROM ?? "onboarding@resend.dev";
