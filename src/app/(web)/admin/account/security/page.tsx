import type { Metadata } from "next";
import { ChangePasswordForm } from "@/components/users/change-password-form";

export const metadata: Metadata = { title: "Security" };

export default function SecurityPage() {
  return <ChangePasswordForm />;
}
