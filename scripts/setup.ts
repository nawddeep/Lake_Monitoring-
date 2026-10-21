import { cancel, confirm, intro, isCancel, log, note, outro } from "@clack/prompts";
import { spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import { constants, copyFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import process from "node:process";

class SetupError extends Error {}

function run(command: string, arguments_: string[], message: string) {
  log.step(message);

  const result = spawnSync(command, arguments_, {
    cwd: process.cwd(),
    stdio: "inherit",
  });

  if (result.error) {
    throw new SetupError(`Could not run ${command}: ${result.error.message}`);
  }

  if (result.status !== 0) {
    throw new SetupError(`Command failed: ${command} ${arguments_.join(" ")}`);
  }
}

function commandSucceeds(command: string, arguments_: string[]) {
  const result = spawnSync(command, arguments_, {
    cwd: process.cwd(),
    stdio: "ignore",
  });

  return !result.error && result.status === 0;
}

function checkDocker() {
  if (!commandSucceeds("docker", ["--version"])) {
    throw new SetupError("Docker is not installed or is not available on your PATH.");
  }

  if (!commandSucceeds("docker", ["compose", "version"])) {
    throw new SetupError("Docker Compose is not installed or is not available.");
  }

  if (!commandSucceeds("docker", ["info"])) {
    throw new SetupError("Docker is installed but is not running. Start Docker and try again.");
  }
}

function createEnvironmentFile() {
  const environmentPath = resolve(process.cwd(), ".env");
  const exampleEnvironmentPath = resolve(process.cwd(), ".env.example");

  if (existsSync(environmentPath)) {
    log.info("Keeping the existing .env file.");
    return;
  }

  if (!existsSync(exampleEnvironmentPath)) {
    throw new SetupError("Could not find .env.example.");
  }

  copyFileSync(exampleEnvironmentPath, environmentPath, constants.COPYFILE_EXCL);
  log.success("Created .env from .env.example.");
}

function ensureBetterAuthSecret() {
  const environmentPath = resolve(process.cwd(), ".env");
  const environmentContents = readFileSync(environmentPath, "utf8");
  const secretMatch = environmentContents.match(/^BETTER_AUTH_SECRET=(.*)$/m);
  const configuredSecret = secretMatch?.[1].trim().replace(/^(['"])(.*)\1$/, "$2");

  if (configuredSecret) {
    log.info("Keeping the existing Better Auth secret.");
    return;
  }

  const generatedSecret = randomBytes(32).toString("base64url");
  const secretLine = `BETTER_AUTH_SECRET=${generatedSecret}`;
  let updatedEnvironmentContents: string;

  if (secretMatch) {
    updatedEnvironmentContents = environmentContents.replace(
      /^BETTER_AUTH_SECRET=.*$/m,
      secretLine,
    );
  } else {
    const separator = environmentContents.endsWith("\n") ? "" : "\n";
    updatedEnvironmentContents = `${environmentContents}${separator}${secretLine}\n`;
  }

  writeFileSync(environmentPath, updatedEnvironmentContents, { encoding: "utf8", mode: 0o600 });
  log.success("Generated a local Better Auth secret.");
}

async function waitForPostgres() {
  log.step("Waiting for PostgreSQL to accept connections...");

  for (let attempt = 0; attempt < 30; attempt += 1) {
    if (
      commandSucceeds("docker", [
        "compose",
        "exec",
        "-T",
        "db",
        "pg_isready",
        "-U",
        "lake",
        "-d",
        "lake_monitoring",
      ])
    ) {
      log.success("PostgreSQL is ready.");
      return;
    }

    await new Promise((resolvePromise) => setTimeout(resolvePromise, 1_000));
  }

  throw new SetupError("PostgreSQL did not become ready within 30 seconds.");
}

async function main() {
  intro("Set up your application");

  note("Checking Docker and preparing local configuration.", "Environment");
  checkDocker();
  createEnvironmentFile();
  ensureBetterAuthSecret();

  note("Starting PostgreSQL and applying the Prisma schema.", "Database");
  run("docker", ["compose", "up", "-d"], "Starting PostgreSQL...");
  await waitForPostgres();
  run("npx", ["prisma", "migrate", "dev"], "Applying database migrations...");

  note("Creating the first admin and optional demo records.", "Application data");
  run("npm", ["run", "admin:create"], "Creating an admin account...");

  const shouldSeedDemoData = await confirm({
    message: "Seed demo data? (fake organizations and users, for local testing only)",
    initialValue: false,
  });

  if (isCancel(shouldSeedDemoData)) {
    cancel("Setup cancelled.");
    process.exitCode = 1;
    return;
  }

  if (shouldSeedDemoData) {
    run("npm", ["run", "seed"], "Seeding demo data...");
  }

  outro("Setup complete. Run `npm run dev` to start the development server.");
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : "Unexpected setup error.";
  cancel(message);
  process.exitCode = 1;
});
