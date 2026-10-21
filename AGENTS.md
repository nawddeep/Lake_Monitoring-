<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

## Application Overview

- Built on Next.js (custom fork behavior noted above) with Prisma for data access.
- Better Auth provides authentication; its generated Prisma models manage users, sessions, and related entities.
- React Hook Form handles form state; Zod schemas validate inputs on both client and server.
- ShadCN supplies reusable UI primitives.

## Verification

- Do not run production builds (for example, `npm run build` or `next build`). The developer will handle builds separately.

## Conventions

- Use the `@/…` path alias for imports (supports files in `src` and project-level scripts). The alias resolves to the `src` directory via `baseUrl`/`paths` in `tsconfig.json`—prefer it over deep relative paths.
- Prefer using full names for variable names, e.g organizationId instead of orgId.

## Project Structure

### `src/services/api/` — Frontend API client layer

Scoped by portal or authentication context (e.g. `src/services/api/admin/` and `src/services/api/auth/`). Each domain has an `*Api.ts` file that exports a typed object calling `apiClient` from `src/services/api/client.ts`. Infer request types from colocated route schemas when possible and use shared application types for response DTOs. The API client returns typed promises; all frontend requests flow through these service files—never call `fetch` directly from components.

### `src/app/api/` — Route handlers (server)

Route handlers are organized to mirror the frontend API paths (e.g. `src/app/api/admin/users/route.ts`). All admin routes are wrapped with `withAdmin()` (from `src/app/api/admin/with-admin.ts`), which handles session and portal auth. `withAdmin` composes `withErrorHandler` so `ZodError` thrown anywhere in the handler is automatically returned as a 400.

Query param parsing uses `parseQuery(request, schema)` from `src/lib/api.ts` instead of manually constructing `URLSearchParams`.

### `src/app/api/admin/*/schema.ts` — Shared Zod schemas

Schemas live alongside their route handler and are imported by both the route (for server-side validation) and the frontend API service (for type inference). This is the single source of truth for input shapes.

### `src/serializers/` — Data transformation

Each domain has a `*Serializer.ts` file that maps Prisma entities to API DTOs (e.g. `serializeUser`, `serializeApiKey`). Serializers handle date serialization (`Date` → ISO string), field renaming, and computed relations. Route handlers never return raw Prisma objects.

### `src/repositories/` — Data access

Repository functions wrap Prisma queries. They accept loosely-typed params (e.g. `sort?: string`, `order?: SortOrder`) since validation happens upstream in the schema layer. Shared types (e.g. `SortOrder`) live in `src/repositories/types.ts`.

Keep admin and customer repositories separate, even when some queries currently look identical. This is an intentional portal trust boundary:

- Customer portal code uses customer repositories. Customer queries are tenant-scoped and generally require an organization ID where organization-owned data is accessed.
- Admin portal code uses admin repositories. Admin queries may operate platform-wide without implicit organization scoping.
- Do not deduplicate functions across these repository namespaces merely because their present Prisma queries match. Preserve the boundary to prevent admin-level data access from leaking into customer code.

### Server-side validation and pre-checks

Use colocated Zod schemas directly for request shape validation. Keep database-backed existence checks, authorization, and business-rule pre-checks in the route handler by default. Extract them into a dedicated validator or service only when the logic is sufficiently complex or reused; extending `BaseValidator<T>` is available but not mandatory.

### Better Auth backend calls

Better Auth skills are general reference material for server APIs, plugins, sessions, organizations, and security. Their client-side examples do not define this application's architecture. Do not call Better Auth client APIs directly from components. Frontend authentication and organization requests must flow through `src/services/api/` and application route handlers; route handlers may call Better Auth server APIs after completing the application's validation and authorization checks. These project conventions take precedence over conflicting suggestions in installed skills.

Before calling a Better Auth server API, perform all applicable checks in application code. Validate the request shape and pre-check records, ownership, membership, permissions, and other business constraints so only valid, authorized data is passed to Better Auth.

Do not wrap a Better Auth server API call in `try/catch` merely to translate errors that the route should have prevented through these checks. After validation and authorization succeed, call Better Auth directly. If it still throws unexpectedly, allow the error to bubble to the global error handler and become a 500 response. Catch an error only when the application has a deliberate recovery path that cannot be handled through pre-checks.

### Request lifecycle

```
Component → *Api.ts (apiClient) → route.ts (withAdmin → withErrorHandler)
  → parseQuery/body.parse → pre-checks → Repository → Serializer → Response
```

## Forms

All forms use React Hook Form with Zod validation and ShadCN form primitives. This is the standard pattern — do not use raw `<label>`/`<input>` pairs or manual error rendering.

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { MutationError } from "@/components/feedback/mutation-error";
import { PrimaryButton } from "@/components/buttons/primary-button";

const form = useForm<FormValues>({ resolver: zodResolver(schema), defaultValues: { ... } });

const { mutate, isPending, isSuccess, isError, error } = useMutation({ mutationFn: ... });

<Form {...form}>
  <form onSubmit={form.handleSubmit((values) => mutate(values))}>
    <FormField
      control={form.control}
      name="fieldName"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Label</FormLabel>
          <FormControl><Input {...field} /></FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
    <MutationError isError={isError} error={error} fallback="Something went wrong." />
    <PrimaryButton type="submit" isPending={isPending} pendingLabel="Saving...">
      Submit
    </PrimaryButton>
  </form>
</Form>
```

- `<Form>` is RHF's `FormProvider` — it provides context to `FormField`, renders no DOM element
- `<FormMessage />` handles field-level validation errors automatically
- `<MutationError>` handles API-level errors; it surfaces `ApiError` detail messages or falls back to the `fallback` string
- `<PrimaryButton isPending>` handles loading state on the submit button
- For success feedback, render a message conditionally on `isSuccess` next to the button

## Skills

Custom skills for this project live in `.agents/skills/`. Always check this directory for relevant skills before implementing auth, organization, or security features. Available skills:

- **better-auth-best-practices** — Configure Better Auth server/client, database adapters, sessions, plugins
- **better-auth-security-best-practices** — Rate limiting, CSRF, secrets, session security, audit logging
- **create-auth-skill** — Scaffold full authentication (login, sign-up, OAuth) with Better Auth
- **email-and-password-best-practices** — Email verification, password reset, password policies, hashing
- **organization-best-practices** — Multi-tenant orgs, members, invitations, RBAC, Better Auth org plugin
- **two-factor-authentication-best-practices** — TOTP, OTP via email/SMS, backup codes, trusted devices
