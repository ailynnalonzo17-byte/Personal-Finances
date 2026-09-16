# How this repo is organized

**Version: 1.0 - 2026-09-16**

**This is the standard layout, adapted for a personal finance repo rather than a landlord business.
It is yours: rename or add folders whenever you like, and edit this file to match. Vera reads THIS
copy, not the course's, so whatever you write here is the rule she follows.**

---

## The folders

| Folder | What goes there | Example |
|---|---|---|
| `CLAUDE.md` (at the top) | Operating notes: who you are, how you like to work, what Vera should always remember. | |
| `.claude/skills/` | Your team: Vera, Tessa, Fiona, Owen. Your own copies, customize freely. | `.claude/skills/fiona/SKILL.md` |
| `data/raw/` | Original bank and card statements as downloaded, untouched. **Already existed before Vera; kept as-is.** | `data/raw/card_statements/citi_sept.pdf` |
| `data/seed/` | Parsed bills, loan plans, card transactions, checking transactions. **Already existed before Vera; kept as-is.** | `data/seed/bill_rent.json` |
| `data/processed/` | Categorized, reconciled output. **Already existed before Vera; kept as-is.** | `data/processed/checking_categorized.csv` |
| `scripts/` | The build/categorize/reconcile pipeline. **Already existed before Vera; kept as-is.** | `scripts/build_workbook.py` |
| `artifact/` | The built workbook/dashboard output. **Already existed before Vera; kept as-is.** | `artifact/index.html` |
| `policies/` | House rules, one per file: what you always do, so the agents never guess. | `policies/late-fees.md` |
| `procedures/` | How you do a recurring job, step by step. | `procedures/monthly-close.md` |
| `templates/` | Messages you reuse. The agents fill them in, never invent wording. | `templates/rent-reminder.md` |
| `business/` | Facts that are not records: your profile, contacts, standing rules. | `business/profile.md` |
| `decisions/` | Decisions you made and why, dated. | `decisions/2026-09-16_repurposed-team.md` |
| `notes/` | Reviews, ideas, thinking that is not a rule yet. | `notes/2026-09-16_weekly-review.md` |
| `reference/` | Maps Vera keeps for herself. | `reference/your-base.md`, `reference/repo-layout.md` |
| `log.md` (at the top) | The running log. Vera appends a line when something worth remembering happened. You never edit it. | |

Your actual live records (bills table today; routines, tasks and skills tables as of this session)
live in **Airtable**, in the "Personal Finance" base. This repo holds how you think, how you work,
and the data pipeline files above. Airtable holds what is true right now for anything it tracks.

## Naming

1. **Lowercase, words joined with hyphens, no spaces.**
2. **Everything outside `data/`, `scripts/` and `artifact/` is `.md`.**
3. **Anything that happens on a date starts with the date:** `2026-09-16_topic.md`.
4. **A skill folder is named exactly what the skill is called.**
5. **One topic per file.**

## Changing it

Rename a folder, add one, or drop one you never use, then update the table above or tell Vera and
she updates it. **She never puts the course's default back over your changes.**
