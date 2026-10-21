import type { User } from "@/types/user";

export type ApiKey = {
  id: string;
  name: string | null;
  start: string | null;
  prefix: string | null;
  enabled: boolean | null;
  expiresAt: string | null;
  lastRequest: string | null;
  createdAt: string;
  user: User | null;
};

export type CreatedApiKey = ApiKey & {
  key: string;
};
