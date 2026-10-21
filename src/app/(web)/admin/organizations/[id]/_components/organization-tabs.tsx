"use client";

import Link from "next/link";
import { useSelectedLayoutSegment } from "next/navigation";
import type { ReactNode } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const SECTIONS = [
  { value: "members", label: "Members" },
  { value: "invitations", label: "Invitations" },
] as const;

export function OrganizationTabs({
  organizationId,
  children,
}: {
  organizationId: string;
  children: ReactNode;
}) {
  const segment = useSelectedLayoutSegment();
  const activeValue = segment ?? "members";

  return (
    <Tabs value={activeValue} className="space-y-6">
      <TabsList variant="line">
        {SECTIONS.map(({ value, label }) => (
          <TabsTrigger key={value} value={value} asChild>
            <Link href={`/admin/organizations/${organizationId}/${value}`}>{label}</Link>
          </TabsTrigger>
        ))}
      </TabsList>

      <TabsContent value={activeValue}>{children}</TabsContent>
    </Tabs>
  );
}
