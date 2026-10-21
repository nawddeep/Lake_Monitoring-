## Prisma Naming Conventions

- Define Prisma model fields and relations in camelCase so the generated TypeScript client stays ergonomic.
- Add `@map("snake_case")` to every field that persists to the database, and keep `@@map("snake_case")` on models when the table name is snake_case.
- When adding indexes or foreign keys, remember to refer to the Prisma field names (camelCase); Prisma will translate them via the existing `@map` metadata.
- Double-check new migrations to ensure column names remain snake_case and that there are no missing `@map` annotations.
- If an external generator rewrites `schema.prisma`, reapply these mappings before creating migrations.
