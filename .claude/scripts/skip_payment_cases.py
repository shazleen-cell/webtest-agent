#!/usr/bin/env python3
"""Write a SKIPPED result for every payment case of a site, without running anything.

Usage: skip_payment_cases.py <RUN> <SITE> [filter]

A payment case is a row of SITE/testcases.xlsx whose Sub-type starts with "Payment" (written by /test-website with
Approved = Skip). Payment cases are never run, so no browser is opened, nothing is clicked and no money is spent.
For each one this writes RUN/results/<TC ID>.json (status SKIPPED, skip_kind "payment") and an empty RUN/<TC ID>/
evidence folder, so the reports can list them in their own "Skipped (payment)" group.

- A payment case with Approved = Yes is still not run: it is written as skipped and a warning is printed.
- A payment case with Approved = No is left out (the reviewer rejected it).
- filter (optional): the same filter as /run-tests: High, Medium, Low, LoggedOut, LoggedIn, Changes or a list of TC IDs.
Only placeholders such as {CARD_NUMBER} appear in the steps. This script never reads or writes a real card value."""
import json, os, re, sys
from datetime import datetime
import openpyxl

if len(sys.argv) < 3:
    sys.exit(__doc__)
RUN, SITE = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
FILTER = sys.argv[3].strip() if len(sys.argv) > 3 else ""
NOTE = "Skip: not executed, no money spent. Payment cases are written but never run by the agent."


def wanted(row, flt):
    """Apply the /run-tests filter to one row (a dict)."""
    if not flt:
        return True
    title = str(row.get("Title") or "")
    logged_in = title.startswith(("[LOGGED IN]", "[PLAYER]"))
    f = flt.lower()
    if f in ("high", "medium", "low"):
        return str(row.get("Priority") or "").lower() == f
    if f in ("loggedout", "guest"):
        return not logged_in
    if f in ("loggedin", "player"):
        return logged_in
    if f == "changes":
        return str(row.get("Changes account") or "").lower() == "yes"
    ids = {x.strip().upper() for x in re.split(r"[,\s]+", flt) if x.strip()}
    return str(row.get("TC ID") or "").upper() in ids


def parse_steps(text):
    """'1. Do this.\\n2. Is it so?' -> [(1, 'Do this.'), (2, 'Is it so?')]"""
    out = []
    for line in str(text or "").splitlines():
        m = re.match(r"\s*(\d+)\.\s*(.*)", line)
        if m:
            out.append((int(m.group(1)), m.group(2).strip()))
        elif out and line.strip():
            out[-1] = (out[-1][0], out[-1][1] + " " + line.strip())
    return out


def expected_map(text):
    """'#3 Yes, #5 No' -> {3: 'Yes', 5: 'No'}"""
    return {int(n): a.capitalize() for n, a in re.findall(r"#(\d+)\s*(Yes|No)", str(text or ""), flags=re.I)}


ws = openpyxl.load_workbook(os.path.join(SITE, "testcases.xlsx"), read_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True))
head = [str(c) for c in rows[0]]
now = datetime.now().replace(microsecond=0).isoformat()
os.makedirs(os.path.join(RUN, "results"), exist_ok=True)
done = []
for values in rows[1:]:
    row = dict(zip(head, values))
    if not row.get("TC ID") or not str(row.get("Sub-type") or "").strip().lower().startswith("payment"):
        continue
    approved = str(row.get("Approved") or "").strip().lower()
    if approved == "no" or not wanted(row, FILTER):
        continue
    if approved == "yes":
        print(f"WARNING: {row['TC ID']} is a payment case with Approved = Yes. It is NOT run; written as skipped.")
    exp = expected_map(row.get("Expected answers"))
    steps = [{"n": n, "text": text, "expected": "", "answer": "Skipped (payment)",
              "saw": "Not run: payment case, skipped on purpose." + (f" Expected answer if it were run: {exp[n]}." if n in exp else ""),
              "ok": True} for n, text in parse_steps(row.get("Steps"))]
    tid = str(row["TC ID"])
    result = {"id": tid, "title": row.get("Title"), "area": row.get("Area"), "priority": row.get("Priority"),
              "status": "SKIPPED", "skip_kind": "payment", "started": now, "ended": now, "duration_sec": 0,
              "failed_step": None, "reason": NOTE, "account_changes": [], "steps": steps}
    with open(os.path.join(RUN, "results", f"{tid}.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(RUN, tid), exist_ok=True)
    done.append(tid)
print(f"payment cases skipped: {len(done)}" + (f" ({', '.join(done)})" if done else ""))
