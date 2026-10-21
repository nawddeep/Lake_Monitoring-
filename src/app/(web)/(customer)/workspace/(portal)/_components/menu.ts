import { Building2, LayoutDashboard, Users } from "lucide-react";
import type { SidebarData } from "@/components/layout/types";

export const menu: SidebarData = {
  navGroups: [
    {
      title: "General",
      items: [
        {
          title: "Dashboard",
          url: "/workspace",
          icon: LayoutDashboard,
        },
      ],
    },
    {
      title: "Administration",
      items: [
        {
          title: "Members",
          url: "/workspace/members",
          icon: Users,
        },
        {
          title: "Organization",
          url: "/workspace/organization",
          icon: Building2,
        },
      ],
    },
  ],
};
