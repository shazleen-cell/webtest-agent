#!/usr/bin/env python3
"""Gather the newest result of every test into one self-contained Results/ folder.
Usage: gather_results.py <runs dir> <site name>
Sources: every run folder (runs/<run>/results/*.json) plus results already in Results/json/*.json.
Copies only; never moves or deletes anything from the run folders.
Writes Results/results.html, Results/results.xlsx, Results/json/<TC ID>.json and Results/<TC ID>/ evidence folders."""
import glob, json, os, re, shutil, sys
import openpyxl
from openpyxl.styles import Font, PatternFill
from report_html import COLORS, PRIOS, e, totals, render, load_categories

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

def md_inline(s):
    s = e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)


def md_to_html(text):
    """Small Markdown subset used by Results/README.md: headings, tables, bullet lists, paragraphs, **bold**, `code`.
    URLs stay plain text so the report only links to files inside Results/."""
    out, para, rows, items = [], [], [], []

    def flush():
        if para:
            out.append(f"<p>{md_inline(' '.join(para))}</p>"); para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{md_inline(i)}</li>" for i in items) + "</ul>"); items.clear()
        if rows:
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows if not re.fullmatch(r"[\s|:-]+", r)]
            head, body = cells[0], cells[1:]
            out.append("<table><thead><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table>"); rows.clear()

    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            if para or items: flush()
            rows.append(s); continue
        if rows: flush()
        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            flush(); lvl = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{lvl}>{md_inline(m.group(2))}</h{lvl}>")
        elif s.startswith(("- ", "* ")):
            if para: flush()
            items.append(s[2:])
        elif not s:
            flush()
        else:
            if items: flush()
            para.append(s)
    flush()
    return "\n".join(out)


def md_sections(text):
    """[(heading, body)] split on "## " headings; the first entry is the text before the first heading."""
    secs, head, body = [], "", []
    for line in text.splitlines():
        m = re.match(r"##\s+(.*)", line)
        if m:
            secs.append((head, "\n".join(body))); head, body = m.group(1).strip(), []
        else:
            body.append(line)
    secs.append((head, "\n".join(body)))
    return secs


def findings(body):
    """{TC ID: "Bug or test wording?" value} from the README table of tests that did not pass."""
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in body.splitlines()
            if r.strip().startswith("|") and not re.fullmatch(r"[\s|:-]+", r)]
    if not rows: return {}
    col = next((i for i, h in enumerate(rows[0]) if h.lower().startswith("bug")), None)
    return {r[0]: r[col] for r in rows[1:] if col is not None and len(r) > col} if col is not None else {}


tot = totals(tests)
total_sec = sum(int(t.get("duration_sec") or 0) for t in tests)
runs_used = sorted({t["run"] for t in tests})
info = load_categories(os.path.join(os.path.dirname(RUNS), "testcases.xlsx"))
readme = os.path.join(OUT, "README.md")
views = []
if os.path.exists(readme):
    with open(readme, encoding="utf-8") as f:
        secs = md_sections(f.read())
    # Totals, the not-passed table and account changes are already on the overview; the rest is the guide.
    for head, body in secs:
        if head.lower().startswith("tests that did not pass"):
            for tid, k in findings(body).items():
                info.setdefault(tid, {})["finding"] = k
    guide = [(h, re.sub(r"^#\s.*$", "", b, flags=re.M)) for h, b in secs
             if not h.lower().startswith(("totals", "tests that did not pass", "account changes"))]
    views.append(("guide", "How to read this report", "<h2>How to read this report</h2>\n" +
                  md_to_html("\n".join((f"## {h}\n" if h else "") + b for h, b in guide))))
intro = (f'<p>Newest result of every test, taken from {len(runs_used)} run{"s" if len(runs_used) != 1 else ""}: {e(", ".join(runs_used))}. '
         f'New here? See <a href="#guide">How to read this report</a>. ' if views else
         f'<p>Newest result of every test, taken from these runs: {e(", ".join(runs_used))}. ') + \
        'Raw results: <a href="json/">json/</a> · <a href="results.xlsx">results.xlsx</a> · <a href="README.md">README.md</a></p>'
page = render(tests, NAME, OUT, f"{len(tests)} tests · newest result from {len(runs_used)} run{'s' if len(runs_used) != 1 else ''}",
              show_run=True, intro=intro, views=views, info=info)
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
