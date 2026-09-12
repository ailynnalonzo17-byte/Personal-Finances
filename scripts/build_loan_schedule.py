import json, datetime

def dates_seq(start_mmdd, count, start_year=2026, day_override=None):
    """Generate a monthly sequence of dates from a start (month, day)."""
    m, d = start_mmdd
    out = []
    y = start_year
    for i in range(count):
        mm = ((m - 1 + i) % 12) + 1
        yy = y + ((m - 1 + i) // 12)
        dd = day_override if day_override else d
        out.append(f"{yy:04d}-{mm:02d}-{min(dd,28) if mm==2 and dd>28 else dd:02d}")
    return out

PLANS = []

def plan(name, provider, amount, dates_amounts, account="checking"):
    installments = []
    for i, (d, a) in enumerate(dates_amounts, start=1):
        installments.append({"n": i, "total": len(dates_amounts), "dueDate": d, "amount": a,
                              "paid": d < "2026-09-12"})
    PLANS.append({"name": name, "provider": provider, "account": account, "installments": installments})

# 1. Klarna - Amazon - car computer (12 x 53.97)
d = ["2026-08-13","2026-09-13","2026-10-13","2026-11-13","2026-12-13","2027-01-13",
     "2027-02-13","2027-03-13","2027-04-13","2027-05-13","2027-06-17","2027-07-13"]
plan("Klarna - Amazon (car computer)", "Klarna", 53.97, [(x,53.97) for x in d])

# 2. Affirm Eufy camera (4 x 88.24)
d = ["2026-08-14","2026-08-28","2026-09-11","2026-09-25"]
plan("Affirm - Eufy camera", "Affirm", 88.24, [(x,88.24) for x in d])

# 3. Affirm - Amazon (5 x 68.11, last 68.09)
d = ["2026-08-18","2026-09-18","2026-10-18","2026-11-18","2026-12-18"]
amts = [68.11,68.11,68.11,68.11,68.09]
plan("Affirm - Amazon (5 mo)", "Affirm", 68.11, list(zip(d,amts)))

# 4. Affirm WRX (6 x 220.95)
d = ["2026-06-21","2026-07-21","2026-08-21","2026-09-21","2026-10-21","2026-11-21"]
plan("Affirm - WRX", "Affirm", 220.95, [(x,220.95) for x in d])

# 5. Affirm Howler Bike Park (12 x 47.93)
d = ["2026-07-01","2026-08-01","2026-09-01","2026-10-01","2026-11-01","2026-12-01",
     "2027-01-01","2027-02-01","2027-03-01","2027-04-01","2027-05-01","2027-06-01"]
plan("Affirm - Howler Bike Park", "Affirm", 47.93, [(x,47.93) for x in d])

# 6. Klarna Fabletics (1 x 13.18)
plan("Klarna - Fabletics", "Klarna", 13.18, [("2026-08-14",13.18)])

# 7. Affirm Expedia - Inn at Avila Beach (3 x 141.09)
d = ["2026-08-20","2026-09-20","2026-10-20"]
plan("Affirm - Expedia (Avila Beach)", "Affirm", 141.09, [(x,141.09) for x in d])

# 8. Affirm Expedia - San Diego (3 x 287.25)
d = ["2026-07-15","2026-08-15","2026-09-15"]
plan("Affirm - Expedia (San Diego)", "Affirm", 287.25, [(x,287.25) for x in d])

# 9. Affirm - Amazon 12mo (12 x 49.17)
d = ["2026-09-24","2026-10-24","2026-11-24","2026-12-24","2027-01-24","2027-02-24",
     "2027-03-24","2027-04-24","2027-05-24","2027-06-24","2027-07-24","2027-08-24"]
plan("Affirm - Amazon (12 mo)", "Affirm", 49.17, [(x,49.17) for x in d])

# 10. Affirm Wayfair plan 1 (6 x 177.82)
d = ["2026-09-26","2026-10-26","2026-11-26","2026-12-26","2027-01-26","2027-02-26"]
plan("Affirm - Wayfair", "Affirm", 177.82, [(x,177.82) for x in d])

# 11. Affirm Wayfair plan 2 (partial, 3 x 177.82 given)
d = ["2026-09-30","2026-10-30","2026-11-30"]
plan("Affirm - Wayfair (2nd plan)", "Affirm", 177.82, [(x,177.82) for x in d])

# 12. Chase - China Air, day-30 schedule (12 x 169.59)
d = ["2026-09-30","2026-10-30","2026-11-30","2026-12-30","2027-01-30","2027-02-28",
     "2027-03-30","2027-04-30","2027-05-30","2027-06-30","2027-07-30","2027-08-30"]
plan("Chase Pay Over Time - China Air (day 30)", "Chase", 169.59, [(x,169.59) for x in d])

# 13. Klarna - OnePay - Walmart TV (6 x 93.87)
d = ["2026-09-26","2026-10-26","2026-11-26","2026-12-26","2027-01-26","2027-02-26"]
plan("Klarna - Walmart (OnePay TV)", "Klarna", 93.87, [(x,93.87) for x in d])

# 14. Chase Pay in 4 (partial, missing 1/4 - given 2/4,3/4,4/4)
dates_amts = [("2026-09-18",75.20), ("2026-10-12",75.20), ("2026-10-16",75.20)]
installments = [{"n": i+2, "total": 4, "dueDate": dd, "amount": aa, "paid": dd < "2026-09-12"} for i,(dd,aa) in enumerate(dates_amts)]
PLANS.append({"name":"Chase Pay in 4","provider":"Chase","account":"checking","installments":installments})

# 15. Chase - China Airline, day-15 schedule (12 x 169.59) - separate plan from #12
d = ["2026-10-15","2026-11-15","2026-12-15","2027-01-15","2027-02-15","2027-03-15",
     "2027-04-15","2027-05-15","2027-06-15","2027-07-15","2027-08-15","2027-09-15"]
plan("Chase Pay Over Time - China Airline (day 15)", "Chase", 169.59, [(x,169.59) for x in d])

def slug(s):
    import re
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

total_installments = 0
for p in PLANS:
    doc_id = slug(p["name"])
    p["docId"] = doc_id
    total_installments += len(p["installments"])
    json.dump({"name":p["name"],"provider":p["provider"],"account":p["account"],"installments":p["installments"]},
               open(f"/home/user/Personal-Finances/data/seed/loanplan_{doc_id}.json","w"))

print(f"{len(PLANS)} plans, {total_installments} total installments")
for p in PLANS:
    unpaid = sum(1 for i in p["installments"] if not i["paid"])
    print(f"  {p['docId']:55s} {len(p['installments']):3d} installments, {unpaid} unpaid")
