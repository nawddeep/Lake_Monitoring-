"use client";

import { useRouter } from "next/navigation";
import { useTransition } from "react";
import { invitationsApi } from "@/services/api/admin/invitationsApi";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

type Member = {
  id: string;
  role: string;
  user: {
    id: string;
    firstName: string | null;
    lastName: string | null;
    name: string;
    email: string;
  };
};

type Invitation = {
  id: string;
  email: string;
  role: string;
  status: string;
  createdAt: Date;
  expiresAt: Date;
};

function CancelButton({
  organizationId,
  invitationId,
}: {
  organizationId: string;
  invitationId: string;
}) {
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  const handleCancel = () => {
    startTransition(async () => {
      await invitationsApi.cancelOrganizationInvitation(organizationId, invitationId);
      router.refresh();
    });
  };

  return (
    <Button variant="ghost" size="sm" disabled={isPending} onClick={handleCancel}>
      {isPending ? "Canceling..." : "Cancel"}
    </Button>
  );
}

const statusVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  pending: "default",
  accepted: "secondary",
  rejected: "outline",
  canceled: "destructive",
};

export function OrgDetailTabs({
  organizationId,
  members,
  invitations,
}: {
  organizationId: string;
  members: Member[];
  invitations: Invitation[];
}) {
  return (
    <Tabs defaultValue="users">
      <TabsList>
        <TabsTrigger value="users">Users</TabsTrigger>
        <TabsTrigger value="invitations">Invitations</TabsTrigger>
      </TabsList>

      <TabsContent value="users" className="mt-4">
        {members.length === 0 ? (
          <p className="text-sm text-muted-foreground">No users in this organization.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {members.map((member) => (
                <TableRow key={member.id}>
                  <TableCell className="font-medium">
                    {member.user.firstName && member.user.lastName
                      ? `${member.user.firstName} ${member.user.lastName}`
                      : member.user.name}
                  </TableCell>
                  <TableCell className="text-muted-foreground">{member.user.email}</TableCell>
                  <TableCell className="capitalize text-muted-foreground">{member.role}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </TabsContent>

      <TabsContent value="invitations" className="mt-4">
        {invitations.length === 0 ? (
          <p className="text-sm text-muted-foreground">No invitations sent yet.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Sent</TableHead>
                <TableHead>Expires</TableHead>
                <TableHead />
              </TableRow>
            </TableHeader>
            <TableBody>
              {invitations.map((inv) => (
                <TableRow key={inv.id}>
                  <TableCell className="font-medium">{inv.email}</TableCell>
                  <TableCell className="capitalize text-muted-foreground">{inv.role}</TableCell>
                  <TableCell>
                    <Badge variant={statusVariant[inv.status] ?? "outline"} className="capitalize">
                      {inv.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {inv.createdAt.toLocaleDateString()}
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {inv.expiresAt.toLocaleDateString()}
                  </TableCell>
                  <TableCell className="text-right">
                    {inv.status === "pending" && (
                      <CancelButton organizationId={organizationId} invitationId={inv.id} />
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </TabsContent>
    </Tabs>
  );
}
