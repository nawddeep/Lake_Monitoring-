"use client";

import { NavGroup } from "@/components/layout/nav-group";
import type { NavGroup as NavGroupType } from "@/components/layout/types";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
import { useLayout } from "@/context/layout-provider";

type AppSidebarProps = {
  header: React.ReactNode;
  navigationGroups: NavGroupType[];
  footer: React.ReactNode;
};

export function AppSidebar({ header, navigationGroups, footer }: AppSidebarProps) {
  const { collapsible, variant } = useLayout();

  return (
    <Sidebar collapsible={collapsible} variant={variant}>
      <SidebarHeader>{header}</SidebarHeader>
      <SidebarContent>
        {navigationGroups.map((properties) => (
          <NavGroup key={properties.title} {...properties} />
        ))}
      </SidebarContent>
      <SidebarFooter>{footer}</SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
