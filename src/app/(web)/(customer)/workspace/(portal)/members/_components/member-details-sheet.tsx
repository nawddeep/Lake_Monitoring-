"use client";

import { useMembers } from "./members-provider";
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
      <span className="text-sm">{value || <span className="text-muted-foreground">—</span>}</span>
    </div>
  );
}

export function MemberDetailsSheet() {
  const { open, setOpen, currentMember } = useMembers();
  if (!currentMember) return null;

  const { user } = currentMember;
  const fullName = [user.firstName, user.lastName].filter(Boolean).join(" ") || user.name;

  return (
    <Sheet open={open === "view"} onOpenChange={(value) => !value && setOpen(null)}>
      <SheetContent className="flex flex-col gap-0 p-0">
        <SheetHeader className="border-b p-6">
          <div className="flex items-center gap-4">
            <UserAvatar user={user} alt={fullName} className="h-12 w-12" />
            <div>
              <SheetTitle>{fullName}</SheetTitle>
              <SheetDescription>{user.email}</SheetDescription>
            </div>
          </div>
        </SheetHeader>
        <div className="flex flex-col gap-6 overflow-y-auto p-6">
          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Member</h3>
            <DetailRow label="First name" value={user.firstName} />
            <DetailRow label="Last name" value={user.lastName} />
            <DetailRow label="Email" value={user.email} />
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
