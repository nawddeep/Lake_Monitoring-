import type { Metadata } from "next";
import { AccountApiKeysTab } from "@/app/(web)/admin/account/api-keys/_components/tab";

export const metadata: Metadata = { title: "API Keys" };

export default function AccountApiKeysPage() {
  return <AccountApiKeysTab />;
}
