# How this repo is organized

**Version: 1.0 - 2026-09-22**

**This is a Memory Vault laid out from the standard template, adapted for a repo that also holds real
working finance data and the scripts that process it.** It is yours: rename or add folders whenever
you like, and edit this file to match. Vera reads THIS copy and follows it.

One idea per file. Plain English. If you would not know where to put something, ask Vera and she
puts it where this file says, or proposes a new place and writes it here.

---

## The folders

| Folder | What goes there | Example |
|---|---|---|
| `CLAUDE.md` (a file, at the top) | Operating notes: who you are, what you track, how you like to work. Claude reads it automatically every session. Keep it short. | |
| `.claude/skills/` | The team. One folder per skill: Vera, Tessa, Fiona, Owen. These are your copies, customize them freely. | `.claude/skills/fiona/SKILL.md` |
| `data/raw/` | Statements and feeds exactly as they arrived: bank CSVs, card PDFs. Never edited by hand. | `data/raw/card_statements/citi_aug.pdf` |
| `data/seed/` | The structured record built from `data/raw/`: accounts, bills, loan plans, card transactions. Owen's pipeline writes this. | `data/seed/bill_rent.json` |
| `data/processed/` | Derived/reconciled views, ready to read. | `data/processed/checking_categorized.csv` |
| `scripts/` | The build and categorize scripts that turn `data/raw/` into `data/seed/` and `data/processed/`. | `scripts/build_card_data.py` |
| `artifact/` | The generated dashboard/workbook output. | `artifact/index.html` |
| `policies/` | House rules, one per file. What you always do, so the agents never guess. | `policies/how-i-categorize-cash-back.md` |
| `procedures/` | How you do a recurring job, step by step. The agents follow these when a routine runs. | `procedures/monthly-close.md` |
| `templates/` | Messages you reuse. The agents fill them in, they never invent wording. | `templates/dispute-letter.md` |
| `business/` | Facts that are not records: your household profile, contacts, insurers, lender info. | `business/profile.md` |
| `decisions/` | Decisions you made and why, dated, so nobody re-argues them later. | `decisions/2026-09-22_categories.md` |
| `notes/` | Weekly reviews, ideas. The thinking that is not a rule yet. | `notes/2026-09-22_weekly-review.md` |
| `reference/` | Maps and lookups Vera keeps for herself: where your data lives, this layout file. | `reference/your-base.md` |
| `log.md` (a file, at the top) | The running log. Vera appends a line whenever something worth remembering happened. You never edit it. | |

The course calls this whole repo your **Memory Vault**. Same thing.

**How this repo differs from the standard template:** the standard design keeps all real records in
Airtable and treats the repo as pure notes. Here, the real financial data (`data/`) and the scripts
that build it (`scripts/`) live in the repo itself and are the actual working pipeline. Airtable
holds the meta-tables this system needs (Routines, Tasks, Skills) plus a Bills table, not the full
transaction history.

## Naming

1. **Lowercase, words joined with hyphens, no spaces:** `late-fees.md`, not `Late Fees.md`.
2. **Everything outside `data/` and `scripts/` is `.md`** (plain text).
3. **Anything that happens on a date starts with the date:** `2026-09-22_topic.md`. Sorts itself.
4. **Folder names are plural nouns:** `policies`, `templates`, `decisions`.
5. **A skill folder is named exactly what the skill is called** in its first line.
6. **One topic per file.**

## Changing it

Rename a folder, add one, or drop one you never use. Then update the table above, or tell Vera and
she updates it and moves the files. From then on she follows the new layout.
