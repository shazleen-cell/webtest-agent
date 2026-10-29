#!/usr/bin/env python3
"""Shared report.html layout for build_run_report.py (one run) and gather_results.py (all runs).
render() returns the page: sticky top bar with status pills and mode/priority filters, a searchable
sidebar of cases grouped by status, an overview table, and one view per test with its steps."""
import html, os

COLORS = {"PASSED": "#16a34a", "FAILED": "#dc2626", "BLOCKED": "#d97706", "SKIPPED": "#2563eb", "UNSURE": "#6b7280"}
SHOWN = ["FAILED", "BLOCKED", "SKIPPED", "PASSED"]  # statuses with a filter pill (UNSURE has none)
ICON = {"PASSED": "✓", "FAILED": "✗", "BLOCKED": "!", "SKIPPED": "»", "UNSURE": "?"}
PRIOS = ["High", "Medium", "Low"]
e = lambda s: html.escape(str(s if s is not None else ""))


def totals(tests): return {k: sum(1 for t in tests if t.get("status") == k) for k in COLORS}
def fmt(sec): return f"{sec // 3600} h {sec % 3600 // 60} min {sec % 60} s" if sec >= 3600 else f"{sec // 60} min {sec % 60} s"
def mode(t): return "LOGGED IN" if str(t.get("title", "")).startswith(("[LOGGED IN]", "[PLAYER]")) else "LOGGED OUT"
def changes(t): return [str(c) for c in (t.get("account_changes") or [])]
def low(t): return e(" ".join(str(t[k]) for k in ("id", "title", "area", "priority", "reason", "run") if t.get(k)).lower())
def step_badge(s):
    """DONE / SKIPPED / PASS / FAIL label for one step."""
    if not s.get("ok", True): return "fail", "FAIL"
    if s.get("expected"): return "pass", "PASS"
    return ("done", "SKIPPED") if str(s.get("answer", "")).startswith("Skipped") else ("done", "DONE")

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--fg:#1d2330;--mut:#5f6b7a;--line:#e3e7ec;--pass:#1f8a4c;--fail:#c62828;--block:#b26a00;--done:#6b7685;--skip:#2563eb;--sel:#e8eefc;--top:56px}
@media (prefers-color-scheme:dark){:root{--bg:#12151b;--card:#1b2029;--fg:#e8ebf0;--mut:#9aa5b4;--line:#2c3340;--pass:#4cc38a;--fail:#ff6b6b;--block:#f0a640;--done:#8b96a5;--skip:#6b9bff;--sel:#26304a}}
*{box-sizing:border-box}html{scroll-padding-top:calc(var(--top) + 8px)}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 -apple-system,system-ui,Segoe UI,Roboto,sans-serif}
button,select{font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
button:hover,select:hover{border-color:var(--mut)}
a{color:#2563eb}
.top{position:sticky;top:0;z-index:20;height:var(--top);display:flex;align-items:center;gap:12px;padding:0 16px;background:var(--card);border-bottom:1px solid var(--line)}
.top h1{font-size:16px;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.health{font-size:13px;color:var(--mut);white-space:nowrap}.health b{color:var(--fg)}
.filters{margin-left:auto;display:flex;gap:6px;align-items:center}.pill{border-radius:999px;font-size:13px}.pill.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.filters select{font-size:13px;border-radius:999px}
.menubtn{display:none}.top button{white-space:nowrap;flex:none}
.wrap{display:grid;grid-template-columns:300px minmax(0,1fr)}
aside{position:sticky;top:var(--top);height:calc(100vh - var(--top));overflow:auto;border-right:1px solid var(--line);background:var(--card);padding:12px 8px 24px}
.search{width:100%;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit;margin-bottom:8px}
.links a{display:block;padding:5px 8px;border-radius:6px;color:inherit;text-decoration:none;font-size:14px}.links a:hover,.item:hover{background:var(--bg)}
.links.cur-o a[href="#overview"]{background:var(--sel)}
.gh{font-size:12px;font-weight:700;color:var(--mut);letter-spacing:.04em;padding:12px 8px 4px}
.item{display:grid;grid-template-columns:18px 58px minmax(0,1fr);gap:4px;align-items:center;padding:5px 8px;border-radius:6px;color:inherit;text-decoration:none;font-size:14px}
.item .it{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.iid{font-weight:600;font-variant-numeric:tabular-nums}
.ic{font-weight:700;text-align:center}.i-failed .ic{color:var(--fail)}.i-passed .ic{color:var(--pass)}.i-blocked .ic{color:var(--block)}.i-skipped .ic{color:var(--skip)}.i-unsure .ic{color:var(--done)}
.item.cur{background:var(--sel);outline:1px solid var(--line)}
main{padding:20px 24px 80px;min-width:0}
.view{max-width:1150px}
.b{display:inline-block;font-size:12px;font-weight:700;border-radius:4px;padding:1px 6px;color:#fff;vertical-align:middle}
.b-passed,.b-pass{background:var(--pass)}.b-failed,.b-fail{background:var(--fail)}.b-blocked{background:var(--block)}.b-skipped{background:var(--skip)}.b-done,.b-unsure{background:var(--done)}
.m{font-size:11px;border:1px solid var(--line);border-radius:4px;padding:0 5px;color:var(--mut);white-space:nowrap}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
td,th{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{font-size:13px;color:var(--mut)}td a{color:inherit;font-weight:600}
tbody tr{cursor:pointer}td:first-child{white-space:nowrap}tbody tr:hover{background:var(--bg)}
.note{background:color-mix(in srgb,var(--block) 10%,transparent);border:1px solid color-mix(in srgb,var(--block) 35%,transparent);padding:8px 12px;border-radius:6px;font-size:14px}
.case{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--done);border-radius:8px;padding:16px}
.case.v-passed{border-left-color:var(--pass)}.case.v-failed{border-left-color:var(--fail)}.case.v-blocked{border-left-color:var(--block)}.case.v-skipped{border-left-color:var(--skip)}
.ctitle{display:flex;gap:12px;align-items:flex-start;justify-content:space-between}.ctitle h2{font-size:19px;margin:0}
.nav{display:flex;gap:6px;flex:none}.meta{color:var(--mut);margin:6px 0}
.reason{margin:8px 0;padding:8px 10px;border-radius:6px;background:color-mix(in srgb,var(--fail) 9%,transparent)}
.v-passed .reason{background:var(--bg)}.v-blocked .reason{background:color-mix(in srgb,var(--block) 10%,transparent)}.v-skipped .reason{background:color-mix(in srgb,var(--skip) 10%,transparent)}
.changes{margin:8px 0;padding:8px 10px 8px 28px;border-radius:6px;background:var(--bg);font-size:14px}
.files{font-size:14px;margin:6px 0}.files a{margin-right:14px}
.tools{display:flex;gap:6px;margin:10px 0 4px;flex-wrap:wrap}
.replay{margin:8px 0}.replay summary{cursor:pointer;color:var(--mut);font-size:14px}.replay img{width:640px;max-width:100%;border:1px solid var(--line);border-radius:6px;margin-top:8px}
.steps{border-top:1px solid var(--line);margin-top:8px}
.step{border-bottom:1px solid var(--line)}
.step summary{list-style:none;display:flex;align-items:center;gap:8px;padding:9px 6px;cursor:pointer}
.step summary::-webkit-details-marker{display:none}
.step summary::before{content:'▸';color:var(--mut);width:10px}.step[open] summary::before{content:'▾'}
.step .num{font-weight:700;min-width:22px;color:var(--mut);font-variant-numeric:tabular-nums}
.step .st{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;flex:1}
.step[open] .st{white-space:normal}
.step.r-fail{background:color-mix(in srgb,var(--fail) 7%,transparent)}
.body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);gap:16px;padding:4px 6px 14px 26px}
.txt p{margin:4px 0}.ans{font-size:14px}.ev{color:var(--mut);font-size:13px}
.shot img{width:100%;border:1px solid var(--line);border-radius:6px;display:block;margin-bottom:6px;min-height:40px}
.noshot{color:var(--block);font-size:13px;padding:8px;border:1px dashed var(--line);border-radius:6px}
.hint{color:var(--mut);font-size:12px;margin-top:16px}kbd{border:1px solid var(--line);border-radius:3px;padding:0 4px;font-size:11px}
.empty{color:var(--mut);font-size:13px;padding:8px}
.md table{margin:8px 0 16px}.md tbody tr{cursor:auto}.md td:first-child{white-space:normal}.md h2{margin-top:0}.md h3{margin:22px 0 6px}
.md code{font-size:13px;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:0 4px}
@media (max-width:860px){
 .wrap{grid-template-columns:1fr}.menubtn{display:inline-block}.health{display:none}
 aside{position:fixed;left:0;top:var(--top);width:85vw;max-width:340px;z-index:15;transform:translateX(-105%);transition:transform .2s;box-shadow:0 6px 24px #0004}
 body.menu aside{transform:none}
 .filters .pill:not(.on),.filters select{display:none}
 main{padding:14px 12px 60px}.body{grid-template-columns:1fr;padding-left:6px}.ctitle{flex-direction:column}
}
"""

JS = """
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s) }
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)) }
  var filter = 'ALL', query = '', mode = 'ALL', prio = 'ALL'
  function loadImgs(root) { $$('img[data-src]', root).forEach(function (i) { i.src = i.dataset.src; i.removeAttribute('data-src') }) }
  function visibleItems() { return $$('.item').filter(function (a) { return !a.hidden }) }
  function current() { return (location.hash || '#overview').slice(1) }
  function show() {
    var id = decodeURIComponent(current())
    var target = document.getElementById(id)
    if (!target || !target.classList.contains('view')) { id = 'overview'; target = document.getElementById('overview') }
    $$('.view').forEach(function (v) { v.hidden = v !== target })
    $$('.item').forEach(function (a) { a.classList.toggle('cur', a.dataset.id === id) })
    $('.links').classList.toggle('cur-o', id === 'overview')
    $$('details[open]', target).forEach(loadImgs)
    var cur = $('.item.cur'); if (cur) cur.scrollIntoView({ block: 'nearest' })
    window.scrollTo(0, 0)
    document.body.classList.remove('menu')
    document.title = (id === 'overview' ? 'Overview' : id) + ' — ' + document.body.dataset.site
  }
  function go(id) { if (id) location.hash = id }
  function step(dir) {
    var items = visibleItems(); if (!items.length) return
    var i = items.findIndex(function (a) { return a.dataset.id === current() })
    var n = i < 0 ? (dir > 0 ? 0 : items.length - 1) : (i + dir + items.length) % items.length
    go(items[n].dataset.id)
  }
  function nextFailed() {
    var all = $$('.item'), i = all.findIndex(function (a) { return a.dataset.id === current() })
    for (var k = 1; k <= all.length; k++) { var a = all[(i + k + all.length) % all.length]; if (a.dataset.verdict === 'FAILED') return go(a.dataset.id) }
  }
  function match(el, useQuery) {
    return (filter === 'ALL' || el.dataset.verdict === filter) && (mode === 'ALL' || el.dataset.mode === mode)
      && (prio === 'ALL' || el.dataset.prio === prio)
      && (!useQuery || !query || el.dataset.text.indexOf(query) >= 0)
  }
  function apply() {
    $$('.item').forEach(function (a) { a.hidden = !match(a, true) })
    $$('.grp').forEach(function (g) { g.hidden = !$$('.item', g).some(function (a) { return !a.hidden }) })
    $('.empty').hidden = visibleItems().length > 0
    var rows = 0
    $$('#overview tbody tr').forEach(function (r) { r.hidden = !match(r, true); if (!r.hidden) rows++ })
    $('#shown').textContent = rows
  }
  $$('.pill').forEach(function (b) { b.onclick = function () {
    $$('.pill').forEach(function (x) { x.classList.toggle('on', x === b) }); filter = b.dataset.f; apply()
  } })
  $('#mode').onchange = function (e) { mode = e.target.value; apply() }
  $('#prio').onchange = function (e) { prio = e.target.value; apply() }
  $('.search').addEventListener('input', function (e) { query = e.target.value.trim().toLowerCase(); apply() })
  $('.menubtn').onclick = function () { document.body.classList.toggle('menu') }
  $$('details').forEach(function (d) { d.addEventListener('toggle', function () { if (d.open) loadImgs(d) }) })
  $$('.prev').forEach(function (b) { b.onclick = function () { step(-1) } })
  $$('.next').forEach(function (b) { b.onclick = function () { step(1) } })
  $$('.expand').forEach(function (b) { b.onclick = function () { $$('details.step', b.closest('.case')).forEach(function (d) { d.open = true }) } })
  $$('.collapse').forEach(function (b) { b.onclick = function () { $$('details.step', b.closest('.case')).forEach(function (d) { d.open = false }) } })
  $$('#overview tbody tr').forEach(function (r) { r.onclick = function () { go(r.dataset.go) } })
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return
    var t = e.target; if (t && t.matches && t.matches('input, textarea, select')) { if (e.key === 'Escape') t.blur(); return }
    if (e.key === 'j') step(1); else if (e.key === 'k') step(-1); else if (e.key === 'n') nextFailed()
    else if (e.key === 'e') {
      var c = $('.case:not([hidden])'); if (!c) return
      var openAll = $$('details.step:not([open])', c).length > 0
      $$('details.step', c).forEach(function (d) { d.open = openAll })
    }
    else if (e.key === '/') { e.preventDefault(); document.body.classList.add('menu'); $('.search').focus() }
  })
  window.addEventListener('hashchange', show)
  apply(); show()
})()
"""


def render(tests, name, root, summary, show_run=False, intro="", views=()):
    """tests: result dicts; root: folder the evidence paths are relative to; summary: overview line (plain text);
    show_run: add a Run column and run label per test; intro: extra HTML paragraph for the overview;
    views: extra (id, label, html) pages, linked in the sidebar next to Overview."""
    def exists(rel): return bool(rel) and os.path.exists(os.path.join(root, rel))
    tot = totals(tests)
    total_sec = sum(int(t.get("duration_sec") or 0) for t in tests)
    health = "DEGRADED" if tot["FAILED"] or tot["BLOCKED"] else "HEALTHY"
    title = f"Test results — {name}"
    attrs = lambda t: f'data-mode="{mode(t)}" data-prio="{e(t.get("priority"))}" data-text="{low(t)}"'

    out = [f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><style>{CSS}</style></head><body data-site="{e(name)}">
<div class="top">
  <button class="menubtn" aria-label="Show cases">☰ Cases</button>
  <h1>{e(title)}</h1>
  <span class="health"><b>{health}</b> · {tot['PASSED']} ✓ · {tot['FAILED']} ✗ · {tot['BLOCKED']} ! · {tot['SKIPPED']} » · {len(tests)} total</span>
  <div class="filters">
    <button class="pill on" data-f="ALL">All {len(tests)}</button>"""]
    out += [f'    <button class="pill" data-f="{k}">{k.capitalize()} {tot[k]}</button>' for k in SHOWN]
    out.append("""    <select id="mode" aria-label="Mode"><option value="ALL">Logged out + in</option><option value="LOGGED OUT">LOGGED OUT</option><option value="LOGGED IN">LOGGED IN</option></select>
    <select id="prio" aria-label="Priority"><option value="ALL">All priorities</option>""" +
               "".join(f'<option value="{p}">{p}</option>' for p in PRIOS) + """</select>
  </div>
</div>
<div class="wrap">
<aside>
  <input class="search" type="search" placeholder="Search cases…  ( / )" aria-label="Search cases">
  <div class="links"><a href="#overview">Overview</a>""" +
               "".join(f'<a href="#{e(vid)}">{e(label)}</a>' for vid, label, _ in views) + "</div>")
    for k in SHOWN + ["UNSURE"]:
        group = [t for t in tests if t.get("status") == k]
        if not group: continue
        out.append(f'  <div class="grp"><div class="gh">{k} ({len(group)})</div>')
        for t in group:
            out.append(f'  <a class="item i-{k.lower()}" href="#{e(t["id"])}" data-id="{e(t["id"])}" data-verdict="{k}" {attrs(t)} '
                       f'title="{e(t["id"])} — {e(t.get("title"))}"><span class="ic">{ICON[k]}</span>'
                       f'<span class="iid">{e(t["id"])}</span><span class="it">{e(t.get("title"))}</span></a>')
        out.append("  </div>")
    out.append("""  <div class="empty" hidden>No cases match.</div>
  <p class="hint"><kbd>j</kbd>/<kbd>k</kbd> next/previous · <kbd>n</kbd> next failed · <kbd>e</kbd> expand all · <kbd>/</kbd> search</p>
</aside>
<main>""")

    # Overview
    verdict = "some checks failed" if health == "DEGRADED" else "all checks passed"
    run_th = "<th>Run</th>" if show_run else ""
    out.append(f"""<section class="view" id="overview">
  <h2 style="margin-top:0">Overview</h2>
  <p>{e(summary)} · total time {fmt(total_sec)}</p>
  <p><strong>{health} — {verdict}</strong> — {tot['PASSED']} passed, {tot['FAILED']} failed, {tot['BLOCKED']} blocked, {tot['SKIPPED']} skipped, {tot['UNSURE']} unsure, {len(tests)} total</p>
  {intro}
  <p class="note">Real video is not available: wdio-mcp has no screen-recording tool. Each test has a step-by-step replay GIF and a WebdriverIO trace zip instead.</p>
  <p class="ev">Showing <span id="shown">{len(tests)}</span> of {len(tests)} tests. Click a row to open the test.</p>
  <table><thead><tr><th>ID</th><th>Priority</th><th>Verdict</th><th>Mode</th>{run_th}<th>Test</th><th>Reason</th></tr></thead><tbody>""")
    order = {k: i for i, k in enumerate(SHOWN + ["UNSURE"])}
    for t in sorted(tests, key=lambda t: (order.get(t.get("status"), 9), t["id"])):
        st = t.get("status", "")
        reason = t.get("reason") if st != "PASSED" else ""
        run_td = f'<td>{e(t.get("run"))}</td>' if show_run else ""
        out.append(f'  <tr data-verdict="{e(st)}" {attrs(t)} data-go="{e(t["id"])}"><td><a href="#{e(t["id"])}">{e(t["id"])}</a></td>'
                   f'<td>{e(t.get("priority"))}</td><td><span class="b b-{e(st.lower())}">{e(st)}</span></td><td><span class="m">{mode(t)}</span></td>'
                   f'{run_td}<td>{e(t.get("title"))}</td><td>{e(reason)}</td></tr>')
    out.append("  </tbody></table>\n</section>")

    for vid, _, html_ in views:
        out.append(f'<section class="view md" id="{e(vid)}" hidden>\n{html_}\n</section>')

    # One view per test
    for t in tests:
        tid, st = t["id"], t.get("status", "")
        steps = t.get("steps", [])
        files = [f'<a href="{e(tid)}/">Evidence folder</a>']
        if exists(f"{tid}/{tid}_steps.pdf"): files.append(f'<a href="{e(tid)}/{e(tid)}_steps.pdf">Steps PDF</a>')
        if exists(f"{tid}/{tid}_trace.zip"): files.append(f'<a href="{e(tid)}/{e(tid)}_trace.zip">Trace zip</a>')
        meta = [e(t.get("area")), e(t.get("priority")), mode(t), f'{e(t.get("duration_sec"))} s', f"{len(steps)} steps"]
        if show_run: meta.append(f'run {e(t.get("run"))}')
        if t.get("failed_step"): meta.append(f'failed at step {e(t["failed_step"])}')
        out.append(f"""<section class="view case v-{e(st.lower())}" id="{e(tid)}" hidden>
  <div class="ctitle"><h2><span class="b b-{e(st.lower())}">{e(st)}</span> {e(tid)} — {e(t.get("title"))}</h2>
  <div class="nav"><button class="prev">◀ Prev</button><button class="next">Next ▶</button></div></div>
  <p class="meta">{" · ".join(meta)}</p>""")
        if t.get("reason"):
            out.append(f'  <div class="reason">{e(t["reason"])}</div>')
        if changes(t):
            out.append('  <ul class="changes" aria-label="Changes to the test account">' + "".join(f"<li>{e(c)}</li>" for c in changes(t)) + "</ul>")
        out.append(f'  <p class="files">{"".join(files)}</p>')
        gif = t.get("replay_gif") or f"{tid}/{tid}_replay.gif"
        if exists(gif):
            out.append(f'  <details class="replay"><summary>Replay GIF</summary><a href="{e(gif)}" target="_blank"><img data-src="{e(gif)}" alt="{e(tid)} replay"></a></details>')
        out.append('  <div class="tools"><button class="expand">Expand all</button><button class="collapse">Collapse all</button></div>\n  <div class="steps">')
        for s in steps:
            cls, label = step_badge(s)
            is_q = bool(s.get("expected"))
            shot = s.get("screenshot")
            img = (f'<a href="{e(shot)}" target="_blank"><img data-src="{e(shot)}" alt="{e(tid)} step {e(s["n"])}"></a>'
                   if exists(shot) else '<div class="noshot">No screenshot</div>')
            ans = (f'Expected <b>{e(s.get("expected"))}</b> · Actual <b>{e(s.get("answer"))}</b>' if is_q
                   else f'Result <b>{e(s.get("answer"))}</b>')
            opened = " open" if cls == "fail" else ""
            out.append(f'  <details class="step r-{cls}"{opened}><summary><span class="num">{e(s["n"])}</span>'
                       f'<span class="b b-{cls}">{label}</span><span class="st">{e(s.get("text"))}</span></summary>'
                       f'<div class="body"><div class="txt"><p>{e(s.get("text"))}</p><p class="ans">{ans}</p>'
                       f'<p class="ev">{e(s.get("saw"))}</p></div><div class="shot">{img}</div></div></details>')
        out.append("  </div>\n</section>")
    out.append(f"</main>\n</div>\n<script>{JS}</script>\n</body></html>")
    return "\n".join(out)
