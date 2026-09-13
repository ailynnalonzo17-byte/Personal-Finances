"""Turn parsed credit-card statement data (scratchpad/parsed_cards.json, plus
the Chase Amazon Visa statement handled separately) into the DB documents the
artifact needs: one `credit_cards/<key>` doc per card (latest statement) and
one `card_transactions/<key>_<month>` doc per card per statement month, with
every transaction categorized via categorize_card_tx.

Run from the repo root: python3 scripts/build_card_data.py
Writes JSON files under data/seed/ (credit_card_*.json, cardtx_*.json) AND
prints a single JSON file listing every doc for a write_db batch.
"""
import json, re, sys, os
from dateutil import parser as dtparser

sys.path.insert(0, os.path.dirname(__file__))
from categorize_card_tx import categorize_card_entry

SCRATCH = "/tmp/claude-0/-home-user-Personal-Finances/bb1444b0-ea24-540b-ac08-9598707e0312/scratchpad"
SEED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "seed")

HOLDER = {
    "paypal_1": "Christopher", "paypal_cashback_mc": "Christopher", "onepay": "Ailynn",
    "ollo": "Christopher", "mission_lane": "Christopher", "aspire": "Christopher",
    "credit1_4838": "Christopher", "credit1_4352": "Christopher", "frontier": "Ailynn",
    "citi": "Christopher", "capital1": "Ailynn", "fpb": "Christopher", "chase_amazon": "Christopher",
}
ISSUER = {
    "paypal_1": "Synchrony Bank", "paypal_cashback_mc": "Synchrony Bank", "onepay": "Synchrony Bank",
    "ollo": "Ollo Card Services", "mission_lane": "Transportation Alliance Bank (TAB Bank)",
    "aspire": "Aspire Mastercard / MSB", "credit1_4838": "Credit One Bank", "credit1_4352": "Credit One Bank",
    "frontier": "Barclays Bank Delaware", "citi": "Citibank", "capital1": "Capital One",
    "fpb": "First Premier Bank", "chase_amazon": "Chase",
}
DISPLAY_NAME = {
    "paypal_1": "PayPal Credit", "paypal_cashback_mc": "PayPal Cashback Mastercard",
    "onepay": "OnePay CashRewards", "ollo": "Ollo Credit Card", "mission_lane": "Mission Lane Visa",
    "aspire": "Aspire Mastercard", "credit1_4838": "Credit One Bank (...4838)",
    "credit1_4352": "Credit One Bank (...4352)", "frontier": "Frontier Airlines World Mastercard",
    "citi": "Costco Anywhere Visa (Citi)", "capital1": "Capital One Quicksilver",
    "fpb": "First Premier Bank", "chase_amazon": "Chase Amazon Prime Visa",
}
LAST4 = {
    "paypal_1": "1164", "paypal_cashback_mc": "2682", "onepay": "0461", "ollo": "3450",
    "mission_lane": "6793", "aspire": "5551", "credit1_4838": "4838", "credit1_4352": "4352",
    "frontier": "6936", "citi": "3533", "capital1": "5643", "fpb": "3035", "chase_amazon": "1755",
}

def flexdate(s):
    if not s: return None
    return dtparser.parse(s).strftime("%Y-%m-%d")

def slug(s):
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))

def main():
    parsed = json.load(open(os.path.join(SCRATCH, "parsed_cards.json")))

    # Add the Chase Amazon Visa statement (parsed separately, single month).
    parsed.append({
        "file": "chase_sept.txt", "issuer": "Chase", "category": "CC - Chase Amazon Visa",
        "account_key": "chase_amazon", "last4": "1755", "name": "Chase Amazon Prime Visa",
        "statement_date": "08/18/26", "due_date": "09/15/26", "apr": 27.49, "new_balance": 30.00,
        "min_payment": 30.00, "n_tx": 1,
        "transactions": [{"date_md": "08/14", "ref": "", "desc": "CARE USA CARE.ORG GA", "amount": 30.00}],
    })

    by_account = {}
    for r in parsed:
        by_account.setdefault(r["account_key"], []).append(r)

    card_docs = {}       # credit_cards/<key>.json
    cardtx_docs = {}     # cardtx_<key>_<month>.json
    batch_writes = []

    for acct, statements in by_account.items():
        # sort by statement date to find the latest
        for s in statements:
            s["_iso_stmt"] = flexdate(s["statement_date"])
        statements.sort(key=lambda s: s["_iso_stmt"] or "")
        latest = statements[-1]
        category = latest["category"]

        card_doc = {
            "name": DISPLAY_NAME.get(acct, latest["name"]),
            "issuer": ISSUER.get(acct, latest["issuer"]),
            "holder": HOLDER.get(acct, ""),
            "last4": LAST4.get(acct, latest.get("last4", "")),
            "category": category,
            "statementDate": latest["_iso_stmt"],
            "balance": latest["new_balance"],
            "minPayment": latest["min_payment"],
            "dueDate": flexdate(latest["due_date"]),
            "apr": latest["apr"],
            "source": f"Statement PDF you uploaded ({len(statements)} month(s) on file)",
        }
        card_docs[acct] = card_doc

        for s in statements:
            month = s["_iso_stmt"][:7] if s["_iso_stmt"] else "unknown"
            entries = []
            for i, t in enumerate(s["transactions"]):
                # Attach a year using the statement date's year/month for MM/DD-only dates.
                date_iso = None
                if s["_iso_stmt"]:
                    y = int(s["_iso_stmt"][:4])
                    try:
                        mm, dd = t["date_md"].split("/") if "/" in t["date_md"] else (None, None)
                        if mm and mm.isdigit():
                            date_iso = dtparser.parse(f"{t['date_md']}/{y}").strftime("%Y-%m-%d")
                        else:
                            date_iso = dtparser.parse(f"{t['date_md']} {y}").strftime("%Y-%m-%d")
                        # Handle month-end wraparound (Dec txn on a Jan-closing statement etc.)
                        if date_iso[:7] > month:
                            date_iso = dtparser.parse(f"{t['date_md']}/{y-1}" if '/' in t['date_md'] else f"{t['date_md']} {y-1}").strftime("%Y-%m-%d")
                    except Exception:
                        date_iso = s["_iso_stmt"]
                cat, grp, conf, note, etype = categorize_card_entry(t["desc"], t["amount"], category)
                entries.append({
                    "id": f"{acct}_{month}_{i}",
                    "date": date_iso or s["_iso_stmt"],
                    "description": t["desc"],
                    "amount": t["amount"],
                    "category": cat, "group": grp, "confidence": conf, "note": note,
                    "type": etype, "source": "Card statement PDF you uploaded",
                })
            doc_id = f"{acct}_{month}"
            cardtx_docs[doc_id] = {"account": acct, "month": month, "cardCategory": category, "entries": entries}

    os.makedirs(SEED_DIR, exist_ok=True)
    for acct, doc in card_docs.items():
        with open(os.path.join(SEED_DIR, f"credit_card_{acct}.json"), "w") as f:
            json.dump(doc, f, indent=2)
    for doc_id, doc in cardtx_docs.items():
        with open(os.path.join(SEED_DIR, f"cardtx_{doc_id}.json"), "w") as f:
            json.dump(doc, f, indent=2)

    print(f"Wrote {len(card_docs)} credit_cards docs and {len(cardtx_docs)} card_transactions docs to {SEED_DIR}")
    print("Cards:", sorted(card_docs.keys()))

if __name__ == "__main__":
    main()
