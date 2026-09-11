import csv, sys, datetime
sys.path.insert(0, "scripts")
from build_master_categories import flat, ALL_GROUPS

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

FONT = "Arial"
CURRENCY = '$#,##0.00;[RED]($#,##0.00)'
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name=FONT, bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(name=FONT, bold=True, size=14, color="1F4E78")
SUB_FONT = Font(name=FONT, italic=True, size=9, color="666666")
BOLD = Font(name=FONT, bold=True, size=10)
NORMAL = Font(name=FONT, size=10)
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
INPUT_FONT = Font(name=FONT, size=10, color="0000FF")
GROUP_FILL = {
    "Monthly Bills": PatternFill("solid", fgColor="DDEBF7"),
    "Expenses": PatternFill("solid", fgColor="E2EFDA"),
    "Debt": PatternFill("solid", fgColor="FCE4D6"),
    "Income": PatternFill("solid", fgColor="FFF2CC"),
    "Transfer": PatternFill("solid", fgColor="EDEDED"),
}
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER

def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

wb = Workbook()

# ============================================================ Dashboard
ws = wb.active
ws.title = "Dashboard"
ws["A1"] = "Personal Finance Tracker"
ws["A1"].font = TITLE_FONT
ws["A2"] = "Source: Chase checking ...0861, statement activity 05/01/2026 - 08/31/2026. Built from your uploaded CSV."
ws["A2"].font = SUB_FONT
ws["A3"] = "Yellow cells are for you to type into. Everything else is a formula and updates itself."
ws["A3"].font = SUB_FONT

r = 5
ws.cell(row=r, column=1, value="This statement period, by group (Checking only)").font = BOLD
r += 1
headers = ["Group", "Total", "# Transactions"]
for i, h in enumerate(headers, start=1):
    ws.cell(row=r, column=i, value=h)
style_header_row(ws, r, len(headers))
group_row_start = r + 1
for i, g in enumerate(["Income", "Monthly Bills", "Expenses", "Debt", "Transfer"]):
    rr = group_row_start + i
    ws.cell(row=rr, column=1, value=g).font = NORMAL
    ws.cell(row=rr, column=2, value=f'=SUMIF(Checking!$H$5:$H$991,A{rr},Checking!$D$5:$D$991)').number_format = CURRENCY
    ws.cell(row=rr, column=3, value=f'=COUNTIF(Checking!$H$5:$H$991,A{rr})')
    for c in (1, 2, 3):
        ws.cell(row=rr, column=c).border = BORDER
group_row_end = group_row_start + 4

r = group_row_end + 2
ws.cell(row=r, column=1, value="Net cash flow this period (Income + Bills + Expenses + Debt, Transfers excluded)").font = BOLD
ws.cell(row=r, column=2, value=f'=SUMIF(A{group_row_start}:A{group_row_end},"Income",B{group_row_start}:B{group_row_end})'
                                f'+SUMIF(A{group_row_start}:A{group_row_end},"Monthly Bills",B{group_row_start}:B{group_row_end})'
                                f'+SUMIF(A{group_row_start}:A{group_row_end},"Expenses",B{group_row_start}:B{group_row_end})'
                                f'+SUMIF(A{group_row_start}:A{group_row_end},"Debt",B{group_row_start}:B{group_row_end})')
ws.cell(row=r, column=2).number_format = CURRENCY
ws.cell(row=r, column=2).font = BOLD

r += 3
ws.cell(row=r, column=1, value="Needs your review").font = BOLD
r += 1
ws.cell(row=r, column=1, value="Transactions I could not confidently categorize (flagged Confidence = R)")
ws.cell(row=r, column=1).font = NORMAL
r += 1
ws.cell(row=r, column=1, value="Count:")
ws.cell(row=r, column=2, value='=COUNTIF(Checking!$I$5:$I$991,"R")')
r += 1
ws.cell(row=r, column=1, value="Total $ amount flagged:")
ws.cell(row=r, column=2, value='=SUMIF(Checking!$I$5:$I$991,"R",Checking!$D$5:$D$991)')
ws.cell(row=r, column=2).number_format = CURRENCY
r += 1
ws.cell(row=r, column=1, value="-> Go to the Checking sheet, use the filter on column I (Confidence), select \"R\", and read column J (Note) for what I need from you. Full list is also in the 'Open Questions' tab.").font = SUB_FONT

r += 3
ws.cell(row=r, column=1, value="See also:  Accounts & Balances  |  Categories  |  Checking  |  Savings  |  PayPal  |  Open Questions").font = SUB_FONT

autosize(ws, [55, 16, 16])

# ============================================================ Accounts & Balances
ws = wb.create_sheet("Accounts & Balances")
ws["A1"] = "Accounts & Balances"
ws["A1"].font = TITLE_FONT
ws["A2"] = "Type your real, current balance from each account into the yellow cells. The Difference row tells you if this tracker matches reality."
ws["A2"].font = SUB_FONT

def account_block(ws, row, title, starting_balance, tx_sheet, has_data, note=""):
    ws.cell(row=row, column=1, value=title).font = BOLD
    ws.cell(row=row, column=1).fill = GROUP_FILL["Transfer"]
    row += 1
    ws.cell(row=row, column=1, value="Starting balance (before earliest imported transaction)")
    c = ws.cell(row=row, column=2, value=starting_balance)
    c.number_format = CURRENCY; c.font = INPUT_FONT; c.fill = INPUT_FILL
    start_row = row
    row += 1
    ws.cell(row=row, column=1, value="+ Sum of all transactions imported")
    tx_range = {"Checking": "Checking!$D$5:$D$991", "Savings": "Savings!$D$5:$D$304",
                "PayPal": "PayPal!$D$5:$D$304"}.get(tx_sheet)
    if has_data:
        ws.cell(row=row, column=2, value=f'=SUM({tx_range})')
    else:
        ws.cell(row=row, column=2, value=0)
    ws.cell(row=row, column=2).number_format = CURRENCY
    sum_row = row
    row += 1
    ws.cell(row=row, column=1, value="Balance this tracker computes").font = BOLD
    ws.cell(row=row, column=2, value=f'=B{start_row}+B{sum_row}').number_format = CURRENCY
    ws.cell(row=row, column=2).font = BOLD
    computed_row = row
    row += 1
    ws.cell(row=row, column=1, value="Actual balance per your bank / account (type it in, and the date)")
    c = ws.cell(row=row, column=2, value=None)
    c.number_format = CURRENCY; c.font = INPUT_FONT; c.fill = INPUT_FILL
    c2 = ws.cell(row=row, column=3, value=None)
    c2.font = INPUT_FONT; c2.fill = INPUT_FILL
    ws.cell(row=row, column=3).number_format = "mm/dd/yyyy"
    ws.cell(row=row, column=1).comment = None
    actual_row = row
    row += 1
    ws.cell(row=row, column=1, value="Difference (should be $0.00 once you enter the actual balance above)").font = BOLD
    ws.cell(row=row, column=2, value=f'=IF(B{actual_row}="","enter actual balance above",B{actual_row}-B{computed_row})')
    ws.cell(row=row, column=2).number_format = CURRENCY
    diff_row = row
    row += 1
    if note:
        ws.cell(row=row, column=1, value=note).font = SUB_FONT
        row += 1
    return row + 1

row = 4
row = account_block(ws, row, "CHECKING  (Chase ...0861)", 2043.65, "Checking", True,
    "Starting balance is computed from Chase's own running balance on your statement (the balance just before your oldest imported transaction).")
row = account_block(ws, row, "SAVINGS  (Chase ...5953)", 0, "Savings", True,
    "No savings statement imported yet. Once you give me one, I'll set the correct starting balance and this will total itself. "
    "For now this cross-checks against the transfers Checking already shows below.")
row = account_block(ws, row, "PAYPAL", 0, "PayPal", True,
    "No PayPal statement/export imported yet. Same as Savings above - give me one and I'll wire it up.")

row += 1
ws.cell(row=row, column=1, value="Cross-check: transfers Checking shows moving to/from other accounts").font = BOLD
row += 1
ws.cell(row=row, column=1, value="Checking -> Savings, this period")
ws.cell(row=row, column=2, value='=-SUMIF(Checking!$G$5:$G$991,"Transfer - Checking to Savings",Checking!$D$5:$D$991)').number_format = CURRENCY
row += 1
ws.cell(row=row, column=1, value="Savings -> Checking, this period")
ws.cell(row=row, column=2, value='=SUMIF(Checking!$G$5:$G$991,"Transfer - Savings to Checking",Checking!$D$5:$D$991)').number_format = CURRENCY
row += 1
ws.cell(row=row, column=1, value="Checking -> PayPal, this period")
ws.cell(row=row, column=2, value='=-SUMIF(Checking!$G$5:$G$991,"Transfer - Checking to PayPal",Checking!$D$5:$D$991)').number_format = CURRENCY
row += 1
ws.cell(row=row, column=1, value="PayPal -> Checking, this period")
ws.cell(row=row, column=2, value='=SUMIF(Checking!$G$5:$G$991,"Transfer - PayPal to Checking",Checking!$D$5:$D$991)').number_format = CURRENCY
row += 1
ws.cell(row=row, column=1, value="When you add Savings/PayPal statements, these two numbers should match what those accounts show for the same transfers.").font = SUB_FONT

autosize(ws, [62, 16, 14])

# ============================================================ Categories
ws = wb.create_sheet("Categories")
ws["A1"] = "Categories"
ws["A1"].font = TITLE_FONT
ws["A2"] = "The full category list (your list, plus Income and Transfer groups needed for reconciliation). Totals pull from all three transaction sheets."
ws["A2"].font = SUB_FONT
headers = ["Group", "Category", "Checking Total", "Savings Total", "PayPal Total", "Combined Total", "# Transactions (Checking)"]
hr = 4
for i, h in enumerate(headers, start=1):
    ws.cell(row=hr, column=i, value=h)
style_header_row(ws, hr, len(headers))
cats = flat()
for i, (g, c) in enumerate(cats):
    rr = hr + 1 + i
    ws.cell(row=rr, column=1, value=g).font = NORMAL
    ws.cell(row=rr, column=2, value=c).font = NORMAL
    ws.cell(row=rr, column=3, value=f'=SUMIF(Checking!$G$5:$G$991,B{rr},Checking!$D$5:$D$991)').number_format = CURRENCY
    ws.cell(row=rr, column=4, value=f'=SUMIF(Savings!$G$5:$G$304,B{rr},Savings!$D$5:$D$304)').number_format = CURRENCY
    ws.cell(row=rr, column=5, value=f'=SUMIF(PayPal!$G$5:$G$304,B{rr},PayPal!$D$5:$D$304)').number_format = CURRENCY
    ws.cell(row=rr, column=6, value=f'=C{rr}+D{rr}+E{rr}').number_format = CURRENCY
    ws.cell(row=rr, column=7, value=f'=COUNTIF(Checking!$G$5:$G$991,B{rr})')
    fill = GROUP_FILL.get(g)
    for c_ in range(1, 8):
        cell = ws.cell(row=rr, column=c_)
        cell.border = BORDER
        if fill:
            cell.fill = fill
cat_last_row = hr + len(cats)
ws.freeze_panes = "A5"
autosize(ws, [16, 32, 15, 15, 15, 16, 20])
CATEGORY_RANGE = f"Categories!$B${hr+1}:$B${cat_last_row}"

# ============================================================ Transaction sheets
def build_tx_sheet(name, csv_path=None, account_label=""):
    ws = wb.create_sheet(name)
    ws["A1"] = f"{name} Transactions"
    ws["A1"].font = TITLE_FONT
    if csv_path:
        ws["A2"] = f"Imported from your Chase CSV. {account_label}"
    else:
        ws["A2"] = f"Template, ready for your next {name} statement or export - paste rows in starting at row 5, columns A-F (Account, Date, Description, Amount, Type, source Balance). Then set Category in column G."
    ws["A2"].font = SUB_FONT

    headers = ["Account", "Date", "Description", "Amount", "Type", "Source Balance",
               "Category", "Group", "Confidence", "Note"]
    hr = 4
    for i, h in enumerate(headers, start=1):
        ws.cell(row=hr, column=i, value=h)
    style_header_row(ws, hr, len(headers))

    n = 0
    if csv_path:
        rows = list(csv.DictReader(open(csv_path)))
        n = len(rows)
        for i, r in enumerate(rows):
            rr = hr + 1 + i
            ws.cell(row=rr, column=1, value=r["Account"]).font = NORMAL
            d = datetime.datetime.strptime(r["Date"], "%m/%d/%Y")
            ws.cell(row=rr, column=2, value=d).number_format = "mm/dd/yyyy"
            ws.cell(row=rr, column=3, value=r["Description"]).font = NORMAL
            ws.cell(row=rr, column=4, value=float(r["Amount"])).number_format = CURRENCY
            ws.cell(row=rr, column=5, value=r["Type"]).font = NORMAL
            ws.cell(row=rr, column=6, value=float(r["ChaseBalance"])).number_format = CURRENCY
            ws.cell(row=rr, column=7, value=r["Category"]).font = NORMAL
            ws.cell(row=rr, column=8, value=f'=IFERROR(INDEX(Categories!$A$5:$A$93,MATCH(G{rr},Categories!$B$5:$B$93,0)),"")')
            ws.cell(row=rr, column=9, value=r["Confidence"]).font = NORMAL
            ws.cell(row=rr, column=10, value=r["Note"]).font = NORMAL

    last_row = hr + max(n, 300)  # leave room to paste more rows in later
    dv = DataValidation(type="list", formula1=CATEGORY_RANGE, allow_blank=True, showErrorMessage=True)
    dv.error = "Pick a category from the dropdown (see the Categories tab for the full list)."
    ws.add_data_validation(dv)
    dv.add(f"G{hr+1}:G{last_row}")

    # Group formula also for any pasted-in future rows
    for rr in range(hr + 1 + n, last_row + 1):
        ws.cell(row=rr, column=8, value=f'=IFERROR(INDEX(Categories!$A$5:$A$93,MATCH(G{rr},Categories!$B$5:$B$93,0)),"")')

    # conditional formatting on Confidence column
    conf_col = f"I{hr+1}:I{last_row}"
    ws.conditional_formatting.add(conf_col, CellIsRule(operator="equal", formula=['"R"'],
        fill=PatternFill("solid", fgColor="FFC7CE")))
    ws.conditional_formatting.add(conf_col, CellIsRule(operator="equal", formula=['"D"'],
        fill=PatternFill("solid", fgColor="FFEB9C")))
    ws.conditional_formatting.add(conf_col, CellIsRule(operator="equal", formula=['"H"'],
        fill=PatternFill("solid", fgColor="C6EFCE")))

    ws.freeze_panes = f"A{hr+1}"
    ws.auto_filter.ref = f"A{hr}:J{max(hr+n, hr+1)}"
    autosize(ws, [16, 12, 46, 12, 16, 13, 24, 14, 11, 55])
    return ws

build_tx_sheet("Checking", "data/processed/checking_categorized.csv", "Account ...0861, 05/01/2026 - 08/31/2026.")
build_tx_sheet("Savings")
build_tx_sheet("PayPal")

# ============================================================ Open Questions
ws = wb.create_sheet("Open Questions")
ws["A1"] = "Open Questions - things I guessed and need you to confirm"
ws["A1"].font = TITLE_FONT
ws["A2"] = "Answer these and I'll fix the categorization in one pass. Everything else in the tracker already reflects my best-confidence read of your statement."
ws["A2"].font = SUB_FONT

questions = [
 ("Income", "Chris' pension", "\"TEAMSTERS PAYMENTS\", ~$4,275, lands on the 3rd of each month.",
  "Is this Chris' pension? If not, what is it, and which line IS the pension?"),
 ("Income", "Your income from Kristin (COO)", "Nothing in this statement is labeled Kristin or similarly.",
  "Which deposit is this? A name, company, or approximate $ amount would let me find and tag it."),
 ("Income", "Key Salary", "\"UNITED PARCEL SE PAYROLL\", ~$2,275, twice in this statement.",
  "Is this your own UPS paycheck / Key Salary? "),
 ("Debt", "Auto Loan - Honda", "\"WestlakeSvcs\" (Aug) and \"WF PAYMENT\" (Jun-Jul) - same two amounts each time, ~$223.53 + ~$276.47, paid together.",
  "Is this the Honda auto loan (servicer changed from WF to Westlake)? Or a different loan?"),
 ("Debt", "CC - cashback MC", "\"Payment to Chase card ending in 1755\", $409.50, one time.",
  "Is this your Chase cashback Mastercard? If you have more than one Chase card, which one?"),
 ("Debt", "CC - Frontier card", "\"BARCLAYCARD US CREDITCARD\", 4 times, ~$1,099.59 - $2,510 range.",
  "Confirming this Barclaycard is the Frontier Airlines card and not a different Barclays card."),
 ("Expenses", "\"ALA 0908\"", "\"Online Payment ... To ALA 0908\", $706.36, monthly (recurring).",
  "What is this? A loan, rent, tuition? None of your categories obviously fit - tell me and I'll add or map it."),
 ("Transfer", "SoFi / SMBS transfers", "\"SoFi Bank TRANSFER CPerez\" and \"SMBS Account TRANSFER CPerez\" - large, $1,000 to $20,065.",
  "What account is this (savings, investment)? Should I track it as a 4th account alongside Checking/Savings/PayPal?"),
 ("Expenses", "Remittances (Taptap Send, Sendwave, LBC)", "~20 Taptap Send + 8 Sendwave + 1 LBC transactions, varying amounts, recipient not shown.",
  "Are these all going to Aron, or a mix of Aron / Aron's tuition / others? If a mix, is there a way to tell them apart (e.g. amount, day of month)?"),
 ("Expenses", "Zelle payments", "14+ recurring to/from RHIAN ABIGAIL ALMO, 5 from Katrina T Perez, 4 from Angelynn Flora, plus Dennis Chua, Doris 2, Kyle Kromer, Ivory Janine Morales, Alvin Anthony Alonzo, Maria Bravo, Rose Ann Alonzo, Harold Alvarado, and others.",
  "Tell me who each of these is (family, helper, etc.) and I'll map recurring ones to a category - e.g. is Gail one of these names under something I haven't matched?"),
 ("Expenses", "Paper checks", "Checks 283-287, 353-358, no payee shown. Amounts: mostly $500, plus $1,800, $2,000, $2,200 x2, $180, and one blank $7,500.",
  "Who were these written to? The recurring $500 ones in particular - could that be Rent?"),
 ("Debt", "\"paypal - pay in 4 Golden Nugget\"", "Not found in this statement - only a one-off $51.98 Golden Nugget Hotel charge (looks like Vacation) and generic recurring PayPal Pay-in-4 charges (already mapped to \"Paypal pay in 4\").",
  "Is this a specific purchase plan, or should I just fold it into \"Paypal pay in 4\"?"),
 ("Debt", "CC - Whole foods, CC - cashback MC (if not the Chase card above)", "Not found in this statement.",
  "These may just not have activity in this particular statement - nothing to do unless you tell me otherwise."),
]

hdr = ["Group", "Item", "What I found", "What I need from you"]
hr = 4
for i, h in enumerate(hdr, start=1):
    ws.cell(row=hr, column=i, value=h)
style_header_row(ws, hr, len(hdr))
for i, (g, item, found, ask) in enumerate(questions):
    rr = hr + 1 + i
    ws.cell(row=rr, column=1, value=g).font = NORMAL
    ws.cell(row=rr, column=2, value=item).font = BOLD
    ws.cell(row=rr, column=3, value=found).font = NORMAL
    ws.cell(row=rr, column=4, value=ask).font = NORMAL
    for c_ in range(1, 5):
        cell = ws.cell(row=rr, column=c_)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = BORDER
    ws.row_dimensions[rr].height = 45

ws.freeze_panes = "A5"
autosize(ws, [12, 26, 55, 55])

wb.save("Personal_Finance_Tracker.xlsx")
print("saved")
