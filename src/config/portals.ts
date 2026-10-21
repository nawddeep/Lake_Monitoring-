export const Portal = {
  admin: "admin",
  customer: "customer",
} as const;

export type PortalValue = (typeof Portal)[keyof typeof Portal];
