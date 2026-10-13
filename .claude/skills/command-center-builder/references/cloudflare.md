# Cloudflare — deploy, lock down, and schedule (click-by-click)

This is the exact flow that worked on the reference build (Sept 2026, the *new* unified
Workers UI). Cloudflare changes its UI; if a screen differs, the *principles* still hold —
build command → deploy command → variables → deploy → Access.

## Two halves: before the session (student alone) and in the session (you drive)

Everything in Cloudflare that needs the student's login, card, agreement or a secret value has
NO dependency on the dashboard existing, so it moves ahead of the build session (decision 35,
09-08-2026). The session then only imports and deploys. Rule of thumb for the in-session half: the read-only Airtable token is yours to handle (ask for
it in chat); a card, a password, a write-capable token or an agreement is still theirs. **Don't
screenshot while any secret is visible**, including the one you are pasting.

### Before the session — the student does these alone

These are the student's steps, written the way the Week 4 page writes them (Stephanie corrected the
wording from a real screen on 09-09-2026; keep to it). Vera's role here is ONLY the "stuck" helper:
the student pastes the stuck prompt (`assets/prep-prompt.md`) with the step number and a screenshot,
and Vera reads the screenshot and gives the next click. Vera does not narrate the steps unprompted.

**FOUR student steps, then Phase P as step 5 (Stephanie, 09-12-2026).** The old step 2, where the
student opened Cloudflare's Create an application screen purely to authorize GitHub and then backed
out without deploying, is DELETED. That authorization now happens inside Phase P, in Cloudflare's own
import flow, with Vera driving and the student clicking the GitHub popup. The back-out was the single
most confusing instruction in the pre-work and it left students staring at an empty Workers & Pages
list wondering what had failed.

One click per line, indented where a step has a sub-sequence, with where-on-the-screen cues, the
same words for the same thing every time ("memory vault" = their GitHub repository; say "aka your
GitHub repository" the first time and never again), and a "Done when" on every step. This mirrors
the Week 4 page's `CommandCenterPrepCard` (rewritten 09-11-2026 from the dry-run feedback: a student
could not follow paragraphs, "the same way you did in step 4" sent her back to step 4, and no step
said where on the screen to look). **Keep the two in step.**

**1. Create the Cloudflare account** (depends on nothing)
- Go to dash.cloudflare.com and choose Sign up.
- Use the email they check every day; it is also the login for the finished page.
- Confirm the verification email.
- Done when: they can sign in and see the Cloudflare dashboard.

**2. Turn on the login gate (Zero Trust)** (depends on nothing)
- From the Cloudflare dashboard, click Zero Trust in the left-hand menu, then Get Started (or
  one.dash.cloudflare.com if they closed it).
- Choose the Free plan.
- Checkout: billing address, credit card, terms. Expect no charge at this size.
- Done when: Zero Trust opens to its own dashboard instead of asking for a plan.

**3. Cloudflare API token → GitHub** (depends on nothing)
- Why (say it if asked): the every-two-hours clock lives in GitHub, next to the memory vault. A small
  job there wakes up, rebuilds the numbers and publishes to Cloudflare, and Cloudflare only accepts a
  publish from a key it issued. So the key is made in Cloudflare and handed to GitHub: GitHub gets
  permission to update the page.
- In Cloudflare, click the profile icon at the top right, then Profile.
- In the left-hand menu of the profile page, click API Tokens.
- Click the Create Token button. It is in the MIDDLE of the screen, not a corner (Stephanie, 09-12-2026).
- Find the template Edit Cloudflare Workers and click Use template.
- Scroll down to Account Resources; open the dropdown after Include; select their account.
  (Empty by default and the form lets them create a useless token. Fill it.)
- Under Zone Resources choose All zones.
- Continue to summary; it must list Workers Scripts: Edit. Click Create Token.
- Click the copy icon next to the token. Cloudflare shows it once.
- In a new tab, github.com, open the memory vault itself (its name shows at the top of the page),
  not the GitHub home page.
- Click the Settings tab in the row across the top of the vault's page (Code, Issues, Pull
  requests, ..., Settings). Not the Settings under the profile picture.
- In the left-hand menu: Secrets and variables, then Actions.
- Click the New repository secret button (top right).
- Paste the token into the Secret box FIRST, then type the name `CLOUDFLARE_API_TOKEN`, then Add
  secret. (Copying the name from the page overwrites the clipboard and loses the token.)
- Done when: the vault's Actions secrets page lists CLOUDFLARE_API_TOKEN.

**4. Read-only Airtable token → keep it reachable → GitHub** (depends on their Airtable)
- Why (say it if asked): the same GitHub job has to READ the numbers out of Airtable before it can
  publish them, so it needs an Airtable key in the same secrets list. Cloudflare needs a copy of the
  same key when it builds the page, but the Cloudflare app does not exist until the session import,
  so that copy cannot be placed in the pre-work: Vera asks for it in the session (golden rule 1).
  Vera cannot hold it between chats either (secrets do not live inside Claude). Saved copy OR a
  fresh token in the session, both fine, both free.
- In Airtable, click the account icon at the top right, then Builder hub.
- In the left-hand menu, click Personal access tokens.
- Click the Create token button (top right).
- Name: something like command-center-read.
- Access: add only their operating base. Not all bases.
- Scopes: add only `data.records:read`.
- Click Create token, then click the copy icon next to it. It starts with pat. Shown once.
- **Keep it reachable for step 5**, two blessed ways: leave the Airtable tab open (the token stays
  on screen, best when they do the whole pre-work in one sitting), or save it to a password manager
  or locked phone note. Losing it costs a minute; a fresh one is free.
- Then GitHub, spelled out again (never "the same as step 4"):
  - github.com, open the memory vault itself
  - the Settings tab in the row across the top of the vault's page
  - left-hand menu: Secrets and variables, then Actions
  - New repository secret button (top right)
  - paste the token into the Secret box FIRST, then type the name `AIRTABLE_TOKEN`, then Add
    secret
- Done when: the vault's Actions secrets page lists both AIRTABLE_TOKEN and CLOUDFLARE_API_TOKEN,
  and the token is saved in their password manager or locked note.
- **In the build session Vera ASKS for this token in chat and places it in Cloudflare herself**
  (golden rule 1, Stephanie 09-09-2026). It is fine to paste it to Vera. It is read-only, locked to
  one base, revocable in Airtable, and free to re-issue if lost. This replaces the old line "never
  into a chat with Vera", which contradicted rule 1 and made a student's Vera refuse the token on
  the 09-10 dry run.

**Traps to say out loud:** Account Resources is empty by default and the form lets you create a
useless token; a 404 on the GitHub secrets page means not signed into GitHub in that browser; the
GitHub Settings they need is the repository's tab, not the profile menu. The Week 4 page carries a
Loom video under each step; point a stuck student at the video before anything else.

### In the session — you drive, the student pastes one value

| Step (Phase P, or the session fallback) | Who | Why |
|---|---|---|
| Verify the prep (sign in works; Continue with GitHub shows the repo; Zero Trust is on; both Actions secrets exist) | **You** | two minutes; anything missing is done now from the table above |
| "Create application" → "Continue with GitHub" → select the repo | **You** | navigation |
| Fill project name, build command, deploy command, root directory | **You** | plain text fields |
| Add build variable `NODE_VERSION = 20` | **You** | not sensitive |
| Add the database token variable — the **name** | **You** | a field name |
| Ask the student in chat for the read-only Airtable token, paste the **value** yourself, click **Encrypt** | **You** | the one credential exception (09-09-2026): read-only, one base, re-issued free. Say in one line that it will sit in the chat history and can be revoked in Airtable. |
| Click **Deploy** | **Student** (or you, after confirming) | the irreversible click |
| Watch the build log, read errors, fix code | **You** | verification |
| Click **Visit**, confirm the page renders | **You** | verification |
| "Protect this Worker behind Access" → All traffic + Cloudflare account policy → Apply | **You** | configuration (Zero Trust already exists from the prep) |
| Verify the gate from a browser that's *not* logged in | **You** | verification |
| Settings → Builds → narrow the watch path to `command-center/*` | **You** | configuration |
| `gh workflow run` the refresh Action and watch it go green | **You** | proves the two secrets from the prep work |

**Since 2.5 (09-11-2026) the import, the token, the gate and the watch path all happen in the
PRE-WORK, as Phase P, because Vera pushes a holding page first so the first build cannot fail.** The
table above is what Phase P does; it also stays the fallback for a student who arrives without
having run step 6. See "Lining it up" below.

### Lining it up — Phase P (pre-work step 6, Vera drives, about ten minutes)

Trigger: the student pastes `assets/lineup-prompt.md` in a LOCAL Claude Code session on their own
computer with Cloudflare and GitHub signed in. A cloud or phone session cannot do this; say so and
stop. Order:

1. **Verify steps 1 to 4**: they can sign into Cloudflare; Zero Trust opens to its own dashboard;
   both `CLOUDFLARE_API_TOKEN` and `AIRTABLE_TOKEN` are in the memory vault's Actions secrets; and
   they can lay hands on the Airtable token itself (open tab or saved copy). Anything missing is
   done now from the bullets above, before anything else. **Do NOT check whether GitHub shows as
   connected in Cloudflare** — that is no longer a pre-work step; you do it yourself in step 3
   below, and the student clicks the GitHub popup when it appears.
2. **Put the skeleton in the memory vault**, in one commit, message "Command Center: holding page":
   - `command-center/public/index.html` ← `assets/holding-page.html` with every placeholder
     filled (name, business, palette if already known else the Lean Landlord defaults, built-at).
   - `command-center/bake.mjs` ← `assets/bake.stub.mjs`, unchanged. Same path the real baker takes
     in the session, so the build command never changes.
   - `wrangler.jsonc` at the repo root ← `assets/wrangler.jsonc` with `<PROJECT_NAME>` filled
     (use `command-center` unless it clashes).
   - `.github/workflows/refresh-data.yml` ← `assets/refresh-data.yml` with `<CLOUDFLARE_ACCOUNT_ID>`
     filled from the dashboard URL.
   - `.gitignore` line `command-center/public/data.json` (the stub writes it at build time).
   Push, and verify the commit is on GitHub before touching Cloudflare.
3. **Import and deploy** — section 1 below, exactly. **Workers only: never the "Continue to Pages" link, never a Pages project.** **The GitHub authorization happens HERE, not in
   the pre-work**: at "Connect to GitHub" a GitHub window opens and the student clicks through it
   (their account, Only select repositories, the memory vault, Install & Authorize). That is an OAuth
   grant, so it is theirs by golden rule 2 — tell them exactly what to click and wait. If GitHub is
   already connected from a previous attempt, the screen shows a green dot and there is no popup. Project name = the `wrangler.jsonc` name. Build
   command `node command-center/bake.mjs`. Variables: `NODE_VERSION` = 20, then ASK for the
   read-only Airtable token in chat and paste it as `AIRTABLE_TOKEN`, Encrypt. Deploy. The log's
   Building step prints "holding page data.json written ... AIRTABLE_TOKEN present"; "MISSING"
   means the variable did not save, fix it before going on.
4. **Visit.** The holding page renders with their name and "Last refreshed" a minute ago.
   **⛔ Check the address before anything else: it must end in `.workers.dev`.** If it ends in
   `.pages.dev`, the import went through Cloudflare's legacy Pages flow, which this build does not
   support (the refresh job deploys with `wrangler deploy` and a Workers Scripts:Edit token, so a
   Pages site can silently stop updating; inferred, not tested). Redo step 3 on Workers, delete the
   Pages project so only one address exists, and only then go on. Nothing in the vault changes.
   (09-15-2026 Week 4 session: a student arrived on pages.dev and nothing had caught it.)
5. **Lock it down** — section 2. Verify from a browser that is not logged in.
6. **Narrow the watch path** — section 3.
7. **Run the refresh job once**: GitHub → the vault → Actions tab → "Refresh Command Center" → Run
   workflow. Green means both secrets from steps 4 and 5 work. Reload the holding page: "Last
   refreshed" moves. That is the receipt the student could never get before.
8. **Hand off in their words**: the address (say it and paste it), log in with the Cloudflare email,
   save it to the phone's home screen, "in the session we build out your actual pages — your
   businesses, your numbers, your briefing — and this page becomes that, at this same address",
   and one plain line: ready, or exactly what is still missing.

   **⛔ DO NOT TELL THEM THE PHRASE THAT STARTS THE BUILD, OR ANY OTHER NEXT STEP TOWARD IT
   (Stephanie, 09-12-2026, from a real Phase P run).** A run ended with "NEXT: on session day, say
   'build my command center' — Vera runs the warm-up, asks her four intake questions, and the real
   page replaces the holding page at this same address." Every word of that is true, and it is
   exactly the wrong thing to say. **A student handed the trigger will use it**, alone, before the
   session, without Stephanie there to run the intake with them — and they arrive at the session
   with the thing the session exists to build already half-done, badly, and nothing left to teach.
   The pre-work's job is to end READY, not to end STARTED.
   - Say what the session produces, never how to start it. "In the session we will build out your
     actual pages" is the whole of it.
   - Do not name the skill, the warm-up, the intake questions, or the build prompt. Naming the
     steps is the same leak, one degree removed.
   - If they ask outright how it gets built, say it takes you and them working through it together
     and that it is what the session is for. Do not hand over the phrase, even on request.
   - This applies to the written hand-off, the run report, and any chat that follows it.

The token sits in the chat history; say so in one line when you ask for it, and that it is revocable
in Airtable. Nothing else of theirs is typed by Vera.

## Prerequisite: the files are on GitHub
Cloudflare builds from what is *on GitHub*, not the student's disk. Before connecting,
confirm the repo contains `wrangler.jsonc` (repo root), `command-center/bake.mjs`,
`command-center/public/index.html`, and the workflow. Push them yourself (your `gh` login
usually has the `workflow` scope that a note-syncing tool like Obsidian's git plugin lacks —
a `.github/workflows/*.yml` push fails without it). Commit **only** the command-center
files; don't sweep unrelated changes.

### ⛔ So the 403 moves the CLICKS, never the build (09-21-2026)

**No session ever needs to reach Cloudflare's API.** The deploy is a dashboard import of what is
already on GitHub, and pushing to GitHub is the one session-dependent step, which a cloud session
does well. So when a cloud session hits the 403 (see `gotchas.md`), what moves to the local session
is the Cloudflare clicks, nothing else.

- **Before sending the student anywhere, open GitHub and say what is already there.** Name the files
  that are pushed. Whatever is on GitHub is the hand-over; the local session picks up from it and
  rebuilds nothing.
- **The local session proves it can push before it touches anything** (`gotchas.md`, "Prove you can
  push BEFORE you build anything").
- **⛔ Never bounce a student between sessions.** It cost one student two days: the cloud session
  sent her local, the local session could not push to GitHub, and she went back and forth between
  them while her code sat on GitHub ready to import the whole time. One line saying which half
  happens where, then the next click.

## 1. Import the repo (Workers flow) — in Phase P (or in the session if step 6 was skipped)
1. dash.cloudflare.com → **Workers & Pages** (on a new account it is not in the left menu; use the
   top search box, type Workers, pick Workers & Pages) → **Create application**. (A tiny link at the
   bottom, "Need to use the legacy Pages workflow? Continue to Pages," still exists — don't
   use it; we build for Workers static assets.)
2. **Continue with GitHub** (a green dot means GitHub is already connected, which the prep
   guarantees — no OAuth handoff). Select the repo → **Next**.
3. **Set up your application:**
   - **Project name:** e.g. `command-center` (becomes `<name>.<subdomain>.workers.dev`).
     Match the `name` in `wrangler.jsonc`.
   - **Build command:** `node command-center/bake.mjs`
   - **Deploy command:** `npx wrangler deploy` (pre-filled; leave it)
   - **Root directory:** leave as repo root (the root `wrangler.jsonc` points assets at
     `./command-center/public`)
   - "Builds for non-production branches": fine either way.
4. **Advanced settings** → **API token: "Create new token"** (leave — Cloudflare auto-creates
   its own deploy token; this is *not* the student's secret).
5. **Variables** (still in Advanced settings): add
   - `NODE_VERSION` = `20` — you type both.
   - `<DATABASE_TOKEN_NAME>` (e.g. `AIRTABLE_TOKEN`) — you type the **name**; the student
     read-only Airtable token in chat, then YOU paste it into the value box and click **Encrypt**
     (stores it as a masked secret). No keyboard handoff.
   Adding both here means the *first* build succeeds instead of failing on a missing token.
6. **Deploy.** Build phases: Initializing → Cloning → Installing → Building → Deploying.
   "Building ✓" means the baker ran (its summary line appears in the log). Deploying runs
   `npx wrangler deploy` (it downloads wrangler; a minute or two). The log then prints the
   live URL. The log pane sometimes stops streaming — reload the page to refresh it.
7. **Visit** → the page should render with live numbers. Verify each tab.

### `wrangler.jsonc` (repo root) — see `assets/wrangler.jsonc`
```
{ "name": "<project-name>", "compatibility_date": "2025-09-01",
  "assets": { "directory": "./command-center/public" } }
```
No `main` — an assets-only Worker. Deploying it will warn that `workers_dev` and
`preview_urls` default to enabled; harmless.

## 2. Lock it down — Cloudflare Access (private login gate)
Zero Trust is already on from the prep. If the Worker's **Access** tab still says "Set up Zero
Trust for this account," the prep was skipped:
1. **Set up Zero Trust** → onboarding: team name, **Choose a plan → Free**, then a **checkout
   page** (billing address, payment card, Terms of Service, and an authorization to charge for
   usage *beyond* free limits). **This is the student's screen** — card, address, terms. Tell them
   plainly: for an Access gate with a handful of logins they stay well within free limits, but
   they *are* putting a card on file. (If they refuse the card, the fallback is HTTP Basic Auth
   coded into the Worker — real privacy, no Zero Trust. Offer it.)
2. On the Worker's **Access** tab → **Protect this Worker behind Access**:
   - **Scope: All traffic** (not "Previews only" — the default; switch it).
   - **Authentication policy → Add policy → "Cloudflare account"** ("Only members of this
     Cloudflare account can reach this Worker") — the simplest, tightest gate for a solo
     owner. Session 24h. **Apply Access.**
3. **Verify** by loading the URL in a browser that is *not* logged into the student's
   Cloudflare (the in-app preview browser works): it must redirect to a "Sign in ·
   Cloudflare Access" page. That's proof. Tell the student their login = their Cloudflare
   account (email + password); no new password was created.

## 3. Stop unrelated pushes from burning build minutes
Default **build watch path** is `*` — *every* push to the repo (including a note-sync
tool auto-pushing notes) triggers a rebuild and can exhaust free build minutes fast.
Settings → Builds → **Build watch paths → Include paths**: remove `*`, add
`command-center/*`, **Save**. Now only dashboard changes build.

## 4. The refresh Action needs a Cloudflare API token — normally done in the prep
If both Actions secrets already exist in the repo (the prep), skip to the last sentence. Otherwise:
Cloudflare → profile → **API Tokens → Create Token → "Edit Cloudflare Workers"** template.
You (Claude) can prepare the form: **Account Resources → Include → <the student's
account>** (it's *empty* by default and must be set), **Zone Resources → All zones** (the
template's Workers Routes permission wants a zone; leave "Specific zone" empty and it
may block), then **Continue to summary**. The summary must show **Workers Scripts:Edit**.
Then **hand off**: the student clicks **Create Token**, copies it (shown once), and pastes
it as the GitHub Actions secret `CLOUDFLARE_API_TOKEN`, alongside `AIRTABLE_TOKEN` (the
same read-only database token). Then you can `gh workflow run` the Action and
`gh run watch` it to prove the 2-hour refresh works end to end.

## UI quirks that will waste your time if you don't know them
- **Some Cloudflare text fields drop the first character you type** through the browser
  automation (typed `NODE_VERSION`, got `ODE_VERSION`). Prepend a throwaway character
  (`XNODE_VERSION` → `NODE_VERSION`). *But not every field does this* — the watch-path
  chip field kept the `X`. Type, screenshot, verify, fix.
- **⌘A doesn't select-all** in those fields. Clear with `End` then repeated `Backspace`.
- **Clicking a settings anchor in the right rail (e.g. "Builds") doesn't scroll** — scroll
  the page yourself.
- **GitHub shows a 404, not "access denied," for a private repo's settings when you're not
  signed in.** If the student "gets a 404" on the secrets page, they clicked it in a
  browser that isn't logged into GitHub. Open it in the logged-in one.
- **The Workers flow has no "deploy hook"** and "Triggers cannot be added to a Worker that
  only has static assets." Don't plan a refresh around a hook — use the GitHub Action.
- **Build variables vs runtime variables:** the Settings page says "Variables cannot be
  added to a Worker that only has static assets" — that's *runtime*. Build-time variables
  (the token, NODE_VERSION) live under **Settings → Builds → Variables and secrets** and
  work fine.
- Cron is **UTC** everywhere; a 5am-local schedule shifts by an hour when daylight time
  ends. Note it for the student.
