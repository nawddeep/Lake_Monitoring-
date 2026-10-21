import assert from "node:assert/strict";
import { test } from "node:test";
import { attemptInvitationEmail } from "@/lib/email/invitation-delivery";

test("invitation email delivery handles missing configuration, success, and provider failure", async () => {
  const previousApiKey = process.env.RESEND_API_KEY;
  const previousEmailEnabled = process.env.INVITATION_EMAIL_ENABLED;
  const previousConsoleError = console.error;
  try {
    delete process.env.INVITATION_EMAIL_ENABLED;
    delete process.env.RESEND_API_KEY;
    let attempted = false;
    assert.equal(
      await attemptInvitationEmail(async () => {
        attempted = true;
      }),
      "not_sent",
    );
    assert.equal(attempted, false);

    process.env.RESEND_API_KEY = "test-key";
    assert.equal(
      await attemptInvitationEmail(async () => {
        attempted = true;
      }),
      "sent",
    );
    assert.equal(attempted, true);

    process.env.INVITATION_EMAIL_ENABLED = "false";
    attempted = false;
    assert.equal(
      await attemptInvitationEmail(async () => {
        attempted = true;
      }),
      "not_sent",
    );
    assert.equal(attempted, false);

    process.env.INVITATION_EMAIL_ENABLED = "true";
    assert.equal(
      await attemptInvitationEmail(async () => {
        attempted = true;
      }),
      "sent",
    );
    assert.equal(attempted, true);

    const loggedErrors: unknown[][] = [];
    console.error = (...arguments_) => {
      loggedErrors.push(arguments_);
    };
    assert.equal(
      await attemptInvitationEmail(async () => {
        throw new Error("Provider rejected email");
      }),
      "failed",
    );
    assert.equal(loggedErrors.length, 1);
  } finally {
    if (previousEmailEnabled === undefined) delete process.env.INVITATION_EMAIL_ENABLED;
    else process.env.INVITATION_EMAIL_ENABLED = previousEmailEnabled;
    if (previousApiKey === undefined) delete process.env.RESEND_API_KEY;
    else process.env.RESEND_API_KEY = previousApiKey;
    console.error = previousConsoleError;
  }
});
