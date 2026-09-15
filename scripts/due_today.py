#!/usr/bin/env python3
"""Print bills, debts, and loan-plan installments due today.

Mirrors the "This month's bills & loans" logic in artifact/index.html:
active bills/debts by dueDay, plus loan-schedule installments by exact date.
Paid/checked state lives in the live dashboard's database, not this repo,
so this only reflects what's due per the seed data on disk.
"""
import glob
import json
import sys
from datetime import date

SEED = "data/seed"


def load(pattern):
    for path in sorted(glob.glob(f"{SEED}/{pattern}")):
        with open(path) as f:
            yield json.load(f)


def main():
    today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    today_iso = today.isoformat()

    bills_due = [
        b for b in load("bill_*.json")
        if b.get("active") and b.get("dueDay") == today.day
    ]

    loans_due = []
    for plan in load("loanplan_*.json"):
        for inst in plan.get("installments", []):
            if inst.get("dueDate") == today_iso and not inst.get("paid"):
                loans_due.append((plan["name"], inst))

    if not bills_due and not loans_due:
        print(f"Nothing due today ({today_iso}).")
        return

    print(f"Due today ({today_iso}):")
    total = 0.0
    for b in sorted(bills_due, key=lambda b: -b["amount"]):
        print(f"  ${b['amount']:>8.2f}  {b['name']} ({b['group']})")
        total += b["amount"]
    for name, inst in sorted(loans_due, key=lambda x: -x[1]["amount"]):
        print(f"  ${inst['amount']:>8.2f}  {name} ({inst['n']}/{inst['total']})")
        total += inst["amount"]
    print(f"  {'-'*30}")
    print(f"  ${total:>8.2f}  total")


if __name__ == "__main__":
    main()
