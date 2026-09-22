# Your base

**Version: 4.1 - 2026-08-10**

**Vera writes this file into your own repo and keeps it current. You never fill it in by hand,
though you can correct anything she gets wrong.**

It is a plain snapshot of your Airtable base: what tables you have, what fields are in them, and a
note on anything unusual. The agents read it so they know where your data lives without guessing.

**If you rename a table or add a field, just tell Vera "my base changed" and she rewrites this.**

---

## Base

| | |
|---|---|
| Base name | Personal Finance |
| Base id | appUV4lqX4Q9t6zKH |
| Last read | 2026-09-22 |

There is also a separate **Vendor Management** base (`apppCO9mNTtpGoALw`) in this account, not yet
connected to anything this system uses. Flag if that changes.

## Tables

| Table | Fields |
|---|---|
| Bills | Name, Group (single select), Amount (currency), Due day (number), Active (checkbox), Note |
| Routines | Name, What it does, Instructions, How often, Last ran, How it went, Notes, Active, Order, Prepare and wait |
| Tasks | Title, Status, Note |
| Skills | Name, What it does, Version, Path in repo, Last updated |
| Table 1 | Name only — unused placeholder, left over from the base template |

**The real transaction history is not in Airtable.** It lives in this repo under `data/seed/` and
`data/processed/`, built by the scripts in `scripts/`. The Bills table here is a simpler, editable
list of recurring bills — check whether it or `data/seed/bill_*.json` is meant to be the current one
before trusting either blindly.

## Notes

| Note | |
|---|---|
| Which table holds your routines | Routines (empty as of 2026-09-22 — no routine has been set up yet) |
| Which table holds your tasks | Tasks (empty as of 2026-09-22) |
| Your timezone | Not confirmed. Utility switch (PG&E → NV Energy) suggests Pacific, unconfirmed |
| Your currency | USD |
| How you prorate a partial month | Not recorded |
| How you name documents | Not recorded |

---

## For your assistant

- **Read this file before touching data.** It is faster and safer than exploring the base every time.
- **If something you need is not here, re-read the base rather than guessing**, then update this file.
- **If a table or field you need genuinely does not exist, say so and stop.** Never write into the
  closest-looking alternative. Getting it wrong in a base full of real tenant data is worse than
  stopping and asking.
- **Keep this file in the owner's own repo.** The copy in the shared library is an empty template.
