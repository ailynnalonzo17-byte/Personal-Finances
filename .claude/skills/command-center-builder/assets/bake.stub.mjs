#!/usr/bin/env node
/*
 * Command Center — STUB baker, used only during the pre-work (Phase P).
 *
 * Why this exists: the Cloudflare build command and the two-hour GitHub refresh job both run
 * `node command-center/bake.mjs`. In the pre-work there is no real baker yet, but the import,
 * the first build, the login gate and the refresh job all need SOMETHING at that path that
 * exits 0. This is it. It writes a tiny data.json next to the holding page so the page can
 * show "Last refreshed", which is the live proof that both keys and the two-hour job work.
 *
 * In the session, Vera replaces this file with the real bake.mjs (same path, same name), so
 * nothing in Cloudflare or in the refresh job has to change.
 *
 * It deliberately does NOT read Airtable. The token is checked only for presence, so a missing
 * secret is caught in the pre-work rather than on session day.
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "public");
mkdirSync(outDir, { recursive: true });

const tokenPresent = Boolean(process.env.AIRTABLE_TOKEN && process.env.AIRTABLE_TOKEN.startsWith("pat"));

const out = {
  status: "pending",
  refreshedAt: new Date().toISOString(),
  airtableTokenPresent: tokenPresent,
};
writeFileSync(join(outDir, "data.json"), JSON.stringify(out, null, 2));
console.log(`holding page data.json written (${out.refreshedAt}); AIRTABLE_TOKEN ${tokenPresent ? "present" : "MISSING"}`);
if (!tokenPresent) {
  // Do not fail the build: the holding page must deploy either way. The page reads this flag
  // and Vera reads it in the warm-up prep check.
  console.warn("AIRTABLE_TOKEN is not set for this build. The real page will need it. Add it under Settings → Builds → Variables and secrets (Cloudflare) or Actions secrets (GitHub).");
}
