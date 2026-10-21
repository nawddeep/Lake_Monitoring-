export type Invitation = {
  id: string;
  email: string;
  role: string;
  portal: string;
  status: string;
  emailStatus: "not_sent" | "sent" | "failed" | null;
  invitationUrl: string;
  createdAt: string;
  expiresAt: string;
};
