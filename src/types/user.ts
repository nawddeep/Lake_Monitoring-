export type User = {
  id: string;
  name: string;
  firstName: string;
  lastName: string;
  email: string;
  emailVerified: boolean;
  image: string | null;
  role: string | null;
  banned: boolean | null;
  banReason: string | null;
  banExpires: string | null;
  createdAt: string;
  updatedAt: string;
};

export type UserAccess = "admin_only" | "customer_only" | "both" | "none";

export type UserWithAccess = User & {
  access: UserAccess;
};
