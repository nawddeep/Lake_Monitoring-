# Lake Monitoring Web

Web app for the lake monitoring platform. Built on the
[SaaS Foundation](https://saasfoundation.dev) starter (MIT): Next.js, Prisma, PostgreSQL and
Better Auth, with organizations, members, invitations, roles, and separate admin and customer
portals. Template docs: [docs.saasfoundation.dev](https://docs.saasfoundation.dev).

This branch is the foundation only. The lake data tables (sites, stations, sensors, readings,
calibrations, samples, alerts) are added in a later step, linked to the template's users and
organizations.

## Prerequisites

- Node.js 24 (see `.nvmrc`; with nvm run `nvm use`)
- npm (comes with Node.js)
- [Docker Desktop](https://docs.docker.com/get-docker/), running

## Getting Started

1. Clone the repo:

   ```bash
   git clone https://github.com/nawddeep/Lake_Monitoring-.git lake-monitoring-web
   cd lake-monitoring-web
   ```

2. Install dependencies (exact versions from `package-lock.json`):

   ```bash
   npm ci
   ```

3. Set up the environment, auth secret, database and the first admin account:

   ```bash
   npm run app:setup
   ```

   This creates `.env` from `.env.example` if it doesn't exist, generates `BETTER_AUTH_SECRET`,
   starts PostgreSQL in Docker, applies the migrations and asks for the admin's name, email and
   password. Demo data is optional and off by default; it is fake data for local testing only.

4. Start the development server and open http://localhost:3000:

   ```bash
   npm run dev
   ```

## Checks

CI (`.github/workflows/ci.yml`) runs on every pull request and push to `main`: install, Prisma
version check, schema validation, lint, type-check, migrations against a fresh PostgreSQL 18,
a check that `prisma/schema.prisma` has no changes missing a migration, and the production build.
Run the same locally with:

```bash
npm run lint && npm run typecheck && npm run build
```

## Background Jobs

Inngest is configured in `src/inngest/client.ts` and served at `/api/inngest`.
Register background functions in the route handler's `functions` array when adding jobs.

For local development, set `INNGEST_DEV=1` in `.env`, run `npm run dev`, and start the Inngest
Dev Server in another terminal:

```bash
npx inngest-cli@latest dev -u http://localhost:3000/api/inngest
```

Open http://localhost:8288 to inspect functions and runs. No cloud keys are required locally.

For Inngest Cloud, set `INNGEST_EVENT_KEY` and `INNGEST_SIGNING_KEY` in your
deployment environment and sync `/api/inngest` in Inngest. Leave `INNGEST_DEV`
unset or set it to `0` in production.

## Email

Invitation emails are off by default (`INVITATION_EMAIL_ENABLED=false`): invitations are
created with an email status of `not_sent` and you share the link yourself.

To send invitation and account emails, configure the following values in `.env`:

1. Create an account with [Resend](https://resend.com), generate an API key, and add it:

   ```dotenv
   RESEND_API_KEY=re_...
   ```

2. Verify your sending domain in Resend, then set the sender address:

   ```dotenv
   EMAIL_FROM="notifications@your-domain.com"
   ```

3. Set `INVITATION_EMAIL_ENABLED=true`.

Password reset emails are unaffected by `INVITATION_EMAIL_ENABLED`. Restart the development
server after changing environment variables.

## License

The SaaS Foundation template is MIT licensed; see `LICENSE`.
