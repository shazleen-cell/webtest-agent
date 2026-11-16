#!/usr/bin/env python3
"""Build report.html, results.xlsx, results.csv for a run and update testcases.xlsx.
Usage: build_run_report.py <RUN> <SITE> <site name>"""
import csv, glob, json, os, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from report_html import COLORS, totals, changes, render, load_categories, load_timing, run_time

RUN, SITE, NAME = sys.argv[1], sys.argv[2], sys.argv[3]
run_date = os.path.basename(RUN.rstrip("/"))
tests = []
for p in sorted(glob.glob(os.path.join(RUN, "results", "*.json"))):
    with open(p, encoding="utf-8") as f:
        tests.append(json.load(f))
tests.sort(key=lambda t: t["id"])

tot = totals(tests)
total_sec = sum(int(t.get("duration_sec") or 0) for t in tests)
timing = run_time([load_timing(RUN)], [run_date])
page = render(tests, NAME, RUN, f"run {run_date} · {len(tests)} tests", info=load_categories(os.path.join(SITE, "testcases.xlsx")),
              timing=timing)
with open(os.path.join(RUN, "report.html"), "w", encoding="utf-8") as f:
    f.write(page)

# Results rows
hdr = ["TC ID", "Title", "Area", "Priority", "Status", "Run date", "Duration (sec)", "Failed step", "What I saw (if failed)", "Evidence folder", "Account changes"]
rows = []
for t in tests:
    saw = ""
    if t.get("status") != "PASSED":
        fs = [s for s in t.get("steps", []) if not s.get("ok", True)]
        saw = fs[0].get("saw", "") if fs else t.get("reason", "")
    rows.append([t["id"], t.get("title"), t.get("area"), t.get("priority"), t.get("status"), run_date,
                 t.get("duration_sec"), t.get("failed_step"), saw, os.path.join(RUN, t["id"]) + "/", "; ".join(changes(t))])

wb = openpyxl.Workbook()
ws = wb.active; ws.title = "Summary"
for r in [["Site", NAME], ["Run date", run_date], ["Tests", len(tests)]] + [[k.capitalize(), v] for k, v in tot.items()] + \
         ([["Full run time (sec)", timing["full"] if timing else ""], ["Coordinator time (sec)", timing["coordinator"] if timing else ""],
          ["website-tester agent time (sec)", timing["tester"] if timing else ""], ["Test step time (sec)", total_sec],
          ["Tokens (website-tester, latest full run)", timing["tokens"] if timing else ""], ["Token run", timing["token_run"] if timing else ""], ["Tool calls (same run)", timing["tool_calls"] if timing else ""]] + [["Report", os.path.join(RUN, "report.html")],
          ["Video", "Screen recordings of the browser (when available), replay videos of the step screenshots (GIFs in older runs) and trace zips"]]):
    ws.append(r)
ws.column_dimensions["A"].width = 18; ws.column_dimensions["B"].width = 90
wr = wb.create_sheet("Results"); wr.append(hdr)
fills = {k: PatternFill("solid", fgColor=c.lstrip("#")) for k, c in COLORS.items()}
for r in rows:
    wr.append(r)
    c = wr.cell(wr.max_row, 5)
    if r[4] in fills: c.fill = fills[r[4]]; c.font = Font(bold=True, color="FFFFFF")
for col, w in zip("ABCDEFGHIJK", [10, 50, 14, 9, 10, 17, 13, 11, 60, 70, 50]): wr.column_dimensions[col].width = w
wsS = wb.create_sheet("Steps")
wsS.append(["TC ID", "Step", "Text", "Expected", "Answer", "What I saw", "Result", "Screenshot"])
for t in tests:
    for s in t.get("steps", []):
        wsS.append([t["id"], s["n"], s.get("text"), s.get("expected"), s.get("answer"), s.get("saw"),
                    "PASSED" if s.get("ok", True) else "FAILED", os.path.basename(s.get("screenshot") or "")])
        if not s.get("ok", True):
            for cell in wsS[wsS.max_row]: cell.fill = PatternFill("solid", fgColor="FEE2E2")
for col, w in zip("ABCDEFGH", [10, 6, 60, 10, 18, 70, 9, 20]): wsS.column_dimensions[col].width = w
for sh in (wr, wsS):
    for c in sh[1]: c.font = Font(bold=True)
    sh.freeze_panes = "A2"
wb.save(os.path.join(RUN, "results.xlsx"))

with open(os.path.join(RUN, "results.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)

# Update testcases.xlsx
tc_path = os.path.join(SITE, "testcases.xlsx")
lock = os.path.join(SITE, "~$testcases.xlsx")
if os.path.exists(lock):
    print("TESTCASES_OPEN"); sys.exit(2)
twb = openpyxl.load_workbook(tc_path)
tws = twb.worksheets[0]
h = [c.value for c in tws[1]]
ci, cr, cl = h.index("TC ID") + 1, h.index("Last result") + 1, h.index("Last run") + 1
by = {t["id"]: t for t in tests}
for row in range(2, tws.max_row + 1):
    tid = tws.cell(row, ci).value
    if tid in by:
        tws.cell(row, cr).value = by[tid].get("status")
        tws.cell(row, cl).value = run_date
twb.save(tc_path)
print("done", tot, total_sec)
