---
name: command-center-builder
description: >-
  Step-by-step guide for building a student's own hosted, private, auto-refreshing
  multi-company Command Center dashboard — a single web page with an HQ overview
  plus one page per business, pulling live data from the Airtable, Google Calendar,
  Slack, Gmail and (optionally) QuickBooks connectors, deployed on Cloudflare, with metrics
  the student chooses and a briefing their own Vera regenerates each morning. USE THIS SKILL whenever a VA Optional student (or Stephanie) wants to
  build, set up, or replicate the Command Center / "command center dashboard" /
  personal HQ dashboard for their own accounts and businesses — even if they only
  say "build my dashboard," "the command center," "a daily briefing page," "one
  page for each of my companies," or "the thing Steph built." Claude runs this
  interactively and can drive the browser for the parts that are safe to automate.
  This is a teaching artifact: assume nothing, guide the student through every step,
  and never skip the credential-handoff and confirmation rules.
metadata:
  tier: 3.Tool
---

# Command Center Builder

**Version: 3.4 - 09-30-2026** (Phase P deploys as a WORKER only: the line-up prompt now says so, and `references/cloudflare.md` "Lining it up" step 4 checks the address ends in `.workers.dev` and redoes the import if it ends in `.pages.dev`. A student's Vera took Cloudflare's legacy Pages flow and she reached the Week 4 session on pages.dev; the Workers-only warning lived in section 1, which the pre-work never quoted.) (3.3 - 09-21-2026: `references/cloudflare.md` says out loud that Cloudflare builds from GitHub and no session needs Cloudflare's API, so a cloud session that hits the 403 moves only the Cloudflare CLICKS to the local session, after saying what is already pushed, and never bounces the student between sessions. A student lost two days going back and forth while her code sat on GitHub ready to import.) (3.2 - 09-13-2026: a change lands in FOUR places and three times running it landed in one: the skill got fixed while the page a student reads went on saying the old thing, caught each time by Stephanie reading it rather than by anyone checking. Adds the propagation list and the three claims that have actually gone stale — the intake is FOUR questions not three, the Airtable token is handed over in the PRE-WORK not the session, and the session pushes rather than importing, gating and publishing.) (3.1 - 09-13-2026: how the warm-up reads a base, after the live test on Stephanie's: pull table NAMES only, pick the six or eight that carry the business, then read a few real RECORDS from just those — a full schema dump blew the response limit at nearly 300,000 characters, and a schema never tells you whether a field is actually filled in. "Which tables hold real data" must be read, never inferred from table names. Plus Stephanie's point that a student's base is quite likely EMPTY on the day: that is the normal case, it is never raised as a gap, and the metric suggestions come from what their business needs on the assumption the fields get filled in later, each one naming the table and field it waits on.) (3.0 - 09-12-2026: THE WARM-UP NOW DRAFTS THE INTAKE QUESTIONS AND HOLDS THEM, so "build my command center" fires them in seconds instead of after a long silence Stephanie watched from the outside on the dry run. The warm-up's "facts only, no suggestions" was suppressing the THINKING as well as the display, so all the expensive work — choosing metrics from their base, drafting the routing map, framing the money question — landed after the student said go. It now happens in the warm-up, held unshown. Two supporting fixes: the warm-up must collect the ACCOUNTS behind each connector and not just the service names, because question 4 cannot be drafted without them and the pasted prompt was only asking for services; and the prep check collapses to one thing, opening the holding page, now that Phase P proves the rest.) (2.9 - 09-12-2026: three diagnostics from a student stuck for days, all in `references/gotchas.md`: (1) `Cannot find module '/opt/buildhome/repo/command-center/bake.mjs'` means THE REPO DOES NOT HAVE THE FILE — she was told twice that her code was on GitHub by people who never opened GitHub; (2) prove you can PUSH before you build anything, because a session with broken git credentials looks healthy until the push and hers lost a commit outright; (3) a cloud session cannot reach Cloudflare AT ALL, 403 at the proxy, proven with a control. Plus: several clones of the same vault on one machine is its own failure mode, so name the folder you are in.) (2.8 - 09-12-2026: THE PRE-WORK IS FOUR STUDENT STEPS PLUS PHASE P, not five plus Phase P. The old step 2 — open Cloudflare's Create an application screen, authorize GitHub, then STOP and close the tab without deploying — is deleted. It was the single most confusing instruction in the pre-work, it fought Cloudflare's own flow, and it left students staring at an empty Workers & Pages list assuming they had failed (a student, 09-10). The GitHub authorization now happens inside Phase P, in the import flow where Cloudflare wants it, with Vera driving and the student clicking the popup. Phase P therefore has TWO student stops, the GitHub popup and the Airtable token. Also: Cloudflare's Create Token button is in the MIDDLE of the screen, and leaving the Airtable tab open is a blessed alternative to saving the token.) (2.7 - 09-12-2026: two fixes from the first real Phase P run: (1) the hand-off must NEVER give the student the phrase that starts the build — a run ended by telling them to say "build my command center" on session day, and a student handed the trigger will use it alone and arrive with the session's whole lesson already half-done; say what the session produces, never how to start it. (2) Getting the Airtable token into Cloudflare now has two blessed routes, the student pasting into the field on screen or handing it over in chat, because the real run did the first and the rule only allowed the second.) (2.6 - 09-12-2026: a PARKED design note, `references/writing-back.md`, for the day the page has to SAVE something a person types — a journal, a daily gratitude line, a hand-typed metric. Stephanie asked for the pre-work token to be made write-capable now; the answer is no, because the page is static and has nothing running to receive a write, so a bigger token buys nothing and a write-capable key in a browser can delete her tenants. The note records the shape instead: the Worker gains a script beside its assets, the write token becomes a Worker secret, entries land in Airtable and are read back live rather than from the two-hourly bake. Nothing in it is built or proven.) (2.5 - 09-11-2026: PHASE P: the import, the Airtable token, the login gate, the watch path and the first refresh run all move into the PRE-WORK as step 6, "Let Vera line it up", because Vera pushes a HOLDING PAGE first so the first build cannot fail — Stephanie, after asking why the import could not be pre-work. The student arrives at the session with a live address behind their own login showing "being built" and a Last-refreshed stamp that proves both keys work; the session is warm-up, intake, the real page and baker at the same paths, and the routine. New assets: `holding-page.html`, `bake.stub.mjs`, `lineup-prompt.md`. Also: the reference `refresh-data.yml` and `wrangler.jsonc` carry placeholders instead of the reference account id and project name.) (2.4.1 - 09-11-2026: the pre-work page now opens with what Week 4 builds and why the pre-work exists; steps 4 and 5 explain WHY the two keys go to GitHub and why the Cloudflare copy of the Airtable token cannot be placed before the session.) (2.4 - 09-11-2026: pre-work rewritten to match the Week 4 page after the dry run: one click per line, indented sub-steps, on-screen cues, "memory vault" everywhere, step 2 says it creates NO app yet, step 5 repeats the GitHub clicks instead of "same as step 4"; the stuck prompt and the prep table now AGREE with golden rule 1 that Vera asks for the read-only Airtable token in chat — the old "never into a chat" line made a student's Vera refuse it; and the reference baker, page template and PLACEHOLDERS carry `<YOUR_AIRTABLE_BASE_ID>` / `<TBL_…>` / `<FLD_…>` placeholders instead of the reference base's real ids.) (2.3 - 09-10-2026: from the Week 4 dry run: every connected tool gets a SYNTHESIS,
never a list, unless the owner asks for a list — golden rule 7 and the routine prompt. Two students
got a raw dump of every Todoist item and every CRM transaction because only Calendar, Slack and
Email had synthesis instructions. And this skill now lives in the cohort library, so "no
command-center-builder skill exists" stops being the first thing Vera says.) (2.2: the pre-work is TEN minutes, not twenty; on the Week 4 page it is a
collapsed dropdown because it is assumed done, and the lesson opens with the warm-up prompt so the
student starts it and reads while Vera works.) (2.1: the intake asks a FOURTH question, the routing map: which Gmail,
Slack workspace, calendar and QuickBooks company feeds which business. The warm-up now lists the
accounts behind each connector, not just the service names, because that list is what the question
is built from. Phase 4 stops being a second conversation and becomes recording the answer.) (2.0: the build now opens with a WARM-UP phase Vera runs alone — install
the skill, verify the prep, inventory connectors, read their business and their base, check the
books — reporting facts and no suggestions, so a live call can run it before the teaching. Then ONE
intake message, three questions, one reply, as a hard gate before any file is written; metrics come
from their base AND what Vera knows of their business, and an unfed metric is still suggested as a
🔒 placeholder; QuickBooks is offered after the books check instead of waiting to be asked.) (1.10: no hands-on step for the student: Vera ASKS for the read-only
Airtable token in chat and puts it into Cloudflare herself. Card, passwords, the Cloudflare API
token and any write-capable token stay the student's alone.) (1.9: rule 4 rewritten: "build my command center" is the standing approval
for every push, merge, deploy and the routine creation and first run; Vera narrates, never asks.
Only secrets, card, terms, OAuth, account creation and the two student decisions remain stops.) (1.8.2: Airtable token step: Access before Scopes, save the token privately BEFORE pasting it into GitHub, no "save it twice".) (1.8.1: paste the token value before typing the secret name; team name is not a step.) (1.8: prep steps rewritten to Stephanie's real-screen wording: Create
application, Connect to GitHub, Install & Authorize OR Save, Zero Trust via the left menu, Profile →
API Tokens, "scroll to Account Resources, dropdown after Include", the repository's own Settings tab
not the profile menu; the Vera prompt is now a STUCK helper with a screenshot, not a follow-along.) (1.7: brand: use it only if already known, otherwise default to The Lean
Landlord palette without looking or asking; hand-off tells them the address, the login, and to save
it to the home screen.) (1.6.1: Workers & Pages is reached through the dashboard search box, not the left menu, on a new account.) (1.6: the page opens on a phone OR a computer, never "on your phone" alone;
both refresh jobs only READ, nothing is written back to any connected tool; and the GitHub-authorize
prep step now spells out every click, because "authorize it" told a student nothing.) (1.5: student-facing vocabulary from Stephanie: "memory vault" not
"skills repo", "credit card" not "card", explain Cloudflare as the company that hosts the page and
puts a login on it, the Command Center WILL show private information; and the token never goes into
the chat even without a password manager, a locked phone note or a fresh token in the session is the
fallback.) (1.4: adds `assets/prep-prompt.md`, the prompt a student pastes into Vera
to be walked through the before-the-session steps; it sits behind a copy button on the Week 4 prep
page.) (1.3: Phase 3 split: the account half of Cloudflare — account, GitHub
authorization, Zero Trust with the card, the API token, the Airtable token — is now a BEFORE THE
SESSION checklist the student does alone, so the build session only imports and deploys. Matches
how the cohort is onboarded: setup before the live session, teaching during it.) (1.2: Stephanie's
review, two passes: no Worth Anchor; one business = one
page; several businesses = all tabs created, ONE populated first; connectors they already have or a
placeholder, nothing else on day one; no hand-seeded briefing, the first briefing is generated
automatically as the last build step; the old "remaining secrets" phase is now an advanced note.
Second pass: the briefing runs as a **scheduled cloud routine**, not a Daily Routines row. Her
reason, which is correct: every day-one source is a connector, connectors work from the cloud, and a
cloud routine fires at 5am whether or not the laptop is open, while a routines row waits for the
student to open Claude. A row would cost currentness for nothing. 1.1 had this backwards.)

You are guiding a student (a self-managing landlord / small-business owner in the
VA Optional program) through building **their own** version of the Command Center:
a single, private, phone-viewable web page that shows, for each of their businesses,
what needs their attention today — the hard numbers refreshed automatically in the
cloud, and the written briefing refreshed each morning by their own Vera.

**This is a live, guided build.** The student is not a developer. You do the technical
work; they make the decisions and supply the credentials only you're not allowed to
touch. Go one piece at a time, confirm each decision, and explain *why* at each step so
they understand what they're building. The more carefully you follow this the fewer
questions you'll face, because you are the one who will walk them through it.

---

## What you're building (the finished shape)

A static web page (`index.html`) + a data file per source, hosted on **Cloudflare**,
gated by **Cloudflare Access** (private to the student's own login). Tabs:

- **HQ** — the executive layer that sits above every business: a daily mindset, ONE
  "High Leverage / Long-Term Payoff" action, and a one-line "pulse" card per company.
  (There is no Worth Anchor. Stephanie removed it 09-08-2026.)
- **One tab per company** — each with that company's own snapshot: the metrics *they chose*,
  its Calendar, its Slack, its Email, and its Power Move. **Every business gets a tab, including
  ones with nothing wired yet** — an empty tab renders 🔒 placeholders naming what it's waiting
  for, which is exactly the to-do list for the rest of the build. **But only ONE company is
  populated in the first build**; the others stay as honest placeholders until the next session.
- **A student with ONE business gets ONE page, not two tabs.** The HQ content (mindset,
  leverage action) sits at the top and the company content below it, on the same page. Two tabs
  for one business is a tab bar with nothing to switch between.

Two data files drive it:
- `data.json` — hard, structured metrics baked from a database (Airtable in the
  reference build). Refreshed every ~2 hours by a build script.
- `personal.json` — the written briefing + per-company Calendar/Slack/Email/Power Move,
  produced each morning by **a scheduled Claude cloud routine** with the student's connectors and
  their repo attached. It needs an LLM reading their connectors, so a build script cannot make it,
  and it is generated for the FIRST time automatically at the end of the build (Phase 5).

Read **`references/architecture.md`** for the full picture and the reasoning behind
every structural choice before you start building. It will save you and the student
from dead ends.

---

## The golden rules (read before touching anything)

1. **One credential you DO handle, everything else is theirs (Stephanie, 09-09-2026).**
   **The read-only Airtable token is the exception**, and there are TWO acceptable ways to get it
   into Cloudflare (Stephanie, 09-12-2026, after a real run did the second one): (a) bring the
   Cloudflare field up on screen and let the student paste it in themselves, or (b) ask for it in
   chat and type it into the field yourself. **Offer one, say which you are doing, and take theirs
   if they prefer the other.** (a) is slightly better because the token never enters the chat
   transcript; (b) is better for a student who freezes at a form. It is a safe exception either way
   because that token is read-only, scoped to one base, and re-created free in seconds. If you ask
   in chat, say one line when you ask: it will sit in this chat's history, and they can revoke and
   re-issue it from Airtable any time. **Everything else stays theirs and you never type, paste or read it**: passwords, card
   numbers, the Cloudflare API token, any write-capable token. If one of those is needed, stop
   and tell them where to paste it themselves.

2. **Hand off at terms, payments, OAuth grants, and account creation.** Creating a
   Cloudflare account, accepting a Terms of Service, adding a payment method, authorizing
   an OAuth app — these are the student's clicks. You set everything up to that point and
   pause. See `references/cloudflare.md` for exactly where these moments fall.

3. **"We have it" ≠ "the cloud routine has it."** A token existing on the student's
   machine, in their password manager, or in a local server does NOT mean the cloud
   routine can use it. The routine runs isolated on Anthropic's servers; every credential
   must be copied into the routine's own secrets before it can use them. Explain this
   plainly — it is the single most common point of confusion.

4. **"Vera, build my command center" IS the approval. Do not ask again (Stephanie, 09-09-2026).**
   Once the student has asked for the build, every technical step inside it is pre-approved:
   committing and pushing to their memory vault, merging, importing the repo into Cloudflare,
   deploying, turning on Access, narrowing the watch path, creating the morning routine, and
   running it once. Say in one line what you are doing as you do it; never stop to ask "may I
   push?" or "shall I create the routine?". A student who has to approve six invisible steps
   stops trusting the build. The ONLY stops are the ones in rule 1 and rule 2: a secret value, a
   card, a terms page, an OAuth grant, an account creation, and the two decisions only they can
   make (which business first, which metrics). Everything else, do.

5. **Never commit secrets or third-party PII into the repo, and never serve them.** The
   baked data file with personal/tenant data is git-ignored; the source map with email
   addresses lives *outside* the served folder. See `references/gotchas.md`.

6. **When something is genuinely faster for you to do in the browser and it's not a
   credential/terms/payment/OAuth step, take over and do it** rather than narrating
   clicks. `references/cloudflare.md` marks every "you drive" vs "they click" boundary.

7. **Every connected tool gets a SYNTHESIS, never a list, unless the owner asks for a list
   (Stephanie, 09-10-2026).** This applies to EVERY tool the page reads — Calendar, Slack, Email,
   and any other tool the student has connected (a task manager like Todoist, a CRM, GoHighLevel,
   a project board, anything). For each one, the panel says what matters today and why, in a few
   lines: what needs them, what changed, what is stuck, what is winning. It never reproduces the
   tool's own list. **A command center is not a to-do list**; the student already has the tool for
   that, and a page that repeats it gets closed. The rule of thumb is five items or fewer per panel,
   each one a judgement, and a link or a sentence pointing at the tool for the rest. **Why:** on
   the Week 4 dry run one student got every open Todoist item on her page and another got every
   transaction her coordinators were handling, because only Calendar, Slack and Email had synthesis
   instructions and Vera fell back to "here is everything, you decide." **If the student asks for a
   list** ("show me all leases expiring", "list the open tickets"), give them the list — that is the
   one exception, and it is theirs to make, not yours.

---

## The build, in phases

Do these in order. Each phase has a dedicated reference file — open it when you reach
that phase; don't try to hold it all in your head. Confirm completion of each phase with
the student before moving on.

### Before the session — the student does this alone, ahead of time
Everything in Cloudflare that needs THEIR login, THEIR card, or THEIR copy of a secret has no
dependency on the dashboard existing yet, so it comes out of the build session entirely. Send them
the Week 4 page. The steps are theirs to do from the page (a Loom video under each). The page's
"Copy the stuck prompt for Vera" button carries **`assets/prep-prompt.md`**, used ONLY when a screen
does not match: they paste it with the step number and a screenshot, and Vera gives the next click
from **`references/cloudflare.md` → "Before the session"**. They arrive with:

1. A Cloudflare account they can sign into.
2. Zero Trust switched on for the account: Free plan, card on file, terms accepted.
   This is the most friction-heavy step in the whole build and it has nothing to do with the page.
3. A Cloudflare API token ("Edit Cloudflare Workers" template, scoped to their account) already
   pasted into their GitHub repo as the Actions secret `CLOUDFLARE_API_TOKEN`.
4. A read-only token for their database (Airtable: `data.records:read`, that base only) pasted into
   the same repo as the Actions secret `AIRTABLE_TOKEN`, and still reachable — the Airtable tab left
   open, or a saved copy — so they can hand it over once more in step 5.
5. **Step 5 — "Let Vera line it up" (Phase P, Vera drives, about ten minutes, LOCAL session only).**
   The student pastes `assets/lineup-prompt.md` into a new Vera chat on their own computer. Vera
   pushes the holding page skeleton into the vault, imports it into Cloudflare (**the student clicks
   the GitHub authorization popup here — that is the old step 2, moved**), gets the Airtable token in
   and places it, turns on the login gate, narrows the watch path, runs the refresh job once, and
   hands over the address. Full order in `references/cloudflare.md` → "Lining it up".
   They arrive at the session with a live page at their own address, behind their own login, that
   says "being built" and shows when it last refreshed itself. **Her hand-off says what the session
   will produce and never how to start it** — no trigger phrase, no skill name, no intake questions.
   See the hard rule in `references/cloudflare.md` → "Lining it up", step 8.

**First thing in the session, verify the prep** (two minutes): the holding page opens at their
address behind the Cloudflare login, its "Last refreshed" is within the last two hours, and its
`data.json` says `airtableTokenPresent: true`. If all three hold, steps 1 to 6 are proven at once.
If there is no address, step 6 was skipped: run Phase P now, from `references/cloudflare.md` →
"Lining it up" (ten minutes if steps 1 to 5 were done, closer to forty if not). **Why the import
CAN be pre-work now (2.5):** Cloudflare builds what is on GitHub, and Phase P pushes a holding page
and a stub baker first, so the first build succeeds. Before 2.5 nothing was in the vault yet and a
pre-session import failed, which is why the import used to wait for the session.

### Phase 0a — WARM-UP: everything Vera can find out on her own (do this FIRST, before any teaching)
**Trigger:** the student pastes `assets/warmup-prompt.md`, or says "get me set up for the command
center build". On a live call this runs at the top, while Stephanie is still setting up, so the
build later is short. It works just as well solo, minutes or days before the build.

**In this phase Vera gathers, DRAFTS, and reports. She makes no suggestions ON SCREEN, asks NO
questions, and writes NO files.** The point is to arrive at the build with the intake message
already written, so that "build my command center" produces the questions in seconds instead of
after a long silence while she thinks.

**⛔ WHAT "NO SUGGESTIONS" MUST NOT SUPPRESS (Stephanie, 09-12-2026, from the dry run).** It means
nothing recommended is *displayed*. It does NOT mean the thinking is deferred. Choosing four to six
metrics out of their base with a reason for each, drafting the routing map, and framing the money
question is the expensive part of this whole build, and on the dry run every bit of it happened
AFTER the student said go, while they watched a blank screen. **Do all of it here, in step 7, and
hold it.** The student sees only the eight factual lines.

**The warm-up and the build are the SAME CHAT.** The held draft lives in the conversation and
nothing is written to disk. The warm-up prompt tells the student to stay put.

1. **Make sure the skill is here.** If `command-center-builder` is not installed, install it:
   sync it from the student's memory vault (`skills/command-center-builder/`), or install the
   `.skill` file they were given. Say which version loaded.
2. **Verify the prep** — the fast way first: open their Command Center address (it is in the
   vault's `wrangler.jsonc` name plus their workers.dev subdomain, or ask). If the holding page
   opens behind the login, "Last refreshed" is within two hours and `data.json` shows
   `airtableTokenPresent: true`, all six pre-work steps are proven; say so in one line. If there is
   no address, fall back to the four checks in `references/cloudflare.md` → "Before the session"
   (Cloudflare sign-in, GitHub connected, Zero Trust on, both Actions secrets) and report each as
   done or missing, plus "step 6 not run: Phase P will happen at the start of the build". **A
   missing one is a fact, not a lecture** — say what to do and move on.
3. **Inventory the connectors AND the accounts behind them, then stop there.** Not just "Gmail is
   connected" — **which Gmail addresses, which Slack workspaces, which calendar, which QuickBooks
   company**. That list is what question 4 of the intake is built from, and you cannot guess it
   later. List which of Airtable, Google Calendar, Slack, Gmail and QuickBooks are connected right
   now, each with its account names, and which are not connected at all. **Do NOT suggest
   connecting anything yet** and do not say what each one would unlock. That comes in the intake.
4. **Read their business.** The five foundational skills the Week 1 interview wrote (identity and
   positioning, ideal client, programs and offers, brand voice) plus their vault. You are learning
   how they actually make money and what they chase, because that is what makes your metric
   suggestions theirs instead of a copy of somebody else's dashboard.
5. **Read their database in three cheap steps. Never pull the whole schema.** A full schema dump on
   a real base is enormous: Stephanie's forty tables came back at nearly 300,000 characters and blew
   the response limit outright, costing the warm-up several of the minutes it exists to save.
   - **a. Table NAMES only.** Fast at any size.
   - **b. Pick the six or eight that plausibly carry the business**, from the names alone. Operating
     tables are named obviously — Units, Leases, Rent Payments, Maintenance. Skip the other thirty.
   - **c. Read a few real records from just those.** This gives you field names AND proves those
     fields are POPULATED, which a schema never tells you. **A field existing is not a field anyone
     fills in.** "Which tables hold real data" is the most load-bearing fact in the whole warm-up,
     because it decides which metrics ship live and which ship as padlocks. **Read it. Never infer
     it from table names** — that inference is safe only on a base you already know, and on a
     student's base you have no basis for it at all.

   **⛔ AN EMPTY BASE IS THE NORMAL CASE, NOT A PROBLEM (Stephanie, 09-13-2026).** There is a good
   chance a student's base has not been filled in at all yet. Do NOT raise it as a gap, do not treat
   it as a blocker, and above all **do not fall back to a generic dashboard** — that is the failure
   this whole intake exists to prevent. Instead: **suggest the metrics their BUSINESS needs, on the
   assumption the fields will be filled in later**, and name the table and field each one is waiting
   on. Every one ships as a 🔒 placeholder saying what it needs, so the page doubles as their
   Airtable to-do list, and each panel lights itself up the first morning after they start filling
   it in. An empty base changes where your suggestions come FROM; it never changes how specific they
   are.
6. **If QuickBooks is connected, check whether the books are current** — run the P&L and look at
   the last three months (`references/quickbooks.md`). Hold the finding; you will use it in the
   intake. Do not raise money yet.
7. **Write the intake message in full, and HOLD it.** All four questions from Phase 0b, with your
   recommendation already filled in on every line, drawn from what you just read. This is the step
   that makes the build feel instant. Do not display it, do not summarise it, do not hint at what
   is in it.
8. **Report back in about eight lines, facts only.** Skill and version, the prep check, what is
   connected and what is not, one line on what their business does, the tables that hold real
   data, and the books finding if there is one. End with one sentence: "That is everything I can
   work out on my own. When you are ready, say build my command center here and I will ask you
   four questions." **Then stop.** Do not roll into the build.

### Phase 0b — THE INTAKE: one message, four questions, one reply
**⛔ HARD GATE: you may not create a file, a repo entry, a Cloudflare project or a routine until
this message has been sent and answered.** Everything after it is pre-approved (golden rule 4);
this is the one place in the whole build where you stop.

**Why this exists (Stephanie, 09-09-2026).** A build ran that never asked which metrics to show
or whether to put money on the page, so the student got a copy of somebody else's dashboard. The
opposite failure is just as bad: an open-ended design conversation that never reaches a live page.
One message with your recommendation already on each line solves both. The student replies once.

**⛔ SEND THE MESSAGE YOU ALREADY WROTE IN THE WARM-UP. Do not compose it now.** The questions are
the FIRST thing out of your mouth after "build my command center" — no preamble, no "let me take a
look", no re-reading their base. On the dry run that stretch was long enough that Stephanie noticed
it from the outside, and every second of it was work the warm-up should already have done.

**If there is no held draft** (the warm-up was skipped, or this is a fresh chat), say so in one line
— "I need two minutes to read your base first, the warm-up was not run in this chat" — and then do
it. Never leave them watching silence without telling them why.

**The message, in this shape** (full template with worked examples in
`assets/intake-message.md`):

> Before I build, four things. My pick is on each, so reply "go" to take them all, or tell me
> what to change.
> 1. **Which business first.** *(Skip this question entirely if they have one business.)* Name
>    their businesses, say you will make a tab for each and fully build ONE today, name which one
>    you would start with and why, and say the others get placeholders you fill in later sessions.
> 2. **Which numbers.** Suggest four to six, each one they would act on TODAY if it moved the
>    wrong way. Draw them from BOTH sources: the tables in their base that hold real data, AND
>    what you learned about their business in the warm-up. **A metric that matters to them but
>    has nothing feeding it yet is still worth suggesting** — say so plainly and it becomes a 🔒
>    placeholder naming what it needs, which is the honest to-do list. Never install a default set.
> 3. **Money in and out.** Say what you found in the books, then ask. Books current: "rent income
>    posts through August, so money in and out will be accurate — want it on the page?" Books
>    behind: "your books show no income since May, which usually means deposits are sitting
>    uncategorized, so a money panel would read zero and be wrong — I would leave it off until
>    that is caught up. Agree?" QuickBooks not connected: "not connected, so money is off for now;
>    connect it any time and I will add it."
> 4. **Which account feeds which business.** Show the routing map you would use, built from the
>    accounts you listed in the warm-up, and ask them to correct it. This is the question they are
>    most likely to have to fix, because **you can guess an email domain but you cannot guess a
>    Slack workspace** — on the reference build a workspace literally named "the-lean-landlord"
>    held a different company's channels. Rules for building the guess: a dedicated inbox on a
>    business's own domain routes entirely to that business; **a catch-all personal inbox feeds
>    EVERY business, listed once per business with its own filter**, so the same address legitimately
>    appears more than once; one calendar holding everything is normal and gets sorted per event by
>    reading what the event is about, so propose two or three keyword hints per business; QuickBooks
>    holds one company file, so name the single business page its money lands on.
> Then one line, not a question: which colours you are using (theirs if you already know them,
> otherwise The Lean Landlord palette) and that "change the colours" is one sentence away later.

**Keeping it to one round trip:**
- **One message, one reply, then build.** If they answer two of three, take your recommendation on
  the third, say which you took, and start.
- **If they ask something back, answer in one line and re-ask only what is outstanding.** Never
  more than two rounds. A third round means you are designing, not building.
- **Anything else they raise mid-build gets "noted, we will do that once it is live."** The page
  is edited by asking, so deferring costs them nothing and costs the session everything if you
  do not.
- **Never re-open a choice they already made.** Cap the numbers at six; if they want a seventh,
  ask which comes off.

### Phase 0c — The shape, settled without asking
These are decided by rule, not by conversation. Do not spend intake questions on them:
- **One business = one page.** No tab bar: HQ content on top, the company below.
- **Two or more = a tab per business plus HQ**, every tab created on day one, **only the one they
  named in question 1 populated**. The rest carry honest 🔒 placeholders and get filled one per
  later session. One company done properly beats three done halfway.
- **The HQ page is called HQ** unless they say otherwise.
- **Only tools they have already connected.** Anything else is a 🔒 placeholder naming the tool;
  it fills the first morning after they connect it. No API tokens, no self-hosted mail server, no
  per-workspace Slack keys on day one (`source-map.md` and `_advanced` in
  `sources.template.json` cover the student who later outgrows a connector).
- **Every company page gets Calendar, Slack, Email and Power Move** on top of its numbers, plus
  one synthesized panel per OTHER connected tool (task manager, CRM, project board). Every one of
  those panels is a synthesis, not a list — golden rule 7.
- **Brand: use theirs only if you ALREADY know it** — hex colours in the Week 1 foundational
  skills, or a brand book in their vault's `sources/`. Otherwise **default to The Lean Landlord
  palette and move on**: terracotta `#C4622D` accent, ink `#1C1C1C`, cream `#F9F7F4` ground,
  border `#E0DEDA`, muted `#6B6B6B`, light header `#fbf9f4`, heading serif Fraunces. Do not read
  their website, do not ask for hex values.
- **Hosting: Cloudflare Workers static assets + a scheduled refresh**, code in their own GitHub
  repo. `references/architecture.md` has the reasoning against the alternatives.

### Phase 1 — The page (`index.html`)
Build the page **at the same path as the holding page, `command-center/public/index.html`**, so the
push replaces it in place at the address the student already saved. Use `assets/index.template.html` as the starting point — it already has HQ +
per-company tabs, the palette tokens, the render logic, the 🔒 "add credential" states, and
the charts. Fill in the student's companies, brand tokens, and database field IDs. For a
single-business student, collapse HQ and the company into one page (no tab bar). **There is
no hand-seeded briefing any more**: the numbers connect the moment the baker runs, and the
written briefing is generated for real at the end of Phase 5, in the same build session. Until
then the HQ section shows its one-line "not generated yet" note, which is honest and lasts
minutes. Preview locally (serve the folder, open it) before deploying. Details + the exact
token list: `references/architecture.md` → "Building the page."

### Phase 2 — The database baker (structured metrics)
If a company has a real database, write/adapt the baker that reads it and writes
`data.json`. **It replaces the stub at the same path, `command-center/bake.mjs`**, so neither the
Cloudflare build command nor the refresh job changes. The reference build reads Airtable via REST with a read-only token and does
all aggregation in the baker. Use `assets/bake.mjs` as the reference implementation and
`references/architecture.md` → "The baker" for how to remap it to the student's own base,
tables, and fields. Key discipline: the baker owns `data.json` and nothing else; it runs
in the cloud build with the token as a build env var; `data.json` is git-ignored.

### Phase 3 — Deploy on Cloudflare (already done in Phase P; here only if step 6 was skipped)
**If the holding page is live, this phase is one push.** Commit the real page and baker, push, watch
Cloudflare rebuild, Visit, verify each tab. Nothing to import, no token to ask for, the gate and the
watch path are already set. **Only if there is no address** do the full phase, which is: import the repo (Workers "Import a repository" flow), set
the build and deploy commands, add `NODE_VERSION` and the database token (ask the student for the
read-only Airtable token in chat, then type the name AND paste the value yourself and click
**Encrypt**), deploy, visit, protect the Worker behind Access (policy: Cloudflare account
members), narrow the build watch path to `command-center/*`. Follow **`references/cloudflare.md`**
→ "In the session" exactly; it carries the field-input quirks (some fields drop the first typed
character — prepend a throwaway one) so you don't fight the UI. **There is no student click left
in this phase**; you drive all of it. If the prep
was skipped, the account half of `cloudflare.md` is done first, in the session, and the phase
takes closer to forty minutes.

### Phase 4 — The source map (multi-account inputs)
**This is no longer a conversation — it is writing down what they answered in intake question 4.**
Do not re-open it. Record the routing they confirmed in `sources.json` (template:
`assets/sources.template.json`), which lives **outside** the served folder. **Every `via` says `connector` on day one.** The same file records
their chosen `metrics` per company. This is the heart of making it work for any
student's accounts. Full pattern — dedicated vs. shared/"wildcard" inboxes, Gmail labels +
LLM fallback, per-workspace Slack tokens, connector vs. direct-API access, and the exact
JSON schema — is in **`references/source-map.md`**. A student with one Gmail and one Slack
fills in one line each; a power user with an account per business maps each one.

### Phase 5 — The morning briefing (a cloud routine, created automatically, first run now)
Regenerate `personal.json` each morning from the source map and push it (Cloudflare
redeploys). **Vera does this phase without being asked and without asking, as the last step of
the build** (rule 4: creating the routine and running it once are inside the approval the student
already gave):

1. **Create a scheduled Claude cloud routine** (the `schedule` skill / RemoteTrigger): daily at
   5am their local time (cron in UTC), model Opus, the student's repo attached as a source, and
   every connector they have already connected attached (`mcp_connections`: Calendar, Slack,
   Gmail, Airtable, QuickBooks as applicable). Its prompt is `assets/routine-prompt.md`, filled
   in. No question to the student; the routine IS the deliverable.
2. **Run it once right now** (`RemoteTrigger run`) and watch for the commit. Cloudflare
   redeploys on the push. Open the page and show them their real HQ and company content within
   minutes of the build finishing. This replaces the old hand-seeded briefing entirely.
3. Tell them: "From tomorrow this rewrites itself at 5am, laptop open or closed."

**Why the cloud and not a row in their Daily Routines table (settled by Stephanie 09-08-2026).**
Every day-one source is a claude.ai connector, and connectors work from a cloud routine; the
repo is attached, so the push works too (proven on the reference build, five mornings running).
A routines row runs only when the student opens Claude on their machine, so the briefing would
be as late as their morning. The cloud routine fires at 5am regardless. The only thing a cloud
routine cannot reach is something local to their machine (a self-hosted server, a local MCP
server), and a connector-only student has none. **A routines row is the fallback for a source
that is local**, not the default. Vera's manual's one-scheduled-task rule is about tasks on the
machine and does not forbid this.

**One trap that IS real: a cloud routine can report SUCCEEDED while doing nothing** (a previous
Cowork-based routine did exactly that for weeks). So never trust the status flag: watch for the
commit on the briefing file and read the run log the first time. `routine.md` has the full
detail, the secrets a power user may need, and the graceful "🔒 pending" behavior.

### Phase 6 — Fill the padlocks, later, one per session
A 🔒 on a company page means one of two things, and the note under it says which:
- **A tool they have not connected yet** (the day-one case). The fix is the student connecting
  it on claude.ai; the panel fills on the next morning run. Nothing to paste.
- **A source reached by API instead of a connector** (advanced, only if they later outgrow a
  connector: a second Slack workspace, a self-hosted mail server). Then a secret has to be
  handed to the morning run, and the note names it.
Connectors carry their own login, so **a connector-only student never pastes a secret in this
phase.** Do one padlock per session and confirm each; the other company tabs from Phase 0 are
filled the same way, one company per session.

### Phase 6b — money in / money out (QuickBooks)
**Not opt-in by the student any more (Stephanie, 09-09-2026): you check the books in the warm-up
and OFFER it as question 3 of the intake.** A student who does not know the option exists never
asks for it, which is why the first real build shipped without money on the page. Build it if they
said yes. Read **`references/quickbooks.md`** first.
The short version: it runs through the **QuickBooks connector on the morning routine** (never
send a student to the Intuit REST API — it needs a developer app and a compliance review that
takes days), it lands in `personal.json` under the owning company, and there are two traps that
will otherwise bite you. **Check the books are current before building** — a QBO report shows
only POSTED transactions, so uncategorized deposits sitting in "For Review" read as $0 income
and the panel will confidently display a wrong number every morning. And **the connector's
computed totals are wrong** — read the named `Income` / `Cost of Goods Sold` / `Expenses` rows
and never sum the account maps.

### Phase 7 — Record + hand off
- Update the student's own skills/automation catalog if they keep one.
- For Stephanie's own copy: update the Sunrise Airtable skills catalog (see the
  skill-creator "Sunrise rule").
- Leave the student with: their live URL (say it out loud and put it in the chat), how they log
  in (their Cloudflare email and password, remembered for a day), that they should save it to their
  phone's home screen and bookmark it on the computer, that "what is my command center address?"
  gets it back any time, how it refreshes, and how to ask you to change it later ("change X on my command center" → you edit the repo files,
  push, it redeploys).

---

## How to run this with a student (interaction style)

- **One piece at a time.** This build has a lot of moving parts. Resist doing five things
  at once — the reference build went cleanly precisely because each source (Gmail, then
  Slack, then Calendar) was mapped and confirmed on its own.
- **Explain the why, not just the click.** They're learning a system they'll own. When you
  hit a fork (connector vs API, replace vs keep, labels vs LLM), give them the tradeoff and
  a recommendation, then let them choose.
- **Show, don't assert.** Preview locally and screenshot; deploy and verify; test-run and
  read the result back. Never tell them it works — show them.
- **Protect their live site.** Don't leave a half-finished `index.html` sitting modified on
  disk in a repo that auto-syncs — it can deploy an intermediate version. Revert drafts you
  aren't ready to ship (see `references/gotchas.md`).

---

## ⛔ A CHANGE LANDS IN FOUR PLACES, NOT ONE (09-13-2026, after the third time)

The same words exist in this skill AND on the Week 4 pages in Lovable, and three times running a
rule was fixed here while the copy a student actually reads went on saying the old thing. Each time
it was caught by Stephanie reading the page, not by anyone checking. **A skill change nobody
propagated is a skill change that did not happen**, because the page is what the student follows.

**After changing anything about how the build works, walk this list:**

| Where | What lives there |
|---|---|
| This skill + `references/` | The procedure Vera follows |
| `assets/*-prompt.md` | The three prompts, which must be **byte-identical** to the Lovable constants |
| `this-is-week-4.tsx` | `COMMAND_CENTER_WARMUP_PROMPT`, and the Step 1-4 narrative describing what she will do |
| `command-center-prep.tsx` | `COMMAND_CENTER_PREP_PROMPT`, `COMMAND_CENTER_LINEUP_PROMPT`, and the five pre-work steps |

**The specific things that have gone stale, all three from the Phase P rework:** the number of
intake questions (it is FOUR, the routing map was added and the page still said three), who hands
over the Airtable token and when (the pre-work, not the session), and what the session does to
Cloudflare (it pushes; the import, the gate and the login all happened in the pre-work).

**When you touch any of those, grep the Lovable files for the OLD claim rather than trusting that
you updated everything.** Searching for what should no longer be true is faster and more reliable
than re-reading for what should.

## Reference files (open as you reach each phase)

- `references/architecture.md` — the whole design, why each choice was made, and how to
  build/adapt the page and the baker. Read first.
- `references/cloudflare.md` — click-by-click Cloudflare deploy + Access, with the
  drive-vs-handoff boundaries and UI quirks.
- `references/source-map.md` — multi-account Gmail/Slack/Calendar mapping, connector vs
  API, labels + LLM fallback, and the `sources.json` schema.
- `references/routine.md` — creating, prompting, securing, and testing the morning cloud
  routine.
- `references/decisions.md` — every decision made on the reference build and its outcome,
  so you can offer sane defaults and explain them.
- `references/metrics.md` — the metric catalog Vera offers, how to run the choice, and the
  rules that keep the page honest.
- `references/quickbooks.md` — OPTIONAL money in/out: why the connector and not the API,
  checking the books are current first, and the connector's broken totals.
- `references/gotchas.md` — the traps we hit and how to avoid them.
- `references/writing-back.md` — **PARKED, nothing built.** How the page would SAVE something a
  person types on it (journal, gratitude, a note, a checkbox): why a static page cannot today and a
  bigger token does not help, the Worker-script-plus-secret shape to build, the separate write
  token, and the freshness trap that entries must be read live rather than from the two-hourly
  bake. Read it before agreeing to build any input on the page.

## Asset templates (copy and fill in)

- `assets/holding-page.html` — the PRE-WORK page (Phase P): "your Command Center is being built",
  what is already working, the four intake questions, Last refreshed. Replaced in place in Phase 1.
- `assets/bake.stub.mjs` — the PRE-WORK baker: writes a pending `data.json` and reports whether the
  Airtable token is present, exits 0 either way. Replaced in place in Phase 2.
- `assets/lineup-prompt.md` — the prompt behind the Week 4 pre-work page's step 6 button; a student
  pastes it into a local Vera chat to run Phase P.

- `assets/index.template.html` — the dashboard page (HQ + per-company tabs, palette tokens,
  render logic, 🔒 states, charts).
- `assets/bake.mjs` — the database baker (Airtable reference implementation).
- `assets/wrangler.jsonc` — Cloudflare Workers static-assets config.
- `assets/refresh-data.yml` — GitHub Action that refreshes `data.json` on a schedule.
- `assets/sources.template.json` — the per-source→company map.
- `assets/routine-prompt.md` — the morning routine's full prompt.
- `assets/PLACEHOLDERS.md` — every placeholder token across the templates and what to
  replace it with; open it alongside the templates you're filling in.
- `assets/prep-prompt.md` — the prompt behind the Week 4 prep page's copy button; a student pastes
  it into a new Vera chat to be guided through the before-the-session account steps.
- `assets/warmup-prompt.md` — what the student pastes to start the warm-up (Phase 0a): Vera finds
  out everything she can alone and reports facts, no suggestions and no questions.
- `assets/intake-message.md` — the ONE message Vera sends before building (Phase 0b), with the
  three questions, two worked examples and the one-round-trip rules.
