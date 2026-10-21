"use client";

import { useMutation } from "@tanstack/react-query";
import { authApi } from "@/services/api/auth/authApi";
import { PrimaryButton } from "@/components/buttons/primary-button";
import { MutationError } from "@/components/feedback/mutation-error";
import type { Organization } from "@/types/organization";

type OrganizationSelectorProps = {
  organizations: Organization[];
};

export function OrganizationSelector({ organizations }: OrganizationSelectorProps) {
  const { mutate, variables, isPending, isError, error } = useMutation({
    mutationFn: (organizationId: string) => authApi.setActiveOrganization({ organizationId }),
    onSuccess: () => {
      window.location.assign("/workspace");
    },
  });

  return (
    <div className="grid gap-4">
      <MutationError
        isError={isError}
        error={error}
        fallback="Failed to select the organization. Please try again."
      />

      {organizations.map((organization) => (
        <div
          key={organization.id}
          className="flex items-center justify-between rounded-lg border p-4"
        >
          <div>
            <p className="font-medium">{organization.name}</p>
            {organization.slug ? (
              <p className="text-sm text-muted-foreground">{organization.slug}</p>
            ) : null}
          </div>
          <PrimaryButton
            isPending={isPending && variables === organization.id}
            pendingLabel="Opening..."
            disabled={isPending}
            onClick={() => mutate(organization.id)}
          >
            Continue
          </PrimaryButton>
        </div>
      ))}
    </div>
  );
}
