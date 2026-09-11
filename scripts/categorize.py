import csv, re

# Ordered rules: (regex, category, group, confidence, note)
# First match wins. Case-insensitive. confidence: H = high-confidence direct
# merchant match, D = reasonable default bucket, R = flagged, please confirm.
RULES = [
    # ---- Transfers (own-account moves; excluded from expense/income totals) ----
    (r"ONLINE TRANSFER TO\s+SAV", "Transfer - Checking to Savings", "Transfer", "H", ""),
    (r"ONLINE TRANSFER FROM SAV", "Transfer - Savings to Checking", "Transfer", "H", ""),
    (r"ODP TRANSFER FROM SAVINGS", "Transfer - Savings to Checking", "Transfer", "H", "Overdraft-protection auto-pull from savings"),
    (r"PAYPAL\s+TRANSFER\s+ADD TO BALANCE", "Transfer - Checking to PayPal", "Transfer", "H", ""),
    (r"PAYPAL\s+TRANSFER(?!\s+ADD)", "Transfer - PayPal to Checking", "Transfer", "H", ""),
    (r"SOFI BANK\s+TRANSFER|SMBS ACCOUNT\s+TRANSFER", "Transfer - Checking to SoFi/Other", "Transfer", "R", "Large transfer (thousands) to a SoFi/SMBS account - please confirm what this account is"),

    # ---- Monthly Bills ----
    (r"AMAZON PRIME", "Amazon Prime", "Monthly Bills", "H", ""),
    (r"CHUA TINSAY", "Atty Chua", "Monthly Bills", "H", ""),
    (r"CALWATER", "Cal Water", "Monthly Bills", "H", ""),
    (r"CSAA INSURANCE", "Car insurance", "Monthly Bills", "H", ""),
    (r"CAPITAL ONE AUTO CARPAY", "Car payment", "Monthly Bills", "H", ""),
    (r"COMCAST-XFINITY", "Comcast", "Monthly Bills", "H", ""),
    (r"GOOGLE ONE|GOOGLE \*GOOGLE ONE", "Google 1", "Monthly Bills", "H", ""),
    (r"LIFE INS OF SW", "National Life Ins", "Monthly Bills", "H", ""),
    (r"^NETFLIX\.COM|NETFLIX 1 ", "Netflix", "Monthly Bills", "H", ""),
    (r"\bROKU\b", "Roku", "Monthly Bills", "H", ""),
    (r"VERIZON WIRELESS", "Verizon", "Monthly Bills", "H", ""),
    (r"REPUBLIC SVCS|WASTE MANAGEMENT PAYMENT", "Waste Management", "Monthly Bills", "H", ""),
    (r"GOOGLE YESOULFI|YESOULFIT", "Yesoulfitness", "Monthly Bills", "H", ""),
    (r"GOOGLE YOUTUBE|YOUTUBEPREMIUM", "YT Premium", "Monthly Bills", "H", ""),
    (r"PACIFIC GAS & ELECTRIC|PG&E", "PGE", "Monthly Bills", "H", ""),
    (r"THE HARTFORD", "Insurance", "Monthly Bills", "H", ""),
    (r"GOOGLE \*HARNA|THEHARNAFIT", "Harna fit", "Monthly Bills", "H", ""),
    (r"PLANET FITNESS", "Planet Fitness", "Monthly Bills", "H", ""),
    (r"GOOGLE \*Life360|LIFE360", "Life 360", "Monthly Bills", "H", ""),

    # ---- Debt payments (loan/card servicers) ----
    (r"AFFIRM\.COM|AFFIRM \* PAY", "Affirm", "Debt", "H", ""),
    (r"UPGRADE, INC\.", "Upgrade", "Debt", "H", ""),
    (r"PREMIER BANKCARD", "CC - FPB", "Debt", "H", ""),
    (r"WESTLAKESVCS", "Auto Loan - Honda", "Debt", "R", "Westlake Financial payment - assumed Honda auto loan, please confirm"),
    (r"^WF\s+PAYMENT", "Auto Loan - Honda", "Debt", "R", "Same $ amounts as the Westlake payments below/above - looks like the same auto loan, formerly serviced by 'WF'. Please confirm"),
    (r"OLLO CC", "CC - Ollo", "Debt", "H", ""),
    (r"ASPIRE ?MC|AUTOPMT ASPIREMC", "CC - Aspire", "Debt", "H", ""),
    (r"PAYPAL \*ALIPAYUSINC", "paypal - Alipay", "Debt", "H", ""),
    (r"CREDIT ONE BANK", "CC - Credit 1", "Debt", "H", ""),
    (r"^KLARNA|KLARNA\*", "Klarna", "Debt", "H", ""),
    (r"BARCLAYCARD", "CC - Frontier card", "Debt", "R", "Barclaycard - assumed this is the Frontier Airlines card, please confirm"),
    (r"AFTERPAY", "Afterpay", "Debt", "H", ""),
    (r"ONEPAY CASHREWRD|ONEPAY.*SYF", "CC - One Pay", "Debt", "H", ""),
    (r"CITI CARD ONLINE PAYMENT", "CC - Citibank", "Debt", "H", ""),
    (r"CAPITAL ONE\s+MOBILE PMT|CAPITAL ONE\s+CRCARDPMT", "CC - Capital 1", "Debt", "H", ""),
    (r"PAYPAL\s+INST XFER\s+PPCR", "CC - paypal", "Debt", "H", ""),
    (r"PAYMENT TO CHASE CARD", "CC - cashback MC", "Debt", "R", "Payment to a Chase card ending 1755 - guessed this is the cashback Mastercard, please confirm"),
    (r"PAYPAL \*PYPL PAYIN4", "Paypal pay in 4", "Debt", "H", ""),
    (r"MISSION LANE", "CC - Mission Lane", "Debt", "H", ""),
    (r"CITIZENS PAY", "CC - Citizen bank", "Debt", "H", ""),

    # ---- Expenses: specific merchants ----
    (r"CVS/PHARMACY", "CVS", "Expenses", "H", ""),
    (r"ZELLE PAYMENT TO DORIS LOPEZ", "Doris", "Expenses", "H", ""),
    (r"DOORDASH|GRUBHUB|UBER\s?EATS|UBEREATS", "Food - To go", "Expenses", "H", ""),
    (r"DIAMOND DENTAL|SHS\*SVMHSCLINICS|SHS\*SVHMC", "Medical", "Expenses", "H", ""),
    (r"PAYPAL\s+PURCHASE\s+TIKTOK SHOP", "paypal tiktok", "Expenses", "H", ""),
    (r"TIKTOK SHOP", "Shop - Tiktok", "Expenses", "H", ""),
    (r"TAPTAP SEND|SENDWAVE", "Remittance - others", "Expenses", "R", "Remittance app transfer - recipient not shown; please tell me if this is Aron, Aron's tuition, or someone else"),
    (r"AMAZON MARKETPLA ADJUSTMENT", "Shop - Amazon returns", "Expenses", "H", ""),
    (r"AMAZON MARKETPLA|AMAZON\.COM SERVI|AMAZON\.COM\*|AMAZON PRIME\*", "Shop - Amazon", "Expenses", "H", ""),
    (r"GOODWILL", "Shop - Goodwill", "Expenses", "H", ""),
    (r"ROSS STORES", "Shop - Ross", "Expenses", "H", ""),
    (r"\bSHEIN\b", "Shop - Shein", "Expenses", "H", ""),
    (r"\bTEMU\b", "Shop - Temu", "Expenses", "H", ""),
    (r"\bWHATNOT\b", "Shop - Whatnot", "Expenses", "H", ""),
    (r"PRIMO WATER", "Water", "Expenses", "H", ""),
    (r"COSTCO WHSE", "Groceries - Costco", "Expenses", "H", ""),
    (r"SAFEWAY", "Groceries - Safeway", "Expenses", "H", ""),
    (r"STEVE'S FILIPINO", "Groceries - Steves", "Expenses", "H", ""),
    (r"WM SUPERCENTER|WAL-MART", "Groceries - Walmart", "Expenses", "H", ""),
    (r"TRADER JOE|FOODSCO|NOB HILL FOODS|LUCKY #|FOODMAXX", "Groceries - Others", "Expenses", "H", ""),
    (r"CINEMARK", "Movie", "Expenses", "H", ""),
    (r"MYSUBARU SUBSCRIPTION", "For Car", "Expenses", "H", ""),
    (r"NAPA STORE|O'REILLY|U-HAUL", "For Car", "Expenses", "H", ""),
    (r"SP\+AFF \* HOWLER BIKE", "For Bike", "Expenses", "H", ""),
    (r"GIV\*FIRST PRESBY", "Others", "Expenses", "H", "Recurring $20 church/charitable giving - no matching category in your list, put under Others"),

    # ---- Expenses: broad default buckets (lower confidence, still usable) ----
    (r"CHEVRON|SHELL (SERVICE|OIL)|EXXON|\bARCO\b|VALERO|FASTRAK|SAV ON GASOLINE|MARATHON \d|TRAVEL CENTER|76 - |SALINAS SINCLAI|7-ELEVEN|D & R MKT|NYACK EMIGRANT GAP", "Gas", "Expenses", "D", ""),
    (r"PARKING|PARK LOT|SELFPARK|GARAGE|PAYBYPHONE|CITYOFSAC-OFFSTREETPAY", "For Car", "Expenses", "D", "Parking charge, defaulted to For Car"),
    (r"CAR WASH", "For Car", "Expenses", "D", ""),
    (r"SALINAS HONDA", "For Car", "Expenses", "D", "One-off Honda dealer charge (service/parts), not the loan"),
    (r"(RESTAUR|CAFE|BURGER|GRILL|BBQ|PIZZA|TACO|NOODLE|THAI|CHICKEN|SUSHI|BAKERY|COFFEE|DONUT|BOBA|TEA SOCI|DINER|KITCHEN|BUFFET|DELIGHT|CREPES|WINGSTOP|SUBWAY|MCDONALD|WENDY|ARBY|KFC|JOLLIBEE|IN-N-OUT|CARLS JR|FRESH JERKY|FOSTERS FREEZE|STEAK N SHAKE|IHOP|PANERA|STARBUCKS|CHOCOLATE WORL|FAMOUS NYNY|HABIT (SALINAS|BURGER)|TAQUERIA|LITTLE CAESARS|ELPOLLOLOCO|JACK IN THE BOX|OLIVE GARDEN|CHIPOTLE|FREDDY'S|CRAB BUCKET|MAHARLIKA|PAN ASIAN EXPRESS|GHIRARDELLI|SALINAS MAIN IN|COCA COLA|ABC #101)", "Food - Eat Out", "Expenses", "D", "Restaurant/fast-food - defaulted to Eat Out; move to Food - Ailynn/Chris/Misc if you know whose order it was"),
    (r"^SQ \*|^TST\*|^SG\*V\*|^CKE\*|^ABC\*P|HOTEL LV|GOLDEN NUGGET", "Food - Eat Out", "Expenses", "D", ""),
    (r"\bIKEA\b.*RESTAUR", "Food - Eat Out", "Expenses", "D", ""),
    (r"TARGET T-|T\.J\. MAXX|TOMMY HILFIGER|MARSHALLS|UNIQLO|KIPLING|LACOSTE|\bCROCS\b|EBAY COMMERCE|GROUPON|REI #|CHIC AND COZY|LA SALON AND SPA|SALINAS LIQUIDATIONS|DOLLAR TREE|NESPRESSO|SUDZ LLC|SHOPPAWVIA|AMBERCUP", "Shop - Others", "Expenses", "D", ""),
    (r"^SP\+AFF|^SP\s|^SP[A-Z]|^CM9S|^FLUXIONKQ4W", "Shop - Others", "Expenses", "R", "Small online-shop charge via an affiliate/Affirm-style processor - description doesn't name the actual store"),
    (r"THE HOME DEPOT|LOWE'S|HARBOR FREIGHT|MINUTEKEY", "Others", "Expenses", "D", "Home-improvement store - no matching category in your list"),
    (r"THE UPS STORE|USPS", "Others", "Expenses", "D", "Shipping/postal"),
    (r"PETSMART", "Others", "Expenses", "D", "Pet supplies - no matching category in your list"),
    (r"PIERCE CO\., LP", "Others", "Expenses", "R", "Unclear what this business is"),
    (r"PAYPAL\s+PURCHASE", "Others", "Expenses", "R", "Subscription/purchase via PayPal (Apple, Etsy, Google apps, Lyft, AARP, etc.) - no matching category"),
    (r"UBER |UBER\*|VENMO", "Others", "Expenses", "R", "Rideshare or Venmo payment - no matching category, and Venmo recipient is unclear"),
    (r"^LBC SALINAS", "Remittance - others", "Expenses", "R", "LBC is a Filipino remittance/cargo courier - please confirm recipient"),
    (r"ONLINE PAYMENT.*TO ALA 0908", "Others", "Expenses", "R", "Recurring $706.36/month loan-type payment to 'ALA 0908' - please tell me what this is so I can give it the right category"),
    (r"MADONNA INN|BOARDWALK PLAZA|QUALITY INNS|CITY PISMO BEACH|MSS SURFACE LOT|SFC LAS VEGAS|BOULDER VINTAGE|LITTLE PAMPANGA|CLARK CO PARKS|SSA - USS MIDWAY|CSI-\d", "Vacation", "Expenses", "D", "Hotel/travel-city charge, looks like part of a trip"),

    # ---- Fees / misc bank ----
    (r"FEE_TRANSACTION|WIRE FEE|CHECK OR SUPPLY", "Others", "Expenses", "H", "Bank fee"),
    (r"^ATM WITHDRAWAL", "Others", "Expenses", "H", "ATM cash withdrawal - cash spend is untracked after this point"),
    (r"^CHECK\b", "Others", "Expenses", "R", "Paper check - payee not shown on the statement; please tell me who checks were written to"),

    # ---- Income ----
    (r"TEAMSTERS\s+PAYMENTS", "Chris - Pension", "Income", "R", "Recurring ~$4,275 credit - assumed this is Chris' Teamsters pension, please confirm"),
    (r"UNITED PARCEL SE\s+PAYROLL", "Key Salary", "Income", "R", "UPS payroll deposit - assumed this is your own Key Salary income, please confirm"),
    (r"CHECK_DEPOSIT|REMOTE ONLINE DEPOSIT|DEPOSIT\s+ID NUMBER|CHIPS CREDIT", "Others - Income", "Income", "R", "Deposit/wire with unclear source"),
    (r"UNITED PARCEL SE\s+DV\d", "Others - Income", "Income", "R", "UPS-related credit, not the regular payroll line"),
    (r"JOSE REYES REYES PUSH", "Others - Income", "Income", "R", "Incoming payment, source unclear"),
    (r"ZELLE PAYMENT FROM", "Others - Income", "Income", "R", "Zelle received - please tell me who this person is so I can map them to a category"),
    (r"ZELLE PAYMENT TO", "Others", "Expenses", "R", "Zelle sent - please tell me who this person is so I can map them to a category"),
    (r"^PAYPAL\s+INST XFER", "Others", "Expenses", "R", ""),
]

COMPILED = [(re.compile(pat, re.I), cat, grp, conf, note) for pat, cat, grp, conf, note in RULES]

def type_fallback(ttype, amount):
    credit_types = {"MISC_CREDIT","ACH_CREDIT","QUICKPAY_CREDIT","PARTNERFI_TO_CHASE",
                     "WIRE_INCOMING","CHECK_DEPOSIT","DEPOSIT"}
    if ttype in credit_types or amount > 0:
        return "Others - Income", "Income", "R", "Unrecognized credit - please tell me the source"
    return "Others", "Expenses", "R", "Unrecognized charge - please tell me what this is"

def categorize(desc, ttype, amount):
    for rx, cat, grp, conf, note in COMPILED:
        if rx.search(desc):
            return cat, grp, conf, note
    return type_fallback(ttype, amount)

def main():
    rows = list(csv.DictReader(open("data/raw/Chase0861_Activity_20260907.csv")))
    out = []
    for r in rows:
        desc = r["Description"]
        amt = float(r["Amount"])
        cat, grp, conf, note = categorize(desc, r["Type"], amt)
        out.append({
            "Account": "Checking ...0861",
            "Date": r["Posting Date"],
            "Description": desc.strip(),
            "Amount": amt,
            "Type": r["Type"],
            "ChaseBalance": r["Balance"],
            "Category": cat,
            "Group": grp,
            "Confidence": conf,
            "Note": note,
        })
    with open("data/processed/checking_categorized.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out[0].keys())
        w.writeheader()
        w.writerows(out)

    matched = sum(1 for o in out if o["Category"])
    conf_counts = {}
    for o in out:
        conf_counts[o["Confidence"]] = conf_counts.get(o["Confidence"], 0) + 1
    print(f"Rows: {len(out)}  |  Confidence breakdown: {conf_counts}")

if __name__ == "__main__":
    main()
