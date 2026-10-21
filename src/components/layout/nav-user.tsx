"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTransition } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  BadgeCheck,
  Building2,
  Check,
  ChevronsUpDown,
  LayoutDashboard,
  LogOut,
} from "lucide-react";
import { toast } from "sonner";
import { authApi } from "@/services/api/auth/authApi";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { UserAvatar } from "@/components/users/user-avatar";
import type { User } from "@/types/user";

type NavUserProps = {
  user: User;
  portal: "admin" | "customer";
  accountUrl: string;
  activeOrganizationId?: string | null;
};

export function NavUser({ user, portal, accountUrl, activeOrganizationId }: NavUserProps) {
  const { isMobile } = useSidebar();
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const { data: organizations } = useQuery({
    queryKey: ["session", "organizations"],
    queryFn: () => authApi.listOrganizations(),
  });
  const organizationOptions = organizations ?? [];
  const hasOrganizations = organizationOptions.length > 0;
  const shouldShowOrganizations =
    portal === "admin" ? hasOrganizations : organizationOptions.length > 1;
  const hasAdminPortalAccess = user.role != null;
  const { mutate: setActiveOrganization, isPending: isSwitchingOrganization } = useMutation({
    mutationFn: (organizationId: string) => authApi.setActiveOrganization({ organizationId }),
    onSuccess: () => {
      window.location.assign("/workspace");
    },
    onError: (error) => {
      toast.error(error.message || "Failed to open the customer portal.");
    },
  });

  const handleSignOut = () => {
    startTransition(async () => {
      await authApi.signOut();
      router.push("/login");
    });
  };

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <UserAvatar
                user={user}
                className="h-8 w-8 rounded-lg"
                fallbackClassName="rounded-lg"
              />
              <div className="grid flex-1 text-start text-sm leading-tight">
                <span className="truncate font-semibold">{user.name}</span>
                <span className="truncate text-xs">{user.email}</span>
              </div>
              <ChevronsUpDown className="ms-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-start text-sm">
                <UserAvatar
                  user={user}
                  className="h-8 w-8 rounded-lg"
                  fallbackClassName="rounded-lg"
                />
                <div className="grid flex-1 text-start text-sm leading-tight">
                  <span className="truncate font-semibold">{user.name}</span>
                  <span className="truncate text-xs">{user.email}</span>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem asChild>
                <Link href={accountUrl}>
                  <BadgeCheck />
                  Account
                </Link>
              </DropdownMenuItem>
            </DropdownMenuGroup>
            {((portal === "customer" && hasAdminPortalAccess) || shouldShowOrganizations) && (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  {portal === "customer" && hasAdminPortalAccess && (
                    <DropdownMenuItem asChild>
                      <Link href="/admin">
                        <LayoutDashboard />
                        Admin Portal
                      </Link>
                    </DropdownMenuItem>
                  )}
                  {shouldShowOrganizations && (
                    <DropdownMenuSub>
                      <DropdownMenuSubTrigger className="gap-2">
                        <Building2 className="size-4 text-muted-foreground" />
                        {portal === "admin" ? "Customer Portal" : "Organizations"}
                      </DropdownMenuSubTrigger>
                      <DropdownMenuSubContent>
                        {organizationOptions.map((organization) => (
                          <DropdownMenuItem
                            key={organization.id}
                            disabled={
                              isSwitchingOrganization || organization.id === activeOrganizationId
                            }
                            onSelect={() => setActiveOrganization(organization.id)}
                          >
                            {organization.name}
                            {organization.id === activeOrganizationId && (
                              <Check className="ms-auto" />
                            )}
                          </DropdownMenuItem>
                        ))}
                      </DropdownMenuSubContent>
                    </DropdownMenuSub>
                  )}
                </DropdownMenuGroup>
              </>
            )}
            <DropdownMenuSeparator />
            <DropdownMenuItem variant="destructive" onClick={handleSignOut} disabled={isPending}>
              <LogOut />
              {isPending ? "Signing out..." : "Sign out"}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
