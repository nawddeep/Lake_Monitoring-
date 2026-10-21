"use client";

import { useOrganizationMembers } from "./organization-members-provider";
import { Badge } from "@/components/ui/badge";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { UserAvatar } from "@/components/users/user-avatar";

function DetailRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
        {label}
      </span>
      <span className="text-sm">{value ?? <span className="text-muted-foreground">—</span>}</span>
    </div>
  );
}

export function MemberDetailsSheet() {
  const { open, setOpen, currentMember } = useOrganizationMembers();
  if (!currentMember) return null;

  const { user } = currentMember;
  const fullName = [user.firstName, user.lastName].filter(Boolean).join(" ") || user.name;

  return (
    <Sheet open={open === "view"} onOpenChange={(value) => !value && setOpen(null)}>
      <SheetContent className="flex flex-col gap-0 p-0">
        <SheetHeader className="border-b p-6">
          <div className="flex items-center gap-4">
            <UserAvatar
              user={user}
              alt={fullName}
              className="h-12 w-12"
              fallbackClassName="text-lg font-semibold text-muted-foreground"
            />
            <div>
              <SheetTitle>{fullName}</SheetTitle>
              <SheetDescription>{user.email}</SheetDescription>
            </div>
          </div>
        </SheetHeader>

        <div className="flex flex-col gap-6 overflow-y-auto p-6">
          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Account</h3>
            <DetailRow label="First name" value={user.firstName} />
            <DetailRow label="Last name" value={user.lastName} />
            <DetailRow label="Email" value={user.email} />
            <DetailRow
              label="Email verified"
              value={
                user.emailVerified ? (
                  <Badge variant="secondary">Verified</Badge>
                ) : (
                  <Badge variant="outline">Unverified</Badge>
                )
              }
            />
            <DetailRow
              label="Status"
              value={
                user.banned ? (
                  <Badge variant="destructive">Banned</Badge>
                ) : (
                  <Badge variant="secondary">Active</Badge>
                )
              }
            />
          </section>

          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Membership</h3>
            <DetailRow
              label="Role"
              value={<span className="capitalize">{currentMember.role}</span>}
            />
            <DetailRow
              label="Joined"
              value={new Date(currentMember.createdAt).toLocaleDateString()}
            />
          </section>
        </div>
      </SheetContent>
    </Sheet>
  );
}
