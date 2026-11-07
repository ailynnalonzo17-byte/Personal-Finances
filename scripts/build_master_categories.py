# Master category list, exactly as given by the user, plus system-added
# Income and Transfer groups needed for reconciliation.

MONTHLY_BILLS = [
    "Amazon Prime","Atty Chua","BADD Insurance","Cal Water","Car insurance","Comcast","Cox",
    "Google 1","National Life Ins","Netflix","Rent","Roku","Verizon",
    "Waste Management","Yesoulfitness","YT Premium","PGE","Insurance","Harna fit",
    "Planet Fitness","Life 360","NV Energy","Cove Smart","SW Gas","Prulife","Republic Services",
]

EXPENSES = [
    "Business Expense","Compass","CVS","Dinkers","Doris","Food - Ailynn","Food - Chris","Food - Eat Out",
    "Food - Misc","Food - To go","For Bike","For Car","Gas","Groceries - Costco",
    "Groceries - Others","Groceries - Safeway","Groceries - Santa Fe",
    "Groceries - Seafood City","Groceries - Walmart","Groceries - Smith","Groceries - Filipino Store","Gym","Haircut","Health","Key Salary","Lawyer","Medical","Misc - Gail",
    "Misc - gail gown and cap","Movie","Others",
    "Remittance - Aron","Remittance - Aron tuition","Remittance - others",
    "Salinas Valley Dr","Shop - Amazon","Shop - Amazon returns","Shop - Goodwill",
    "Shop - Others","Shop - Marketplace","Shop - Paypal","Shop - Ross","Shop - Shein","Shop - Temu","Shop - Tiktok",
    "Shop - Whatnot",
    "Shop - AeroFlowDynamics","Shop - AliExpress","Shop - Alloyman Tools","Shop - Ambercup","Shop - Apple","Shop - Billetworkz","Shop - CM9S","Shop - Chic and Cozy Consignment","Shop - Cove","Shop - Crocs","Shop - Daiso","Shop - Dollar Tree","Shop - Fluxion","Shop - Fun Gifts","Shop - Groupon","Shop - Hella Kulit","Shop - HomeGoods","Shop - Hurley","Shop - IKEA","Shop - Kipling","Shop - LA Salon and Spa","Shop - LBC","Shop - LEGO","Shop - Lacoste","Shop - Life Time Off-Road","Shop - Limitless","Shop - Mac.bid","Shop - Marc Jacobs","Shop - Marshalls","Shop - Miss A","Shop - Nespresso","Shop - Nike","Shop - Old Navy","Shop - Original Deal Shop","Shop - Pickleball","Shop - Quality Prints USA","Shop - REI","Shop - Salinas Liquidations","Shop - Shapermint","Shop - Shoppawvia","Shop - Sudz","Shop - TJ Maxx","Shop - Target","Shop - The North Face","Shop - Tigresa Beauty","Shop - Tommy Hilfiger","Shop - Ulta","Shop - Uniqlo","Shop - Verizon","Shop - Victoria's Secret","Shop - eBay","VA expense","Vacation","Water",
]

DEBT = [
    "Affirm","Upgrade","CC - FPB","Auto Loan - Honda","Auto Loan - WRX","Auto Loan - Miata","CC - Ollo","CC - Aspire",
    "paypal - Alipay","paypal - pay in 4 Golden Nugget","CC - Credit 1","Klarna",
    "CC - Frontier card","CC - Whole foods","Afterpay","CC - One Pay",
    "CC - Citibank","CC - Capital 1","CC - paypal","CC - cashback MC",
    "Paypal pay in 4","Chase Pay in 4","CC - Mission Lane","CC - Citizen bank","CC - Chase Amazon Visa","CC - Venmo",
    "PayPal Pay Monthly","Jonathan Neil & Associates","CC - AAA Visa",
]

INCOME = [
    "Chris - Pension","Chris - UPS Income","Kristin - COO Income","Others - Income",
]

TRANSFER = [
    "Transfer - Checking to Savings","Transfer - Savings to Checking",
    "Transfer - Checking to PayPal","Transfer - PayPal to Checking",
    "Transfer - Checking to SoFi Savings",
    "Transfer - SoFi Savings to Checking","Transfer - Pass-through",
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
