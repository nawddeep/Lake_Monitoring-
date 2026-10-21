import { type AdminPermissions } from "@/lib/auth/admin-permissions";

type BaseNavItem = {
  title: string;
  badge?: string;
  icon?: React.ElementType;
  permissions?: AdminPermissions;
};

type NavLink = BaseNavItem & {
  url: string;
  items?: never;
};

type NavCollapsible = BaseNavItem & {
  items: (BaseNavItem & { url: string })[];
  url?: never;
};

type NavItem = NavCollapsible | NavLink;

type NavGroup = {
  title: string;
  items: NavItem[];
};

type SidebarData = {
  navGroups: NavGroup[];
};

export type { SidebarData, NavGroup, NavItem, NavCollapsible, NavLink };
