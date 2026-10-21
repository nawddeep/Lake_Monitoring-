"use client";

import { useUsers } from "./users-provider";
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

export function UserDetailsSheet() {
  const { open, setOpen, currentUser } = useUsers();
  if (!currentUser) return null;

  const fullName =
    [currentUser.firstName, currentUser.lastName].filter(Boolean).join(" ") || currentUser.name;

  return (
    <Sheet open={open === "view"} onOpenChange={(value) => !value && setOpen(null)}>
      <SheetContent className="flex flex-col gap-0 p-0">
        <SheetHeader className="border-b p-6">
          <div className="flex items-center gap-4">
            <UserAvatar
              user={currentUser}
              alt={fullName}
              className="h-12 w-12"
              fallbackClassName="text-lg font-semibold text-muted-foreground"
            />
            <div>
              <SheetTitle>{fullName}</SheetTitle>
              <SheetDescription>{currentUser.email}</SheetDescription>
            </div>
          </div>
        </SheetHeader>

        <div className="flex flex-col gap-6 overflow-y-auto p-6">
          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Account</h3>
            <DetailRow label="First name" value={currentUser.firstName} />
            <DetailRow label="Last name" value={currentUser.lastName} />
            <DetailRow label="Email" value={currentUser.email} />
            <DetailRow
              label="Email verified"
              value={
                currentUser.emailVerified ? (
                  <Badge variant="secondary">Verified</Badge>
                ) : (
                  <Badge variant="outline">Unverified</Badge>
                )
              }
            />
            <DetailRow
              label="Admin role"
              value={<span className="capitalize">{currentUser.role}</span>}
            />
            <DetailRow
              label="Portal access"
              value={
                currentUser.access === "both"
                  ? "Admin and customer"
                  : currentUser.access === "admin_only"
                    ? "Admin only"
                    : currentUser.access === "customer_only"
                      ? "Customer only"
                      : "None"
              }
            />
          </section>

          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Status</h3>
            <DetailRow
              label="Account status"
              value={
                currentUser.banned ? (
                  <Badge variant="destructive">Banned</Badge>
                ) : (
                  <Badge variant="secondary">Active</Badge>
                )
              }
            />
            {currentUser.banned && (
              <>
                <DetailRow label="Reason" value={currentUser.banReason} />
                <DetailRow
                  label="Expires"
                  value={
                    currentUser.banExpires
                      ? new Date(currentUser.banExpires).toLocaleDateString()
                      : null
                  }
                />
              </>
            )}
          </section>

          <section className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold">Dates</h3>
            <DetailRow
              label="Created"
              value={new Date(currentUser.createdAt).toLocaleDateString()}
            />
            <DetailRow
              label="Updated"
              value={new Date(currentUser.updatedAt).toLocaleDateString()}
            />
          </section>
        </div>
      </SheetContent>
    </Sheet>
  );
}
