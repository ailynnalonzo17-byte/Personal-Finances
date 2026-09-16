# Your base

**Version: 1.0 - 2026-09-16**

Vera writes this file and keeps it current. It is a plain snapshot of the "Personal Finance"
Airtable base: what tables exist, what fields are in them, and anything unusual.

---

## Base

| | |
|---|---|
| Base name | Personal Finance |
| Base id | appUV4lqX4Q9t6zKH |
| Last read | 2026-09-16 |

## Tables

| Table | Fields |
|---|---|
| Table 1 | Name (singleLineText) — unused placeholder table from when the base was created |
| Bills | Name, Group (singleSelect), Amount (currency), Due day (number), Active (checkbox), Note (multilineText) |
| Routines | Name, What it does, Instructions, How often, Last ran, How it went, Notes, Active, Order, Prepare and wait — added 2026-09-16 |
| Tasks | Title, Status, Note — added 2026-09-16 |
| Skills | Name, What it does, Version, Path in repo, Last updated — added 2026-09-16 |

## Notes

| Note | |
|---|---|
| Which table holds routines | Routines |
| Which table holds tasks | Tasks |
| Your timezone | Not recorded — ask, or infer from a future session's machine clock |
| Your currency | USD (inferred from $ amounts in the repo's bill/loan data) |
| Most of your actual bill/loan/card/transaction detail | Lives in this repo's `data/seed/` and `data/processed/` files, not yet mirrored into Airtable's Bills table beyond a placeholder start. The Bills table has 0 rows checked as of this session — treat repo data as the source of truth until reconciled |
| How you name documents | Not recorded — ask when it first comes up |

---

## For your assistant

- **Read this file before touching data.** If something you need is not here, re-read the base and
  update this file.
- **If a table or field you need genuinely does not exist, say so and stop.** Never write into the
  closest-looking alternative.
