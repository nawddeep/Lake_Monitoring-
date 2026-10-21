import { serve } from "inngest/next";
import { inngest } from "@/inngest/client";

// Inngest authenticates execution requests using INNGEST_SIGNING_KEY in cloud mode.
export const { GET, POST, PUT } = serve({
  client: inngest,
  functions: [],
});
