"use client";

import { AppSidebar } from "@/components/layout/app-sidebar";
import { AppTitle } from "@/components/layout/app-title";
import { NavUser } from "@/components/layout/nav-user";
import { menu } from "@/app/(web)/admin/_components/menu";
import { useAdminPermissions } from "@/context/admin-permission-provider";
import type { User } from "@/types/user";

type SidebarProps = {
  user: User;
};

export function Sidebar({ user }: SidebarProps) {
  const { can } = useAdminPermissions();
  const navGroups = menu.navGroups.map((group) => ({
    ...group,
    items: group.items.filter((item) => !item.permissions || can(item.permissions)),
  }));

  return (
    <AppSidebar
      header={<AppTitle />}
      navigationGroups={navGroups}
      footer={<NavUser user={user} portal="admin" accountUrl="/admin/account" />}
    />
  );
}
