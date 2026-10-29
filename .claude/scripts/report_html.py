#!/usr/bin/env python3
"""Shared report.html layout for build_run_report.py (one run) and gather_results.py (all runs).
render() returns the page: a slim top bar, a sidebar with search, filters and the tests grouped by status,
an overview (totals, breakdowns, tests that need attention, account changes, all tests) and one view per test
that starts with what went wrong, then its evidence and steps."""
import html, os, re

COLORS = {"PASSED": "#16a34a", "FAILED": "#dc2626", "BLOCKED": "#d97706", "SKIPPED": "#2563eb", "UNSURE": "#6b7280"}
SHOWN = ["FAILED", "BLOCKED", "SKIPPED", "PASSED"]  # status order in the sidebar and tables (UNSURE last)
ICON = {"PASSED": "✓", "FAILED": "✗", "BLOCKED": "!", "SKIPPED": "»", "UNSURE": "?"}
PRIOS = ["High", "Medium", "Low"]
WHY = {"FAILED": "What went wrong", "BLOCKED": "Why it was blocked", "SKIPPED": "Why it was skipped", "UNSURE": "Why the answer is unsure"}
e = lambda s: html.escape(str(s if s is not None else ""))


def totals(tests): return {k: sum(1 for t in tests if t.get("status") == k) for k in COLORS}
def fmt(sec): return f"{sec // 3600} h {sec % 3600 // 60} min" if sec >= 3600 else f"{sec // 60} min {sec % 60} s"
def mode(t): return "LOGGED IN" if str(t.get("title", "")).startswith(("[LOGGED IN]", "[PLAYER]")) else "LOGGED OUT"
def mode_label(t): return mode(t).capitalize()
def short(t): return re.sub(r"^\[(LOGGED (IN|OUT)|PLAYER|GUEST)\]\s*", "", str(t.get("title") or ""))
def changes(t): return [str(c) for c in (t.get("account_changes") or [])]
def pct(n, d): return round(100 * n / d) if d else 0
def step_badge(s):
    """DONE / SKIPPED / PASS / FAIL label for one step."""
    if not s.get("ok", True): return "fail", "FAIL"
    if s.get("expected"): return "pass", "PASS"
    return ("done", "SKIPPED") if str(s.get("answer", "")).startswith("Skipped") else ("done", "DONE")


def run_label(run):
    """2026-10-28_1132 -> 28 Oct 11:32; anything else unchanged."""
    m = re.fullmatch(r"(\d{4})-(\d\d)-(\d\d)_(\d\d)(\d\d)", str(run or ""))
    if not m: return str(run or "")
    return f"{int(m[3])} {'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[int(m[2]) - 1]} {m[4]}:{m[5]}"


def load_categories(xlsx):
    """{TC ID: {"category", "subtype"}} from the "Test category" and "Sub-type" columns of testcases.xlsx, if present."""
    if not os.path.exists(xlsx): return {}
    import openpyxl
    try:
        ws = openpyxl.load_workbook(xlsx, read_only=True)["Test cases"]
    except Exception:
        return {}
    rows = ws.iter_rows(values_only=True)
    head = [str(c or "") for c in next(rows, [])]
    if "TC ID" not in head or "Test category" not in head: return {}
    ci, cc = head.index("TC ID"), head.index("Test category")
    cs = head.index("Sub-type") if "Sub-type" in head else None
    return {r[ci]: {"category": r[cc] or "", "subtype": (r[cs] if cs is not None else "") or ""}
            for r in rows if r and r[ci]}


CSS = """
:root{--bg:#f5f6f8;--card:#fff;--fg:#1d2330;--mut:#5f6b7a;--line:#e1e5ea;--pass:#1f8a4c;--fail:#c62828;--block:#b26a00;--done:#6b7685;--skip:#2563eb;--sel:#e8eefc;--link:#2563eb;--top:52px}
@media (prefers-color-scheme:dark){:root{--bg:#12151b;--card:#1b2029;--fg:#e8ebf0;--mut:#9aa5b4;--line:#2c3340;--pass:#4cc38a;--fail:#ff6b6b;--block:#f0a640;--done:#8b96a5;--skip:#6b9bff;--sel:#26304a;--link:#7aa7ff}}
*{box-sizing:border-box}html{scroll-padding-top:calc(var(--top) + 12px)}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,system-ui,Segoe UI,Roboto,sans-serif}
button,select{font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
button:hover,select:hover{border-color:var(--mut)}
a{color:var(--link)}h2,h3{line-height:1.3}
.top{position:sticky;top:0;z-index:20;height:var(--top);display:flex;align-items:center;gap:14px;padding:0 18px;background:var(--card);border-bottom:1px solid var(--line)}
.top h1{font-size:16px;margin:0;white-space:nowrap}.top h1 span{color:var(--mut);font-weight:500}
.top .sum{font-size:13px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.rate{margin-left:auto;font-size:13px;font-weight:600;white-space:nowrap;padding:3px 10px;border-radius:999px;background:color-mix(in srgb,var(--pass) 14%,transparent);color:var(--pass)}
.rate.bad{background:color-mix(in srgb,var(--fail) 12%,transparent);color:var(--fail)}
.menubtn{display:none;flex:none}
.wrap{display:grid;grid-template-columns:320px minmax(0,1fr)}
aside{position:sticky;top:var(--top);height:calc(100vh - var(--top));overflow:auto;border-right:1px solid var(--line);background:var(--card);padding:12px 10px 24px}
.links a{display:block;padding:6px 10px;border-radius:6px;color:inherit;text-decoration:none;font-weight:600;font-size:14px}.links a:hover,.item:hover{background:var(--bg)}
.links a.cur{background:var(--sel)}
.search{width:100%;padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit;margin:10px 0 8px}
.seg{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}.seg button{font-size:13px;padding:3px 9px;border-radius:999px}
.seg button.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.sel{display:grid;grid-template-columns:1fr 1fr;gap:4px}.sel select{font-size:13px;padding:4px 6px;min-width:0}
.reset{font-size:12px;color:var(--link);background:none;border:0;padding:4px 2px}.reset[hidden]{display:none}
.gh{font-size:12px;font-weight:700;color:var(--mut);letter-spacing:.04em;padding:14px 10px 4px}
.item{display:grid;grid-template-columns:16px 58px minmax(0,1fr);column-gap:4px;padding:6px 10px;border-radius:6px;color:inherit;text-decoration:none;font-size:14px}
.item .it{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.35}
.item .isub{grid-column:3;font-size:12px;color:var(--mut)}
.iid{font-weight:600;font-variant-numeric:tabular-nums}
.ic{font-weight:700}.i-failed .ic{color:var(--fail)}.i-passed .ic{color:var(--pass)}.i-blocked .ic{color:var(--block)}.i-skipped .ic{color:var(--skip)}.i-unsure .ic{color:var(--done)}
.item.cur{background:var(--sel)}
main{padding:24px 28px 80px;min-width:0}
.view{max-width:1180px}
.view>h2:first-child{margin:0 0 4px;font-size:22px}
.lead{color:var(--mut);margin:0 0 18px}
h3.sec{font-size:17px;margin:30px 0 10px}h3.sec .cnt{color:var(--mut);font-weight:500}
.b{display:inline-block;font-size:12px;font-weight:700;border-radius:4px;padding:1px 6px;color:#fff;vertical-align:middle;white-space:nowrap}
.b-passed,.b-pass{background:var(--pass)}.b-failed,.b-fail{background:var(--fail)}.b-blocked{background:var(--block)}.b-skipped{background:var(--skip)}.b-done,.b-unsure{background:var(--done)}
.m{font-size:12px;border:1px solid var(--line);border-radius:4px;padding:0 6px;color:var(--mut);white-space:nowrap}
.k-bug{color:var(--fail);border-color:color-mix(in srgb,var(--fail) 40%,transparent)}.k-wording{color:var(--block);border-color:color-mix(in srgb,var(--block) 45%,transparent)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .k{display:block;font-size:13px;color:var(--mut)}.card .v{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums}.card .s{margin-left:6px;color:var(--mut);font-size:14px}
.c-passed .v{color:var(--pass)}.c-failed .v{color:var(--fail)}.c-blocked .v{color:var(--block)}.c-skipped .v{color:var(--skip)}
.bar{display:flex;height:8px;border-radius:99px;overflow:hidden;background:var(--line)}.bar span{display:block}
.bar.big{height:12px;margin:14px 0 4px}
.s-passed{background:var(--pass)}.s-failed{background:var(--fail)}.s-blocked{background:var(--block)}.s-skipped{background:var(--skip)}.s-unsure{background:var(--done)}
.legend{font-size:13px;color:var(--mut);display:flex;gap:14px;flex-wrap:wrap}.legend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:18px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.panel h4{margin:0 0 6px;font-size:14px}.panel.wide{grid-column:1/-1}.panel.wide .rows{columns:2 300px;column-gap:28px}
.gr{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:10px;row-gap:3px;padding:6px 6px;border-radius:6px;break-inside:avoid;cursor:pointer}
.gr:hover{background:var(--bg)}.gr .gn{font-size:14px}.gr .gc{font-size:13px;color:var(--mut);font-variant-numeric:tabular-nums}.gr .bar{grid-column:1/-1;height:6px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{width:100%;border-collapse:collapse}
td,th{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}tr:last-child td{border-bottom:0}
th{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
td a{color:inherit;font-weight:600;text-decoration:none}.nw{white-space:nowrap}.sub{display:block;font-size:12px;color:var(--mut);margin-top:2px}
tbody tr[data-go]{cursor:pointer}tbody tr[data-go]:hover{background:var(--bg)}
.why{font-size:14px}
.chg{margin:0;padding-left:20px}.chg li{margin:3px 0}
.foot{color:var(--mut);font-size:13px;margin-top:28px;border-top:1px solid var(--line);padding-top:12px}
.case{background:var(--card);border:1px solid var(--line);border-top:5px solid var(--done);border-radius:10px;padding:18px 20px}
.case.v-passed{border-top-color:var(--pass)}.case.v-failed{border-top-color:var(--fail)}.case.v-blocked{border-top-color:var(--block)}.case.v-skipped{border-top-color:var(--skip)}
.crumb{font-size:13px;color:var(--mut);margin:0 0 4px}.crumb a{color:var(--mut)}
.ctitle{display:flex;gap:12px;align-items:flex-start;justify-content:space-between}.ctitle h2{font-size:21px;margin:0}
.nav{display:flex;gap:6px;flex:none}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px}.chips .m{font-size:13px;padding:2px 8px;border-radius:999px}
.box{margin:16px 0;padding:14px 16px;border-radius:8px;border:1px solid var(--line)}
.box h3{margin:0 0 6px;font-size:15px}.box p{margin:4px 0}
.box.v-failed{background:color-mix(in srgb,var(--fail) 7%,transparent);border-color:color-mix(in srgb,var(--fail) 30%,transparent)}
.box.v-blocked{background:color-mix(in srgb,var(--block) 8%,transparent);border-color:color-mix(in srgb,var(--block) 30%,transparent)}
.box.v-skipped{background:color-mix(in srgb,var(--skip) 7%,transparent);border-color:color-mix(in srgb,var(--skip) 30%,transparent)}
.box.v-passed{background:color-mix(in srgb,var(--pass) 7%,transparent);border-color:color-mix(in srgb,var(--pass) 30%,transparent)}
.fstep{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:16px;margin-top:12px;padding-top:12px;border-top:1px solid color-mix(in srgb,var(--fail) 25%,transparent)}
.fstep .fn{font-weight:700}.jump{font-size:13px;margin-top:8px}
.acct h3{margin:0 0 6px;font-size:15px}
.evid{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.btn{display:inline-block;font-size:14px;padding:5px 12px;border:1px solid var(--line);border-radius:6px;color:inherit;text-decoration:none;background:var(--card)}.btn:hover{border-color:var(--mut)}
.replay{margin:0 0 8px}.replay summary{cursor:pointer;color:var(--mut);font-size:14px}.replay img{width:640px;max-width:100%;border:1px solid var(--line);border-radius:6px;margin-top:8px}
.shead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:22px 0 6px}.shead h3{margin:0;font-size:16px}.tools{display:flex;gap:6px}.tools button{font-size:13px}
.steps{border-top:1px solid var(--line)}
.step{border-bottom:1px solid var(--line)}
.step summary{list-style:none;display:flex;align-items:center;gap:8px;padding:9px 6px;cursor:pointer}
.step summary::-webkit-details-marker{display:none}
.step summary::before{content:'▸';color:var(--mut);width:10px}.step[open] summary::before{content:'▾'}
.step .num{font-weight:700;min-width:22px;color:var(--mut);font-variant-numeric:tabular-nums}
.step .st{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;flex:1}
.step[open] .st{white-space:normal}
.step.r-fail{background:color-mix(in srgb,var(--fail) 7%,transparent)}
.step.flash{outline:2px solid var(--fail);outline-offset:-2px}
.body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);gap:16px;padding:4px 6px 14px 26px}
.txt p{margin:4px 0}.ans{font-size:14px}.ev{color:var(--mut);font-size:13px}
.shot img{width:100%;border:1px solid var(--line);border-radius:6px;display:block;margin-bottom:6px;min-height:40px}
.noshot{color:var(--block);font-size:13px;padding:8px;border:1px dashed var(--line);border-radius:6px}
.hint{color:var(--mut);font-size:12px;margin-top:16px;padding:0 10px}kbd{border:1px solid var(--line);border-radius:3px;padding:0 4px;font-size:11px}
.empty{color:var(--mut);font-size:13px;padding:8px 10px}
.md h2{margin-top:0}.md h3{margin:24px 0 6px}.md table{background:var(--card);border:1px solid var(--line);margin:8px 0 16px}.md td:first-child{white-space:nowrap}
.md code{font-size:13px;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:0 4px}
@media (max-width:900px){
 .wrap{grid-template-columns:1fr}.menubtn{display:inline-block}.top .sum,.top h1 span{display:none}.top{gap:10px;padding:0 12px}
 aside{position:fixed;left:0;top:var(--top);width:88vw;max-width:340px;z-index:15;transform:translateX(-105%);transition:transform .2s;box-shadow:0 6px 24px #0004}
 body.menu aside{transform:none}
 main{padding:16px 16px 60px}.body,.fstep{grid-template-columns:1fr}.body{padding-left:6px}.ctitle{flex-direction:column}.case{padding:14px}
 .hide-s{display:none}
}
"""

JS = """
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s) }
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)) }
  var f = { verdict: 'ALL', mode: 'ALL', cat: 'ALL', prio: 'ALL' }, query = ''
  function loadImgs(root) { $$('img[data-src]', root).forEach(function (i) { i.src = i.dataset.src; i.removeAttribute('data-src') }) }
  function visibleItems() { return $$('.item').filter(function (a) { return !a.hidden }) }
  function current() { return (location.hash || '#overview').slice(1) }
  function show() {
    var id = decodeURIComponent(current())
    var target = document.getElementById(id)
    if (!target || !target.classList.contains('view')) { id = 'overview'; target = document.getElementById('overview') }
    $$('.view').forEach(function (v) { v.hidden = v !== target })
    $$('.item').forEach(function (a) { a.classList.toggle('cur', a.dataset.id === id) })
    $$('.links a').forEach(function (a) { a.classList.toggle('cur', a.getAttribute('href') === '#' + id) })
    $$('details[open]', target).forEach(loadImgs)
    $$('.fstep', target).forEach(loadImgs)
    var cur = $('.item.cur'); if (cur) cur.scrollIntoView({ block: 'nearest' })
    window.scrollTo(0, 0)
    document.body.classList.remove('menu')
    var label = target.dataset.label || id
    document.title = label + ' — ' + document.body.dataset.site
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
  function match(el) {
    for (var k in f) if (f[k] !== 'ALL' && el.dataset[k] !== f[k]) return false
    return !query || el.dataset.text.indexOf(query) >= 0
  }
  function apply() {
    $$('.item').forEach(function (a) { a.hidden = !match(a) })
    $$('.grp').forEach(function (g) { g.hidden = !$$('.item', g).some(function (a) { return !a.hidden }) })
    $('.empty').hidden = visibleItems().length > 0
    $$('tr[data-verdict]').forEach(function (r) { r.hidden = !match(r) })
    $$('[data-count]').forEach(function (c) { c.textContent = $$('tbody tr[data-verdict]:not([hidden])', document.getElementById(c.dataset.count)).length })
    $$('.seg button').forEach(function (b) { b.classList.toggle('on', b.dataset.f === f.verdict) })
    $$('.sel select').forEach(function (s) { s.value = f[s.dataset.k] })
    $('.reset').hidden = query === '' && Object.keys(f).every(function (k) { return f[k] === 'ALL' })
  }
  $$('.seg button').forEach(function (b) { b.onclick = function () { f.verdict = b.dataset.f; apply() } })
  $$('.sel select').forEach(function (s) { s.onchange = function () { f[s.dataset.k] = s.value; apply() } })
  $$('.gr').forEach(function (g) { g.onclick = function () {
    f[g.dataset.k] = g.dataset.v; apply(); var t = document.getElementById('all'); if (t) t.scrollIntoView({ behavior: 'smooth' })
  } })
  $('.reset').onclick = function () { for (var k in f) f[k] = 'ALL'; query = ''; $('.search').value = ''; apply() }
  $('.search').addEventListener('input', function (e) { query = e.target.value.trim().toLowerCase(); apply() })
  $('.menubtn').onclick = function () { document.body.classList.toggle('menu') }
  $$('details').forEach(function (d) { d.addEventListener('toggle', function () { if (d.open) loadImgs(d) }) })
  $$('.prev').forEach(function (b) { b.onclick = function () { step(-1) } })
  $$('.next').forEach(function (b) { b.onclick = function () { step(1) } })
  $$('.expand').forEach(function (b) { b.onclick = function () { $$('details.step', b.closest('.case')).forEach(function (d) { d.open = true }) } })
  $$('.collapse').forEach(function (b) { b.onclick = function () { $$('details.step', b.closest('.case')).forEach(function (d) { d.open = false }) } })
  $$('.jump').forEach(function (b) { b.onclick = function () {
    var d = $('details.step[data-n="' + b.dataset.n + '"]', b.closest('.case')); if (!d) return
    d.open = true; d.scrollIntoView({ behavior: 'smooth', block: 'start' })
    d.classList.add('flash'); setTimeout(function () { d.classList.remove('flash') }, 1600)
  } })
  $$('tbody tr[data-go]').forEach(function (r) { r.onclick = function (e) { if (!e.target.closest('a')) go(r.dataset.go) } })
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


def render(tests, name, root, summary, show_run=False, intro="", views=(), info=None):
    """tests: result dicts; root: folder the evidence paths are relative to; summary: one-line description (plain text);
    show_run: show the run each result came from; intro: extra HTML for the overview footer;
    views: extra (id, label, html) pages, linked in the sidebar next to Overview;
    info: optional {TC ID: {"category", "subtype", "finding"}} (Functional / Non-functional, and bug or test wording)."""
    info = info or {}
    def exists(rel): return bool(rel) and os.path.exists(os.path.join(root, rel))
    def x(t, k): return str((info.get(t["id"]) or {}).get(k) or "")
    def cat_line(t): return " · ".join(p for p in (x(t, "category"), x(t, "subtype")) if p)
    def kind(t):
        k = x(t, "finding")
        if not k: return ""
        cls = "k-wording" if k.lower().startswith("test wording") else "k-bug"
        return f'<span class="m {cls}">{e(k)}</span>'
    def attrs(t):
        text = " ".join([t["id"], short(t), str(t.get("area") or ""), str(t.get("priority") or ""), str(t.get("reason") or ""),
                         str(t.get("run") or ""), cat_line(t), x(t, "finding")]).lower()
        return (f'data-verdict="{e(t.get("status"))}" data-mode="{mode(t)}" data-cat="{e(x(t, "category"))}" '
                f'data-prio="{e(t.get("priority"))}" data-text="{e(text)}"')

    tot = totals(tests)
    n = len(tests)
    total_sec = sum(int(t.get("duration_sec") or 0) for t in tests)
    statuses = [k for k in SHOWN + ["UNSURE"] if tot[k]]
    cats = sorted({x(t, "category") for t in tests} - {""})
    prio_rank = {p: i for i, p in enumerate(PRIOS)}
    st_rank = {k: i for i, k in enumerate(SHOWN + ["UNSURE"])}
    bad = tot["FAILED"] + tot["BLOCKED"]

    def bar(group, big=False):
        segs = "".join(f'<span class="s-{k.lower()}" style="width:{100 * sum(1 for t in group if t.get("status") == k) / len(group):.2f}%"></span>'
                       for k in ["PASSED", "FAILED", "BLOCKED", "SKIPPED", "UNSURE"] if group)
        return f'<div class="bar{" big" if big else ""}" aria-hidden="true">{segs}</div>'

    def panel(title, key, values, label=lambda v: v, wide=False):
        rows = []
        for v, group in values:
            if not group: continue
            p = sum(1 for t in group if t.get("status") == "PASSED")
            rows.append(f'<div class="gr" data-k="{key}" data-v="{e(v)}" title="Show only these tests"><span class="gn">{e(label(v))}</span>'
                        f'<span class="gc">{p} of {len(group)} passed</span>{bar(group)}</div>')
        return f'<div class="panel{" wide" if wide else ""}"><h4>{e(title)}</h4><div class="rows">{"".join(rows)}</div></div>'

    out = [f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Test results — {e(name)}</title><style>{CSS}</style></head><body data-site="{e(name)}">
<header class="top">
  <button class="menubtn" aria-label="Show tests">☰ Tests</button>
  <h1>{e(name)} <span>test results</span></h1>
  <span class="sum">{e(summary)}</span>
  <span class="rate{" bad" if bad else ""}">{pct(tot["PASSED"], n)}% passed · {tot["FAILED"]} failed</span>
</header>
<div class="wrap">
<aside>
  <nav class="links"><a href="#overview">Overview</a>""" +
           "".join(f'<a href="#{e(vid)}">{e(label)}</a>' for vid, label, _ in views) + """</nav>
  <input class="search" type="search" placeholder="Search tests…  ( / )" aria-label="Search tests">
  <div class="seg" role="group" aria-label="Status">""" +
           f'<button data-f="ALL">All {n}</button>' +
           "".join(f'<button data-f="{k}">{k.capitalize()} {tot[k]}</button>' for k in statuses) + """</div>
  <div class="sel">
    <select data-k="mode" aria-label="Mode"><option value="ALL">Logged out + in</option><option value="LOGGED OUT">Logged out</option><option value="LOGGED IN">Logged in</option></select>
    <select data-k="prio" aria-label="Priority"><option value="ALL">All priorities</option>""" +
           "".join(f'<option value="{p}">{p}</option>' for p in PRIOS) + "</select>" +
           (f'\n    <select data-k="cat" aria-label="Category"><option value="ALL">All categories</option>' +
            "".join(f'<option value="{e(c)}">{e(c)}</option>' for c in cats) + "</select>" if cats else "") + """
  </div>
  <button class="reset" hidden>Clear filters</button>"""]
    for k in statuses:
        group = [t for t in tests if t.get("status") == k]
        out.append(f'  <div class="grp"><div class="gh">{k} ({len(group)})</div>')
        for t in group:
            sub = " · ".join(p for p in (str(t.get("area") or ""), str(t.get("priority") or ""), mode_label(t)) if p)
            out.append(f'  <a class="item i-{k.lower()}" href="#{e(t["id"])}" data-id="{e(t["id"])}" {attrs(t)} '
                       f'title="{e(t["id"])} — {e(t.get("title"))}"><span class="ic">{ICON[k]}</span>'
                       f'<span class="iid">{e(t["id"])}</span><span class="it">{e(short(t))}</span><span class="isub">{e(sub)}</span></a>')
        out.append("  </div>")
    out.append("""  <div class="empty" hidden>No tests match.</div>
  <p class="hint"><kbd>j</kbd>/<kbd>k</kbd> next/previous · <kbd>n</kbd> next failed · <kbd>e</kbd> expand steps · <kbd>/</kbd> search</p>
</aside>
<main>""")

    # Overview: totals, breakdowns, tests that need attention, account changes, all tests
    out.append(f'<section class="view" id="overview" data-label="Overview">\n  <h2>Overview</h2>\n'
               f'  <p class="lead">{e(summary)} · total test time {fmt(total_sec)}</p>\n  <div class="cards">\n'
               f'    <div class="card"><span class="k">Tests</span><span class="v">{n}</span></div>')
    for k in ["PASSED", "FAILED", "BLOCKED", "SKIPPED", "UNSURE"]:
        if tot[k] or k in ("PASSED", "FAILED"):
            out.append(f'    <div class="card c-{k.lower()}"><span class="k">{k.capitalize()}</span><span class="v">{tot[k]}</span>'
                       f'<span class="s">{pct(tot[k], n)}%</span></div>')
    out.append(f'  </div>\n  {bar(tests, big=True)}\n  <div class="legend">' +
               "".join(f'<span><i class="s-{k.lower()}"></i>{k.capitalize()} {tot[k]}</span>' for k in ["PASSED", "FAILED", "BLOCKED", "SKIPPED", "UNSURE"] if tot[k]) + "</div>")
    out.append('  <div class="panels">')
    if cats:
        out.append("    " + panel("By category", "cat", [(c, [t for t in tests if x(t, "category") == c]) for c in cats]))
    out.append("    " + panel("By mode", "mode", [(m, [t for t in tests if mode(t) == m]) for m in ("LOGGED OUT", "LOGGED IN")], str.capitalize))
    out.append("    " + panel("By priority", "prio", [(p, [t for t in tests if t.get("priority") == p]) for p in PRIOS]))
    out.append("  </div>")

    attention = sorted([t for t in tests if t.get("status") != "PASSED"],
                       key=lambda t: (prio_rank.get(t.get("priority"), 9), st_rank.get(t.get("status"), 9), t["id"]))
    if attention:
        kind_th = '<th>Bug or test wording?</th>' if any(x(t, "finding") for t in attention) else ""
        out.append(f'  <h3 class="sec">Needs attention <span class="cnt">(<span data-count="attn">{len(attention)}</span>)</span></h3>\n'
                   f'  <div class="tw"><table id="attn"><thead><tr><th style="width:30%">Test</th><th>Status</th><th>Priority</th><th>What happened</th>{kind_th}</tr></thead><tbody>')
        for t in attention:
            st = t.get("status", "")
            sub = " · ".join(p for p in (str(t.get("area") or ""), mode_label(t), cat_line(t)) if p)
            out.append(f'  <tr {attrs(t)} data-go="{e(t["id"])}"><td><a href="#{e(t["id"])}">{e(t["id"])}</a> {e(short(t))}<span class="sub">{e(sub)}</span></td>'
                       f'<td><span class="b b-{e(st.lower())}">{e(st)}</span></td><td>{e(t.get("priority"))}</td>'
                       f'<td class="why">{e(t.get("reason"))}</td>{f"<td>{kind(t)}</td>" if kind_th else ""}</tr>')
        out.append("  </tbody></table></div>")

    changed = [t for t in tests if changes(t)]
    if changed:
        out.append(f'  <h3 class="sec">Changes to the test account <span class="cnt">({len(changed)} tests)</span></h3>\n'
                   '  <div class="tw"><table><thead><tr><th>Test</th><th>What changed</th></tr></thead><tbody>')
        for t in changed:
            out.append(f'  <tr data-go="{e(t["id"])}"><td><a href="#{e(t["id"])}">{e(t["id"])}</a> {e(short(t))}</td>'
                       f'<td><ul class="chg">{"".join(f"<li>{e(c)}</li>" for c in changes(t))}</ul></td></tr>')
        out.append("  </tbody></table></div>")

    run_th = '<th class="hide-s">Run</th>' if show_run else ""
    out.append(f'  <h3 class="sec" id="all">All tests <span class="cnt">(showing <span data-count="alltbl">{n}</span> of {n})</span></h3>\n'
               f'  <div class="tw"><table id="alltbl"><thead><tr><th>Test</th><th>Status</th><th>Priority</th><th class="hide-s">Mode</th>'
               f'{run_th}<th class="hide-s">Time</th></tr></thead><tbody>')
    for t in sorted(tests, key=lambda t: (st_rank.get(t.get("status"), 9), t["id"])):
        st = t.get("status", "")
        sub = " · ".join(p for p in (str(t.get("area") or ""), cat_line(t)) if p)
        run_td = f'<td class="nw hide-s">{e(run_label(t.get("run")))}</td>' if show_run else ""
        out.append(f'  <tr {attrs(t)} data-go="{e(t["id"])}"><td><a href="#{e(t["id"])}">{e(t["id"])}</a> {e(short(t))}<span class="sub">{e(sub)}</span></td>'
                   f'<td><span class="b b-{e(st.lower())}">{e(st)}</span></td><td>{e(t.get("priority"))}</td>'
                   f'<td class="nw hide-s">{mode_label(t)}</td>{run_td}<td class="nw hide-s">{e(t.get("duration_sec"))} s</td></tr>')
    out.append(f"""  </tbody></table></div>
  <div class="foot">{intro}<p>There is no real video: wdio-mcp cannot record the screen. Each test has a replay GIF of its step screenshots and a browser trace zip instead.</p></div>
</section>""")

    for vid, label, html_ in views:
        out.append(f'<section class="view md" id="{e(vid)}" data-label="{e(label)}" hidden>\n{html_}\n</section>')

    # One view per test: what went wrong first, then account changes, evidence and steps
    for t in tests:
        tid, st = t["id"], t.get("status", "")
        steps = t.get("steps", [])
        chips = [t.get("area"), f'{t.get("priority")} priority' if t.get("priority") else "", mode_label(t), cat_line(t),
                 f"{len(steps)} steps", f'{t.get("duration_sec")} s' if t.get("duration_sec") is not None else "",
                 f'Run {run_label(t.get("run"))}' if show_run and t.get("run") else ""]
        out.append(f"""<section class="view case v-{e(st.lower())}" id="{e(tid)}" data-label="{e(tid)}" hidden>
  <p class="crumb"><a href="#overview">Overview</a> / {e(tid)}</p>
  <div class="ctitle"><h2><span class="b b-{e(st.lower())}">{e(st)}</span> {e(short(t))}</h2>
  <div class="nav"><button class="prev" title="Previous test (k)">◀ Prev</button><button class="next" title="Next test (j)">Next ▶</button></div></div>
  <div class="chips"><span class="m">{e(tid)}</span>{"".join(f'<span class="m">{e(c)}</span>' for c in chips if c)}{kind(t)}</div>""")

        failed = [s for s in steps if not s.get("ok", True)]
        if st == "PASSED":
            checks = sum(1 for s in steps if s.get("expected"))
            note = f'<p class="ev">{e(t["reason"])}</p>' if t.get("reason") else ""
            out.append(f'  <div class="box v-passed"><p>All {checks} checks gave the expected answer.</p>{note}</div>')
        else:
            out.append(f'  <div class="box v-{e(st.lower())}"><h3>{WHY.get(st, "Result")}</h3><p>{e(t.get("reason"))}</p>')
            for s in failed:
                shot = s.get("screenshot")
                img = (f'<a href="{e(shot)}" target="_blank"><img data-src="{e(shot)}" alt="{e(tid)} step {e(s["n"])}"></a>'
                       if exists(shot) else '<div class="noshot">No screenshot</div>')
                exp = (f'<p class="ans">Expected <b>{e(s.get("expected"))}</b> · Actual <b>{e(s.get("answer"))}</b></p>'
                       if s.get("expected") else f'<p class="ans">Result <b>{e(s.get("answer"))}</b></p>')
                out.append(f'  <div class="fstep"><div><p class="fn">Step {e(s["n"])} failed</p><p>{e(s.get("text"))}</p>{exp}'
                           f'<p class="ev">{e(s.get("saw"))}</p><button class="jump" data-n="{e(s["n"])}">Show in steps ↓</button></div>'
                           f'<div class="shot">{img}</div></div>')
            out.append("  </div>")

        if changes(t):
            out.append('  <div class="box acct"><h3>Changes to the test account</h3><ul class="chg">' +
                       "".join(f"<li>{e(c)}</li>" for c in changes(t)) + "</ul></div>")

        files = [f'<a class="btn" href="{e(tid)}/">Evidence folder</a>']
        if exists(f"{tid}/{tid}_steps.pdf"): files.append(f'<a class="btn" href="{e(tid)}/{e(tid)}_steps.pdf">Steps PDF</a>')
        if exists(f"{tid}/{tid}_trace.zip"): files.append(f'<a class="btn" href="{e(tid)}/{e(tid)}_trace.zip">Trace zip</a>')
        out.append(f'  <div class="evid">{"".join(files)}</div>')
        gif = t.get("replay_gif") or f"{tid}/{tid}_replay.gif"
        if exists(gif):
            out.append(f'  <details class="replay"><summary>Replay of all steps (GIF)</summary><a href="{e(gif)}" target="_blank"><img data-src="{e(gif)}" alt="{e(tid)} replay"></a></details>')
        out.append(f'  <div class="shead"><h3>Steps ({len(steps)})</h3><div class="tools"><button class="expand">Expand all</button>'
                   '<button class="collapse">Collapse all</button></div></div>\n  <div class="steps">')
        for s in steps:
            cls, label = step_badge(s)
            shot = s.get("screenshot")
            img = (f'<a href="{e(shot)}" target="_blank"><img data-src="{e(shot)}" alt="{e(tid)} step {e(s["n"])}"></a>'
                   if exists(shot) else '<div class="noshot">No screenshot</div>')
            ans = (f'Expected <b>{e(s.get("expected"))}</b> · Actual <b>{e(s.get("answer"))}</b>' if s.get("expected")
                   else f'Result <b>{e(s.get("answer"))}</b>')
            out.append(f'  <details class="step r-{cls}" data-n="{e(s["n"])}"><summary><span class="num">{e(s["n"])}</span>'
                       f'<span class="b b-{cls}">{label}</span><span class="st">{e(s.get("text"))}</span></summary>'
                       f'<div class="body"><div class="txt"><p>{e(s.get("text"))}</p><p class="ans">{ans}</p>'
                       f'<p class="ev">{e(s.get("saw"))}</p></div><div class="shot">{img}</div></div></details>')
        out.append("  </div>\n</section>")
    out.append(f"</main>\n</div>\n<script>{JS}</script>\n</body></html>")
    return "\n".join(out)
