# Morning routine always lists the bills Vera needs

Decided: 2026-10-13, by the owner.

Every morning daily pass includes, as a [YOU] item, the bills Vera needs the owner to send her.

- Source: Bills table, Personal Finance Airtable base. Active bills only.
- A bill is needed when its amount is not confirmed for the current month (note says estimated, median, verify, or was confirmed for an earlier month only).
- Part A, new statements likely out: active statement-type bills (cards, loans, buy-now-pay-later, utilities, insurance) whose due day already passed this month and whose new statement Vera does not have yet. Skip fixed confirmed amounts with no statement (rent, attorney, subscriptions). Added same day at owner's request.
- Part B, coming due: bills due in the next 7 days whose amount is not confirmed for the current month.
- For each: name, due day, and exactly what to send (statement or amount due).
- If none: "No bills needed from you today."
- Never mark a bill confirmed or paid unless the owner sent it.

Lives as the routine row "Bills I need from you" (Order 1, daily, active) in the Routines table.

## Update, same day

The owner: ask for a new statement only after its statement date, which Vera already knows from past statements. Dates live in `reference/statement-dates.md`. A statement is due to ask for when today is on or after (last statement on file + 1 month) and that statement is not in the vault yet. Bills with no statement on file are not chased.
