#!/usr/bin/env python3
"""Gather the newest result of every test into one self-contained Results/ folder.
Usage: gather_results.py <runs dir> <site name>
Sources: every run folder (runs/<run>/results/*.json) plus results already in Results/json/*.json.
Copies only; never moves or deletes anything from the run folders.
Writes Results/results.html, Results/results.xlsx, Results/json/<TC ID>.json and Results/<TC ID>/ evidence folders."""
import glob, json, os, shutil, sys
import openpyxl
from openpyxl.styles import Font, PatternFill
from report_html import COLORS, PRIOS, e, totals, render

RUNS, NAME = os.path.abspath(sys.argv[1]), sys.argv[2]
OUT = os.path.join(RUNS, "Results")

# Newest result per test: compare "ended", then run name.
best = {}
sources = [(p, os.path.dirname(os.path.dirname(p))) for p in glob.glob(os.path.join(RUNS, "*", "results", "*.json"))
           if os.path.basename(os.path.dirname(os.path.dirname(p))) != "Results"]
sources += [(p, OUT) for p in glob.glob(os.path.join(OUT, "json", "*.json"))]
for p, run_dir in sources:
    with open(p, encoding="utf-8") as f:
        t = json.load(f)
    run = t.get("run") if run_dir == OUT else os.path.basename(run_dir)
    key = (str(t.get("ended") or ""), str(run))
    if t["id"] not in best or key > best[t["id"]][0]:
        best[t["id"]] = (key, run_dir, run, t)

os.makedirs(os.path.join(OUT, "json"), exist_ok=True)
tests = []
for tid, (_, run_dir, run, t) in sorted(best.items()):
    src = os.path.join(run_dir, tid)
    if run_dir != OUT and os.path.isdir(src):
        dst = os.path.join(OUT, tid)
        if os.path.isdir(dst):
            shutil.rmtree(dst)  # replace an older result's evidence in Results/ only
        shutil.copytree(src, dst)
    t["run"] = run
    with open(os.path.join(OUT, "json", f"{tid}.json"), "w", encoding="utf-8") as f:
        json.dump(t, f, ensure_ascii=False, indent=2)
    tests.append(t)

tot = totals(tests)
total_sec = sum(int(t.get("duration_sec") or 0) for t in tests)
runs_used = sorted({t["run"] for t in tests})
intro = ('<p>New here? Read <a href="README.md">README.md</a> for what every file and folder means. '
         f'Raw results per test: <a href="json/">json/</a>. Newest result per test from these runs: {e(", ".join(runs_used))}.</p>')
page = render(tests, NAME, OUT, f"{NAME} · all runs · {len(tests)} tests", show_run=True, intro=intro)
with open(os.path.join(OUT, "results.html"), "w", encoding="utf-8") as f:
    f.write(page)

# Excel
hdr = ["TC ID", "Title", "Area", "Priority", "Status", "Run", "Duration (sec)", "Failed step", "What I saw (if failed)", "Evidence folder"]
wb = openpyxl.Workbook()
ws = wb.active; ws.title = "Summary"
for r in [["Site", NAME], ["Tests", len(tests)]] + [[k.capitalize(), v] for k, v in tot.items()] + \
         [[f"{p} tests", sum(1 for t in tests if t.get("priority") == p)] for p in PRIOS] + \
         [["Total time (sec)", total_sec], ["Runs used", ", ".join(runs_used)], ["Report", "results.html"],
          ["Video", "Not available (wdio-mcp cannot record video); see replay GIFs and trace zips"]]:
    ws.append(r)
ws.column_dimensions["A"].width = 18; ws.column_dimensions["B"].width = 90
wr = wb.create_sheet("Results"); wr.append(hdr)
fills = {k: PatternFill("solid", fgColor=c.lstrip("#")) for k, c in COLORS.items()}
for t in tests:
    saw = ""
    if t.get("status") != "PASSED":
        fs = [s for s in t.get("steps", []) if not s.get("ok", True)]
        saw = fs[0].get("saw", "") if fs else t.get("reason", "")
    wr.append([t["id"], t.get("title"), t.get("area"), t.get("priority"), t.get("status"), t["run"],
               t.get("duration_sec"), t.get("failed_step"), saw, f"{t['id']}/"])
    c = wr.cell(wr.max_row, 5)
    if t.get("status") in fills: c.fill = fills[t["status"]]; c.font = Font(bold=True, color="FFFFFF")
for col, w in zip("ABCDEFGHIJ", [10, 50, 14, 9, 10, 22, 13, 11, 60, 16]): wr.column_dimensions[col].width = w
wsS = wb.create_sheet("Steps")
wsS.append(["TC ID", "Priority", "Step", "Text", "Expected", "Answer", "What I saw", "Result", "Screenshot"])
for t in tests:
    for s in t.get("steps", []):
        wsS.append([t["id"], t.get("priority"), s["n"], s.get("text"), s.get("expected"), s.get("answer"), s.get("saw"),
                    "PASSED" if s.get("ok", True) else "FAILED", s.get("screenshot") or ""])
        if not s.get("ok", True):
            for cell in wsS[wsS.max_row]: cell.fill = PatternFill("solid", fgColor="FEE2E2")
for col, w in zip("ABCDEFGHI", [10, 9, 6, 60, 10, 18, 70, 9, 26]): wsS.column_dimensions[col].width = w
for sh in (wr, wsS):
    for c in sh[1]: c.font = Font(bold=True)
    sh.freeze_panes = "A2"
    sh.auto_filter.ref = sh.dimensions
wb.save(os.path.join(OUT, "results.xlsx"))
print(len(tests), tot, {p: sum(1 for t in tests if t.get("priority") == p) for p in PRIOS}, runs_used)
