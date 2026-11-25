#!/usr/bin/env python3
"""Spend ledger for real-card payments (payment-human flow): one row per real-card attempt, so every
payment can be found and refunded, and a run is refused when the next payment would go over the budget.

Both files are per tester (this computer only) and ignored by git:
  PROJECT/spend/budget.md   the tester's budget, written by a PERSON (the agent never edits it)
  PROJECT/spend/ledger.csv  one row per real-card attempt (opens in Excel; UTF-8 with BOM)

Usage:
  spend_ledger.py check <amount> [--currency USD]
        Exit 0 = OK to open the payment window, 3 = refused (over the cap or the budget), 2 = budget not set.
  spend_ledger.py add --site S --run RUN --tc TC --item ITEM --amount A --status paid|declined|unclear
                      [--currency USD] [--order-id ID] [--message TEXT]
        Adds a row (or updates the row of the same run + TC). Prints the row ID, for example P-0003.
  spend_ledger.py set <ID> [--refund requested|confirmed] [--refund-date YYYY-MM-DD]
                      [--status paid|declined|unclear|hold|released] [--order-id ID] [--notes TEXT]
        Updates a row, for example when the refund was requested or is confirmed on the card.
  spend_ledger.py list
        Prints every row, the open spend and what is left of the budget.

What counts against the budget ("open spend"):
  - paid      until its refund is "confirmed" (a refund that is only requested still counts),
  - unclear   until a person sets the real status,
  - hold      a declined attempt the bank still holds, until set to "released".
  A declined attempt does not count, unless a person sets it to "hold".
"""
import argparse
import csv
import datetime
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
SPEND = PROJECT / "spend"
BUDGET = SPEND / "budget.md"
LEDGER = SPEND / "ledger.csv"
FIELDS = ["id", "date", "site", "run", "tc", "item", "amount", "currency", "status", "order_id", "message",
          "refund_status", "refund_date", "notes"]
STATUSES = {"paid", "declined", "unclear", "hold", "released"}
OPEN = {"unclear", "hold"}

BUDGET_TEMPLATE = """# Card spending budget (this computer's tester only, ignored by git)

Only a PERSON edits this file; the agent never changes it. Amounts are in USD.
The budget must be lower than the card's own limit, to leave room for holds and fees.

- card-limit: USD 0
- budget: USD 0
- per-payment-cap: USD 0

card-limit: the limit the bank set on your card (for example USD 50).
budget: the most that may be open at once (paid and not yet refunded, plus holds). Below card-limit.
per-payment-cap: the largest single payment the agent may open a payment window for.
"""


def money(text):
    try:
        return Decimal(re.sub(r"[^\d.]", "", str(text)) or "x").quantize(Decimal("0.01"))
    except InvalidOperation:
        sys.exit(f"not an amount: {text!r}")


def read_budget():
    if not BUDGET.exists():
        SPEND.mkdir(exist_ok=True)
        BUDGET.write_text(BUDGET_TEMPLATE, encoding="utf-8")
    vals = dict(re.findall(r"^-\s*(card-limit|budget|per-payment-cap)\s*:\s*USD\s*([\d.]+)", BUDGET.read_text(encoding="utf-8"), re.M | re.I))
    return {k.lower(): money(v) for k, v in vals.items()}


def read_rows():
    if not LEDGER.exists():
        return []
    with LEDGER.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(rows):
    SPEND.mkdir(exist_ok=True)
    tmp = LEDGER.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in rows)
    tmp.replace(LEDGER)


def counts(r):
    st = r.get("status", "")
    return (st == "paid" and r.get("refund_status", "") != "confirmed") or st in OPEN


def open_spend(rows):
    return sum((money(r["amount"]) for r in rows if counts(r)), Decimal("0.00"))


def check(amount, currency):
    b = read_budget()
    budget, cap, limit = b.get("budget", Decimal(0)), b.get("per-payment-cap", Decimal(0)), b.get("card-limit", Decimal(0))
    if budget <= 0 or cap <= 0 or limit <= 0:
        print(f"BUDGET NOT SET: a person writes card-limit, budget and per-payment-cap (USD) in {BUDGET}")
        return 2
    if budget >= limit:
        print(f"REFUSED: the budget (USD {budget}) must be lower than the card limit (USD {limit}); a person fixes {BUDGET}")
        return 3
    if currency.upper() != "USD":
        print(f"REFUSED: the price is in {currency}, the budget is in USD (conversion and fees can make the charge higher)")
        return 3
    used = open_spend(read_rows())
    left = budget - used
    print(f"budget USD {budget} | open spend USD {used} | left USD {left} | per-payment cap USD {cap} | this payment USD {amount}")
    if amount > cap:
        print(f"REFUSED: USD {amount} is above the per-payment cap USD {cap}")
        return 3
    if amount > left:
        print(f"REFUSED: USD {amount} would take the open spend to USD {used + amount}, above the budget USD {budget}")
        return 3
    print("OK")
    return 0


def add(a):
    if a.status not in {"paid", "declined", "unclear"}:
        sys.exit("--status must be paid, declined or unclear")
    rows = read_rows()
    run = Path(a.run).name
    row = next((r for r in rows if r["run"] == run and r["tc"] == a.tc), None)
    if row is None:
        n = max([int(r["id"][2:]) for r in rows if re.fullmatch(r"P-\d+", r.get("id", ""))] or [0]) + 1
        row = {"id": f"P-{n:04d}", "refund_status": "not requested" if a.status == "paid" else ""}
        rows.append(row)
    row.update(date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), site=a.site, run=run, tc=a.tc, item=a.item,
               amount=str(money(a.amount)), currency=a.currency.upper(), status=a.status)
    if a.order_id:
        row["order_id"] = a.order_id
    if a.message:
        row["message"] = a.message
    if a.status == "paid" and not row.get("refund_status"):
        row["refund_status"] = "not requested"
    write_rows(rows)
    print(f"{row['id']} | {row['tc']} | {row['item']} | USD {row['amount']} | {row['status']} | order {row.get('order_id') or '-'}")
    print(f"open spend now USD {open_spend(rows)}")


def set_row(a):
    rows = read_rows()
    row = next((r for r in rows if r["id"] == a.id), None)
    if row is None:
        sys.exit(f"no row {a.id} in {LEDGER}")
    if a.status:
        if a.status not in STATUSES:
            sys.exit(f"--status must be one of {sorted(STATUSES)}")
        row["status"] = a.status
    if a.refund:
        row["refund_status"] = a.refund
        row["refund_date"] = a.refund_date or datetime.date.today().isoformat()
    for key in ("order_id", "notes"):
        if getattr(a, key):
            row[key] = getattr(a, key)
    write_rows(rows)
    print(f"{row['id']} updated: status {row['status']}, refund {row.get('refund_status') or '-'}; open spend USD {open_spend(rows)}")


def list_rows():
    rows = read_rows()
    b = read_budget()
    for r in rows:
        mark = "*" if counts(r) else " "
        print(f"{mark} {r['id']} {r['date']} {r['site']:<8} {r['tc']:<7} USD {r['amount']:>8} {r['status']:<9} "
              f"order {r.get('order_id') or '-':<14} refund {r.get('refund_status') or '-'} {r.get('refund_date') or ''}  {r['item']}")
    used = open_spend(rows)
    print(f"{len(rows)} rows; * = counts against the budget. Open spend USD {used}; budget USD {b.get('budget', 0)}; "
          f"left USD {b.get('budget', Decimal(0)) - used}; ledger {LEDGER}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("amount")
    c.add_argument("--currency", default="USD")
    ad = sub.add_parser("add")
    for k in ("--site", "--run", "--tc", "--item", "--amount", "--status"):
        ad.add_argument(k, required=True)
    ad.add_argument("--currency", default="USD")
    ad.add_argument("--order-id", dest="order_id", default="")
    ad.add_argument("--message", default="")
    s = sub.add_parser("set")
    s.add_argument("id")
    s.add_argument("--status")
    s.add_argument("--refund", choices=["requested", "confirmed"])
    s.add_argument("--refund-date", dest="refund_date")
    s.add_argument("--order-id", dest="order_id")
    s.add_argument("--notes")
    sub.add_parser("list")
    a = p.parse_args()
    if a.cmd == "check":
        sys.exit(check(money(a.amount), a.currency))
    {"add": add, "set": set_row, "list": lambda _a: list_rows()}[a.cmd](a)


if __name__ == "__main__":
    main()
