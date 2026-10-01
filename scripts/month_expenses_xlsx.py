"""Build a month's expenses-by-category workbook (cash + cards) from exported ledger JSON.

Usage: python scripts/month_expenses_xlsx.py YYYY-MM CHECKING_JSON CARD_TX_DIR CREDIT_CARDS_DIR OUT.xlsx
"""
import glob, json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ym, checking_json, card_dir, cards_dir, out = sys.argv[1:6]
html = open('artifact/index.html').read()
ITEM = set(re.findall(r'"([^"]+)"', re.search(r'ITEMIZED_CARD_CATS = new Set\(\[(.*?)\]\)', html, re.S).group(1)))
names = {}
for f in glob.glob(cards_dir + '/*.json'):
    d = json.load(open(f)); n = d["name"]; l4 = d.get("last4", ""); names[f.split("/")[-1][:-5]] = n if l4 in n else f"{n} (...{l4})"

rows, pending = [], []
for e in json.load(open(checking_json))['entries']:
    if not e['date'].startswith(ym): continue
    if e.get('cleared') is False:
        if e['group'] not in ('Income', 'Transfer'): pending.append(e)
        continue
    if e['group'] in ('Income', 'Transfer') or (e['group'] == 'Debt' and any(e['category'] == c or e['category'].startswith(c + ' (') for c in ITEM)): continue
    rows.append((e['date'], e['description'].strip(), 'Checking', e['group'], e['category'], round(-e['amount'], 2)))
for f in sorted(glob.glob(card_dir + '/*.json')):
    d = json.load(open(f))
    for e in d['entries']:
        if e['type'] in ('purchase', 'fee') and e['date'].startswith(ym):
            rows.append((e['date'], e['description'].strip(), names.get(d['account'], d['account']), e['group'], e['category'], round(e['amount'], 2)))
rows.sort(key=lambda r: (r[0], r[2], r[1]))

F = 'Arial'; H = Font(name=F, bold=True, color='FFFFFF'); HF = PatternFill('solid', fgColor='1F4D3D')
GF = PatternFill('solid', fgColor='E1EDE5'); TF = PatternFill('solid', fgColor='D3DAC5'); thin = Side(style='thin', color='B0B8A4')
MON = '$#,##0.00;($#,##0.00);"-"'
wb = Workbook(); li = wb.active; li.title = 'Line Items'
for c, h in enumerate(['Date', 'Description', 'Source', 'Group', 'Category', 'Amount'], 1):
    x = li.cell(row=1, column=c, value=h); x.font = H; x.fill = HF; x.alignment = Alignment(horizontal='center')
for r, row in enumerate(rows, 2):
    for c, v in enumerate(row, 1): li.cell(row=r, column=c, value=v).font = Font(name=F)
    li.cell(row=r, column=6).number_format = MON
last = len(rows) + 1
li.cell(row=last + 1, column=5, value='Total').font = Font(name=F, bold=True)
x = li.cell(row=last + 1, column=6, value=f'=SUM(F2:F{last})'); x.font = Font(name=F, bold=True); x.number_format = MON
li.cell(row=last + 3, column=1, value='Amounts are money spent (positive); refunds and credits are negative. Card rows are purchases, fees and interest from card statements; checking payments to those cards are left out so nothing is counted twice.').font = Font(name=F, italic=True, size=9)
for col, w in zip('ABCDEF', [12, 48, 34, 15, 30, 14]): li.column_dimensions[col].width = w
li.freeze_panes = 'A2'; li.auto_filter.ref = f'A1:F{last}'

sm = wb.create_sheet('Summary', 0); LI = "'Line Items'"
sm['A1'] = f'Perez Household - {ym} Expenses'; sm['A1'].font = Font(name=F, bold=True, size=14)
sm['A2'] = 'Cash (checking) and card spending by category, from the Perez Household Ledger.'; sm['A2'].font = Font(name=F, italic=True, size=9)
for c, h in enumerate(['Group', 'Category', 'Cash', 'Card', 'Total'], 1):
    x = sm.cell(row=4, column=c, value=h); x.font = H; x.fill = HF; x.alignment = Alignment(horizontal='center')
r = 5; subs = []
for g in ['Monthly Bills', 'Expenses', 'Debt']:
    tot = {}
    for row in rows:
        if row[3] == g: tot[row[4]] = tot.get(row[4], 0) + row[5]
    if not tot: continue
    start = r
    for cat in sorted(tot, key=lambda k: -tot[k]):
        sm.cell(row=r, column=1, value=g); sm.cell(row=r, column=2, value=cat)
        base = f'{LI}!$F$2:$F${last},{LI}!$D$2:$D${last},$A{r},{LI}!$E$2:$E${last},$B{r},{LI}!$C$2:$C${last}'
        sm.cell(row=r, column=3, value=f'=SUMIFS({base},"Checking")')
        sm.cell(row=r, column=4, value=f'=SUMIFS({base},"<>Checking")')
        sm.cell(row=r, column=5, value=f'=C{r}+D{r}')
        for c in range(1, 6): sm.cell(row=r, column=c).font = Font(name=F)
        r += 1
    sm.cell(row=r, column=1, value=f'Total {g}')
    for c, L in [(3, 'C'), (4, 'D'), (5, 'E')]: sm.cell(row=r, column=c, value=f'=SUM({L}{start}:{L}{r - 1})')
    for c in range(1, 6): x = sm.cell(row=r, column=c); x.font = Font(name=F, bold=True); x.fill = GF
    subs.append(r); r += 2
sm.cell(row=r, column=1, value='GRAND TOTAL')
for c, L in [(3, 'C'), (4, 'D'), (5, 'E')]: sm.cell(row=r, column=c, value='=' + '+'.join(f'{L}{s}' for s in subs))
for c in range(1, 6): x = sm.cell(row=r, column=c); x.font = Font(name=F, bold=True, size=12); x.fill = TF; x.border = Border(top=thin, bottom=thin)
grand = r; r += 1
sm.cell(row=r, column=2, value='Check: equals Line Items total').font = Font(name=F, italic=True, size=9)
sm.cell(row=r, column=5, value=f'=IF(ROUND(E{grand}-{LI}!F{last + 1},2)=0,"OK","MISMATCH")').font = Font(name=F, italic=True, size=9)
for rr in range(5, grand + 1):
    for c in (3, 4, 5): sm.cell(row=rr, column=c).number_format = MON
if pending:
    r += 2
    sm.cell(row=r, column=1, value='Not counted yet (checked off or held, but not posted in Chase) - not included above').font = Font(name=F, bold=True); r += 1
    ps = r
    for e in pending:
        sm.cell(row=r, column=1, value=e['date']).font = Font(name=F)
        sm.cell(row=r, column=2, value=e['description']).font = Font(name=F)
        x = sm.cell(row=r, column=5, value=round(-e['amount'], 2)); x.font = Font(name=F); x.number_format = MON; r += 1
    sm.cell(row=r, column=2, value='Total not counted yet').font = Font(name=F, bold=True)
    x = sm.cell(row=r, column=5, value=f'=SUM(E{ps}:E{r - 1})'); x.font = Font(name=F, bold=True); x.number_format = MON
r += 2
for n in ['Notes:',
          '- Cash = paid from Chase checking (...0861). Card = purchases, fees and interest on credit card statements, by transaction date.',
          '- Credit card payments from checking are left out, since the card purchases themselves are counted (no double counting).',
          '- Income and transfers (PayPal, savings) are not expenses and are excluded.',
          '- Debt includes Affirm, Klarna, Chase Pay in 4, auto loans and card fees/interest. Refunds and credits show as negatives.',
          "- Card statements only cover purchases through each card's closing date; later purchases appear on the next statements."]:
    sm.cell(row=r, column=1, value=n).font = Font(name=F, size=9, bold=(n == 'Notes:')); r += 1
for col, w in zip('ABCDE', [16, 34, 14, 14, 14]): sm.column_dimensions[col].width = w
sm.freeze_panes = 'A5'
wb.save(out)
print('rows', len(rows), 'total', round(sum(x[5] for x in rows), 2), 'pending', len(pending))
