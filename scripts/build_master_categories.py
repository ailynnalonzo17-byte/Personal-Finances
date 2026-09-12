# Master category list, exactly as given by the user, plus system-added
# Income and Transfer groups needed for reconciliation.

MONTHLY_BILLS = [
    "Amazon Prime","Atty Chua","Cal Water","Car insurance","Car payment","Comcast",
    "Google 1","National Life Ins","Netflix","Rent","Roku","Verizon",
    "Waste Management","Yesoulfitness","YT Premium","PGE","Insurance","Harna fit",
    "Planet Fitness","Life 360",
]

EXPENSES = [
    "Compass","CVS","Doris","Food - Ailynn","Food - Chris","Food - Eat Out",
    "Food - Misc","Food - To go","For Bike","For Car","Gas","Groceries - Costco",
    "Groceries - Others","Groceries - Safeway","Groceries - Santa Fe",
    "Groceries - Steves","Groceries - Walmart","Key Salary","Lawyer","Medical","Misc - Gail",
    "Misc - gail gown and cap","Movie","Others","paypal tiktok",
    "Remittance - Aron","Remittance - Aron tuition","Remittance - others",
    "Salinas Valley Dr","Shop - Amazon","Shop - Amazon returns","Shop - Goodwill",
    "Shop - Others","Shop - Ross","Shop - Shein","Shop - Temu","Shop - Tiktok",
    "Shop - Whatnot","Vacation","Water",
]

DEBT = [
    "Affirm","Upgrade","CC - FPB","Auto Loan - Honda","CC - Ollo","CC - Aspire",
    "paypal - Alipay","paypal - pay in 4 Golden Nugget","CC - Credit 1","Klarna",
    "CC - Frontier card","CC - Whole foods","Afterpay","CC - One Pay",
    "CC - Citibank","CC - Capital 1","CC - paypal","CC - cashback MC",
    "Paypal pay in 4","CC - Mission Lane","CC - Citizen bank",
]

INCOME = [
    "Chris - Pension","Kristin - COO Income","Others - Income",
]

TRANSFER = [
    "Transfer - Checking to Savings","Transfer - Savings to Checking",
    "Transfer - Checking to PayPal","Transfer - PayPal to Checking",
    "Transfer - Checking to SoFi Savings",
    "Transfer - SoFi Savings to Checking",
]

ALL_GROUPS = {
    "Monthly Bills": MONTHLY_BILLS,
    "Expenses": EXPENSES,
    "Debt": DEBT,
    "Income": INCOME,
    "Transfer": TRANSFER,
}

def flat():
    out = []
    for g, cats in ALL_GROUPS.items():
        for c in cats:
            out.append((g, c))
    return out

if __name__ == "__main__":
    for g, c in flat():
        print(g, "|", c)
    print("\nTotal categories:", len(flat()))
