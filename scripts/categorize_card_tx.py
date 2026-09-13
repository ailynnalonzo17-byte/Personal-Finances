"""Categorize individual credit-card statement transactions into the same
category list used for cash/checking transactions (scripts/categorize.py),
so card and cash spend can be combined into one category-by-month view.

Payments TO the card (paying down the balance) are excluded from category
spend entirely - the checking side already books those as a "CC - X" Debt
line when the payment posts there, so counting them again here would double
count. Card-issued fees (annual/late/monthly fee) are booked to that card's
own Debt category, since they're a cost of carrying that card, not a
purchase. Everything else is a purchase and gets categorized the same way
a cash transaction would be.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from categorize import COMPILED

PAYMENT_RE = re.compile(
    r"PAYMENT.*THANK YOU|PAYMENT.*AUTOPAY|^AUTOPAY|AUTO PAYMENT|AUTOMATIC PAYMENT|"
    r"^ONLINE PAYMENT|^ONLINE ONE TIME PAYMENT|^INTERNET PAYMENT|"
    r"CAPITAL ONE AUTOPAY|CAPITAL ONE.*PYMT|PAYMENT RECEIVED", re.I)
FEE_RE = re.compile(r"ANNUAL FEE|LATE FEE|MONTHLY FEE", re.I)
REWARD_RE = re.compile(r"CASH\s?BACK REWARD|REWARDS? REDEE?MED|REWARD REDEMPTION", re.I)

def categorize_card_entry(desc, amount, card_category):
    """Returns (category, group, confidence, note, entry_type)."""
    if PAYMENT_RE.search(desc):
        return card_category, "Debt", "H", "Payment toward this card - already booked on the checking side, excluded from category spend", "payment"
    if REWARD_RE.search(desc):
        return card_category, "Debt", "H", "Cashback/rewards redemption credit - not spend, excluded from category totals", "reward"
    if FEE_RE.search(desc):
        return card_category, "Debt", "H", "Fee charged by this card", "fee"
    for pat, cat, grp, conf, note in COMPILED:
        if pat.search(desc):
            return cat, grp, conf, note, "purchase"
    return "Others", "Expenses", "R", "Card purchase - merchant not recognized, please tell me what this is", "purchase"

if __name__ == "__main__":
    tests = [
        ("PAYMENT - THANK YOU", -100, "CC - Citibank"),
        ("WM SUPERCENTER #5751 SALINAS CA", 154.94, "CC - Capital 1"),
        ("ANNUAL FEE     06/26 THROUGH 06/26", 8.25, "CC - Credit 1"),
        ("STARLUX  101892106486648 TAIPEI ALMO AILYNN ALONZO MRS", 2375.05, "CC - Frontier card"),
    ]
    for desc, amt, cc in tests:
        print(desc[:40], "->", categorize_card_entry(desc, amt, cc))
