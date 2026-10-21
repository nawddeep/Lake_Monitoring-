"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import type { z } from "zod";
import { teamApi } from "@/services/api/admin/teamApi";
import { createAdminPortalInvitationSchema } from "@/app/api/admin/team/invitations/schema";
import type { Invitation } from "@/types/invitation";

export type InviteTeamMemberFormValues = z.infer<typeof createAdminPortalInvitationSchema>;

export function useInviteTeamMemberForm(onSuccess: (invitation: Invitation) => void) {
  const queryClient = useQueryClient();

  const form = useForm<InviteTeamMemberFormValues>({
    resolver: zodResolver(createAdminPortalInvitationSchema),
    defaultValues: { email: "", role: "user" },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (values: InviteTeamMemberFormValues) => teamApi.inviteMember(values),
    onSuccess: (invitation) => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "team"] });
      toast.success("Invitation created.");
      form.reset();
      onSuccess(invitation);
    },
  });

  return { form, mutate, isPending, isError, error };
}
