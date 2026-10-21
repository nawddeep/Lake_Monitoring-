"use client";

import { usePathname, useRouter } from "next/navigation";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface NavTab {
  label: string;
  href: string;
}

interface NavTabsProps {
  tabs: NavTab[];
}

export function NavTabs({ tabs }: NavTabsProps) {
  const pathname = usePathname();
  const router = useRouter();

  const activeTab =
    tabs.find((tab) => pathname === tab.href)?.href ??
    tabs.find((tab) => pathname.startsWith(tab.href))?.href ??
    tabs[0].href;

  return (
    <Tabs value={activeTab} onValueChange={(href) => router.push(href)}>
      <TabsList variant="line" className="mb-6">
        {tabs.map((tab) => (
          <TabsTrigger key={tab.href} value={tab.href}>
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
  );
}
