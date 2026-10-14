# When each new statement comes out

Built 2026-10-13 from the statements you sent (data/seed/credit_card_*.json and bill_*.json `lastStatementDate`).
Vera asks for a bill's new statement only AFTER its next statement date has passed and she does not have it yet.
When you send one, update its "last statement on file" here and in data/seed.

| Bill | Statement closes on day | Last statement on file |
|---|---|---|
| CC - Capital 1 | 2 | 2026-10-02 |
| NV Energy | 3 | 2026-10-03 |
| CC - FPB | 4 | 2026-09-04 |
| CC - Credit 1 (...4838) | 4 | 2026-10-04 ($0 balance, you told me) |
| CC - Venmo | 4 | 2026-10-04 |
| CC - Aspire | 8 | 2026-10-08 ($0 balance, you told me) |
| CC - Ollo | 9 | 2026-10-09 ($0 balance, you told me) |
| CC - Credit 1 (...4352) | 10 | 2026-09-10 |
| CC - Frontier card | 11 | 2026-09-11 |
| CC - AAA Visa (...8228) | 12 | 2026-10-12 |
| Auto Loan - Honda | 13 | 2026-09-13 |
| CC - One Pay | 17 | 2026-09-17 |
| CC - Chase Amazon Visa | 18 | 2026-09-18 |
| CC - Citibank | 18 | 2026-09-18 |
| CC - Capital 1 Savor (...9140) | 18 or 19 | 2026-09-18 |
| CC - cashback MC | 25 | 2026-09-25 ($0 balance, you told me) |
| CC - paypal | 27 | 2026-09-27 ($0 balance, you told me) |
| CC - Mission Lane | 28 | 2026-09-28 ($0 balance, you told me) |

Bills not listed have no statement on file, so there is no known date. Vera does not chase their statements.

A "$0 balance, you told me" counts as that month's statement on file. The next month is still asked for after its date.
