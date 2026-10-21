import type { Organization } from "@/types/organization";
import type { User } from "@/types/user";

export type Member = {
  id: string;
  role: string;
  platformRole: string | null;
  user: User;
  organizations?: Organization[];
  createdAt: string;
};
