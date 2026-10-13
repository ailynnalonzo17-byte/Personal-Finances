# Writing back from the page — PARKED DESIGN NOTE

**Status: PARKED, 09-12-2026. Nothing here has been built or tested.** This is the shape agreed
with Stephanie so that whoever builds it does not work it out from scratch. Treat every claim below
as a design intention, not as verified behaviour, and prove each one as you build.

**The ask that started it (Stephanie, 09-12-2026):** "if we want to later add things like journal
sections or gratitude daily captures." Anything the person types ON the page and expects to still be
there tomorrow: a journal entry, a daily gratitude line, a note against a task, a checkbox they tick,
a metric they type in by hand because no system holds it.

---

## Why the page cannot do this today, and why a bigger token would not help

The Command Center is **static assets only**. `wrangler.jsonc` has no `main`, so there is no program
running at the address. The two jobs that touch it (the Cloudflare build on push, the GitHub Action
every two hours) both run on a schedule, hours before anyone opens the page, and then stop.

So there is nothing to receive what a person types. **This is not a permissions problem**, and
widening the Airtable token achieves nothing on its own — the page has no way to use it.

**And the obvious shortcut is the wrong answer.** Putting a write-capable token into the page's own
JavaScript would work, and it would also ship that token to every browser that loads the page, where
anyone can read it out. Two reasons that is not acceptable here:

1. **`data.records:write` can DELETE records, not only add them.** On the owner's operating base
   that is their tenants, their leases and their money.
2. **Read-only is the entire reason the pre-work token is safe to paste into a Vera chat** (golden
   rule 1, Stephanie 09-09-2026). Make that same token write-capable and the rule stops being true,
   and the pre-work page and the line-up prompt both have to be rewritten to say so.

---

## The shape to build

**One Cloudflare Worker, same address, gains a program alongside its assets.**

1. **`wrangler.jsonc` gains a `main`** pointing at a small Worker script, keeping the existing
   `assets` block. The assets binding serves the page; the script handles the routes the assets do
   not. This is Cloudflare's documented static-assets-plus-script setup and is meant to be an
   additive change rather than a rebuild — **prove that before promising it to anyone.**
2. **The script exposes one route**, e.g. `POST /api/entry` to save and `GET /api/entry` to read
   back the recent ones.
3. **The write token is a Worker secret** (`wrangler secret put`), so it lives on Cloudflare's side
   and is never sent to a browser, never committed, never pasted into a chat.
4. **The page calls its own address.** No cross-origin anything, no token in the page.

**Authentication comes free from Access.** The Worker is already behind Cloudflare Access with
"All traffic" scope, so a request that reaches the script has already passed the login gate. Do not
build a second login. If finer detail is wanted later, Access puts the signed-in identity in the
`Cf-Access-Jwt-Assertion` header — **unverified here.**

---

## The second token

**A separate Airtable token, created when this is built, not during the pre-work.** Per the vera
manual's key rules (v4.48): one key, one user of it; two things needing the same service get two
separate keys.

| | Read token (exists today) | Write token (later) |
|---|---|---|
| Scope | `data.records:read` | `data.records:read` + `data.records:write`, **one base** |
| Lives in | GitHub Actions secret, Cloudflare build variable | Cloudflare **Worker secret**, nothing else |
| Safe to paste in chat | Yes | **No, never** |
| Rotating it breaks | the numbers on the page | the journal only |

Scope the write token to the single base, and if Airtable ever allows narrowing to one table, do
that instead — the journal has no business being able to write to the tenants table.

---

## Where entries should land

**Recommendation: a table in their Airtable.** It is already the hub, Vera reads it, the morning
briefing can reflect on what they wrote, and it shows up in their own base where they can see it.

**The alternative considered and not chosen: committing entries as files to the memory vault.** The
morning routine already commits to the repo, so the path exists. Rejected as the default because a
write to git needs a GitHub token with contents write, which is a much broader key than an
Airtable one scoped to a base, and because entries in a repo are harder for the owner to look at
than rows in their own table. Revisit if the entries are genuinely documents rather than rows.

---

## The freshness trap, and it is the one that will bite

The page's numbers come from `data.json`, baked at most every two hours. **An entry typed at 10:05
would not appear on the page until the next bake**, which reads as the journal having eaten it. That
is the failure that makes someone stop trusting the page.

So the journal panel must **read its entries live from the Worker route**, not from `data.json`.
Entries are the one thing on the page that cannot come from the two-hour cycle. Write the panel so
it renders what the route returns, and shows what was just typed immediately.

---

## What is NOT known and must be settled by building it

- Whether adding `main` to an existing assets-only Worker deploys cleanly without disturbing the
  Access policy, the build watch path, or the GitHub Action.
- Whether the free Workers plan's request limits matter here. Almost certainly not at one person
  writing a line a day, but nobody has checked.
- Whether `wrangler secret put` works against a Worker whose builds come from the GitHub
  integration, or whether the secret has to be set in the dashboard instead.
- What the page should do when the route fails: the entry must not vanish silently. At minimum keep
  the text in the box and say plainly that it did not save.
- Whether this is offered to every student or stays an advanced extension. It adds a token, a
  secret and a code path to a build that is currently a static page, and the whole design of the
  pre-work is that a student pastes nothing but one read-only key.

---

## Before building this, re-read

- `references/architecture.md` — why the page is static in the first place.
- `references/cloudflare.md` — the Access policy and the build watch path, both of which this
  touches.
- The vera manual on API keys (v4.48): one key one user, never paste a key into a script, and check
  what a script SENDS rather than only where it stores things.
