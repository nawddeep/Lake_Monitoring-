# Lake Monitoring Web

Web app for the lake monitoring platform. Built on the
[SaaS Foundation](https://saasfoundation.dev) starter (MIT): Next.js, Prisma, PostgreSQL and
Better Auth, with organizations, members, invitations, roles, and separate admin and customer
portals. Template docs: [docs.saasfoundation.dev](https://docs.saasfoundation.dev).

The lake data tables (sites, stations, sensors, sensor installations, parameters, readings,
calibrations, samples, alerts) are linked to the template's users and organizations. The
`bridge/` folder receives readings from the ESP sensor boards.

## Quick start (Docker only)

Needs only [Docker Desktop](https://docs.docker.com/get-docker/), running. No Node.js, no `.env`.

```bash
git clone https://github.com/nawddeep/Lake_Monitoring-.git lake-monitoring-web
cd lake-monitoring-web && docker compose up
```

Open http://localhost:3000. The first start takes a minute or two (it installs dependencies inside
the container). `docker compose up` starts PostgreSQL 18, applies all migrations to it and runs the
app. **Everything uses the local PostgreSQL in Docker**, never the shared Supabase database.

Create your login (asks for name, email and password):

```bash
docker compose exec app npm run admin:create
```

Optional:

- Sensor bridge on port 5000: `docker compose --profile bridge up`
  (macOS uses port 5000 for AirPlay: `BRIDGE_PORT=5001 docker compose --profile bridge up`)
- Change settings: `cp .env.example .env` and edit. `.env.example` lists every variable.
- Stop: `docker compose down` (data is kept). Wipe the local database: `docker compose down -v`.

## Without Docker for the app (Node.js on your machine)

Prerequisites:

- Node.js 24 (see `.nvmrc`; with nvm run `nvm use`)
- npm (comes with Node.js)
- [Docker Desktop](https://docs.docker.com/get-docker/), running (for PostgreSQL)

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

   This creates `.env` from `.env.example` if it doesn't exist (it points at the local
   PostgreSQL), generates `BETTER_AUTH_SECRET`, starts PostgreSQL in Docker, applies the
   migrations and asks for the admin's name, email and password. Demo data is optional and off by
   default; it is fake data for local testing only.

4. Start the development server and open http://localhost:3000:

   ```bash
   npm run dev
   ```

## Shared database (Supabase)

The team's shared database is PostgreSQL on Supabase (Singapore region). The app connects to it
directly through Prisma; Supabase Auth, Storage and the Supabase JS client are not used.

1. Ask the project owner for the connection string (session pooler, port 5432). It contains the
   database password, so it is shared privately, never committed.
2. In `.env`, set both lines to that string:

   ```dotenv
   DATABASE_URL="postgresql://postgres.<project-ref>:<password>@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
   DIRECT_URL="postgresql://postgres.<project-ref>:<password>@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
   ```

3. Run `npm run dev`. Do not run `npm run app:setup` against the shared database.

Rules for the shared database:

- Apply migrations with `npx prisma migrate deploy` only. Never run `prisma migrate reset` or
  `prisma migrate dev` against it: `reset` deletes all data.
- Every table in `public` must have row-level security enabled (see the
  `enable_row_level_security` migration). Supabase's public Data API roles can otherwise read
  tables directly. New migrations that create tables must enable RLS on them too.
- Use the session pooler string, not the direct `db.<project-ref>.supabase.co` one: the direct
  host is IPv6-only and fails on many networks.

To work against the local Docker database instead, point `DATABASE_URL` back at
`postgresql://lake:<password>@localhost:5432/lake_monitoring` and remove `DIRECT_URL`.

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
