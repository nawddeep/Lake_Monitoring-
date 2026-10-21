"use client";

import { AppSidebar } from "@/components/layout/app-sidebar";
import { NavUser } from "@/components/layout/nav-user";
import { menu } from "@/app/(web)/(customer)/workspace/(portal)/_components/menu";
import { Title } from "@/app/(web)/(customer)/workspace/(portal)/_components/title";
import type { User } from "@/types/user";

type SidebarProps = {
  user: User;
  activeOrganizationId: string;
  organizationName: string;
};

export function Sidebar({ user, activeOrganizationId, organizationName }: SidebarProps) {
  return (
    <AppSidebar
      header={<Title organizationName={organizationName} />}
      navigationGroups={menu.navGroups}
      footer={
        <NavUser
          user={user}
          portal="customer"
          accountUrl="/workspace/account"
          activeOrganizationId={activeOrganizationId}
        />
      }
    />
  );
}
