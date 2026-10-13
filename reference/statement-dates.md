# When each new statement comes out

Built 2026-10-13 from the statements you sent (data/seed/credit_card_*.json and bill_*.json `lastStatementDate`).
Vera asks for a bill's new statement only AFTER its next statement date has passed and she does not have it yet.
When you send one, update its "last statement on file" here and in data/seed.

| Bill | Statement closes on day | Last statement on file |
|---|---|---|
| CC - Capital 1 | 2 | 2026-09-02 |
| NV Energy | 3 | 2026-10-03 |
| CC - FPB | 4 | 2026-09-04 |
| CC - Credit 1 (...4838) | 4 | 2026-09-04 |
| CC - Venmo | 4 | 2026-10-04 |
| CC - Aspire | 8 | 2026-06-08 |
| CC - Ollo | 9 | 2026-09-09 |
| CC - Credit 1 (...4352) | 10 | 2026-09-10 |
| CC - Frontier card | 11 | 2026-09-11 |
| Auto Loan - Honda | 13 | 2026-09-13 |
| CC - One Pay | 17 | 2026-09-17 |
| CC - Chase Amazon Visa | 18 | 2026-09-18 |
| CC - Citibank | 18 | 2026-09-18 |
| CC - cashback MC | 25 | 2026-08-25 |
| CC - paypal | 27 | 2026-05-27 |
| CC - Mission Lane | 28 | 2026-08-28 |

Bills not listed have no statement on file, so there is no known date. Vera does not chase their statements.
