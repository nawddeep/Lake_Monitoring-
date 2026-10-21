## Route Groups Overview

- `src/app/(auth)`: public auth surfaces (login, register). Layout should never rely on an authenticated session.
  Redirects go to `/dashboard` after sign-in.
- `src/app/(admin)/admin`: authenticated experience. Layout fetches the Better Auth session via `fetchSession()` and
  redirects to `/login` when `session.session` is missing. Add new protected pages (e.g., `/dashboard`) inside this
  folder.
- `src/app/page.tsx`: root redirect to `/login`. Adjust if you introduce a marketing homepage.

## Session Helpers

- Use `fetchSession()` (server) and `authClient.useSession()` or `authClient.getSession()` (client) to obtain the
  signed-in user. They already map Better Auth’s `{ session, user }` structure.
- When guarding pages, check `session?.session` rather than the old `.data` shape.

## Common Pitfalls

- Keep imports using the `@/` alias; baseUrl/paths are set for the repo root.

## Frontend Mutations

All frontend mutations must use API routes. Do not use Next.js Server Actions.

All requests to the backend must go through an API service in `src/lib/api/`. Never call `fetch` directly in
components — use the appropriate API service method instead.

API services are scoped by portal and loosely structured by entity:

- `src/services/api/client.ts` — base `ApiClient` class with `get`, `post`, `patch`, `put`, `delete` methods. Throws
  `ApiError` on non-2xx responses.
- `src/services/api/admin/` — admin portal API services (e.g. `invitationsApi`, `organizationsApi`)

## API Structure

The API is scoped per portal, mirroring the app folder structure:

- `src/app/api/admin/` — admin portal endpoints
- `src/app/api/customer/` — customer portal endpoints

## Route Handler Pattern

Every route handler must follow this pattern:

1. **Auth guard** — wrap the handler with the appropriate portal middleware (e.g. `withAdmin`)
2. **Validator** — each route has its own `validator.ts` co-located in the same folder. The validator handles:
   - Syntactic validation (Zod schema)
   - Referential checks (e.g. record exists)
   - Business rule checks (e.g. no duplicate pending invitations)
3. **Service or repository** — if validation passes, call a service or repository to execute the business logic
4. **Response** — return a response using the shared helpers from `@/app/api/response.ts`

### Example structure

```
src/app/api/admin/organizations/[id]/invitations/
  route.ts      ← thin handler: auth guard, validate, call service, respond
  validator.ts  ← all validation logic for this endpoint
```

### Example handler

```ts
export const POST = withAdmin(async (request, { params }, { session }) => {
  const { id: organizationId } = await params;
  const body = await request.json();

  const validator = new MyValidator(organizationId, body);
  const isValid = await validator.validate();
  if (!isValid) return validationErrorResponse(validator.errors);

  await myService({ ...validator.data, inviterId: session.user.id });

  return createdResponse("Done.");
});
```

## Data Access

All Prisma queries must go through a repository. Route handlers, validators, and services must never import `prisma`
directly — always call a repository function instead.

## Data Tables

Always use the reusable `DataTable` component for tabular data — never build a raw `<table>` from scratch.

- `src/components/data-table/data-table.tsx` — generic `<DataTable columns={} data={} emptyMessage={} />`. Handles
  server-side sorting via URL params (`?sort=&order=`) and client-side pagination automatically.
- `src/components/data-table/data-table-column-header.tsx` — use `<DataTableColumnHeader column={column} title="..." />`
  in column definitions to make a column sortable.
- `src/components/data-table/data-table-pagination.tsx` — included automatically by `DataTable`, no need to add it
  manually.

### Column file convention

Co-locate a `columns.tsx` file next to the page that uses it:

```
app/(admin)/admin/team/users/
  columns.tsx      ← "use client" — ColumnDef[] for this domain, uses DataTableColumnHeader
  page.tsx         ← server component — fetches data, passes to <DataTable>
```

- `columns.tsx` must be a client component (`"use client"`).
- Export the row type by inferring from the repository function:
  `type AdminUser = Awaited<ReturnType<typeof listAdminUsers>>[number]`
- Columns with nested/computed data (e.g. arrays) should set `enableSorting: false`.

### Server-side sorting

When a repository needs to support sorting, accept `params?: { sort?: string; order?: string }`, validate the sort field
against an allowlist, and pass it to Prisma's `orderBy`. See `adminOrganizationRepository.ts` for the pattern.

## Shared Utilities

- `src/app/api/response.ts` — response helpers (`validationErrorResponse`, `notFoundResponse`, `conflictResponse`,
  `createdResponse`) and shared response types
- `src/app/api/admin/with-admin.ts` — auth + admin portal guard
- `src/validators/BaseValidator.ts` — base class for all validators
