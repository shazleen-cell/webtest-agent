#!/usr/bin/env python3
"""Post a short summary of a test run to Slack with an incoming webhook (no AI, no tokens).

Usage:
    python3 slack_summary.py <RUN or Results folder> <SITE> <site name> [--send] [--json]

<RUN> is a run folder with results/*.json (from /run-tests); a Results folder (from /gather-results) has json/*.json.
The numbers come from the same helpers as report.html, so they match the report.

Without --send it only prints the message (dry run). With --send it posts it to the webhook in
.claude/slack.local.md (line "- SLACK_WEBHOOK_URL: https://hooks.slack.com/...", git-ignored) or in the
SLACK_WEBHOOK_URL environment variable; if neither is set it prints the message and says it was not sent.
--json prints the Slack payload instead of the plain text.

The message never has evidence (screenshots, videos, traces) or links to it. Before sending, it is checked
against the real test-account values in SITE/settings.local.md: if one is found, nothing is sent.
Exit code: 0 = sent or dry run, 1 = not sent because of an error or a secret found, 2 = wrong arguments.
A failed post never changes the run's results or reports.
"""
import glob, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_html import PRIOS, SHOWN, totals, is_pay_skip, mode, short, changes, pct, fmt, load_categories, load_timing, run_time  # noqa: E402
from scrub_secrets import load_secrets  # noqa: E402

PROJECT = Path(__file__).resolve().parents[2]
CONFIG = PROJECT / ".claude" / "slack.local.md"
MAX_LISTED = 10
# Anything that looks like an evidence file is cut out of the reasons shown in Slack.
EVIDENCE = re.compile(r"\S+\.(png|jpe?g|gif|mp4|webm|zip|pdf|json|html)\b", re.I)


def load_tests(folder):
    files = glob.glob(os.path.join(folder, "results", "*.json")) or glob.glob(os.path.join(folder, "json", "*.json"))
    tests = []
    for p in sorted(files):
        with open(p, encoding="utf-8") as f:
            tests.append(json.load(f))
    return sorted(tests, key=lambda t: t["id"])


def load_run_timing(folder, tests):
    """run_time() of a run folder, or of the runs a Results folder was gathered from (like gather_results.py)."""
    if os.path.exists(os.path.join(folder, "results")):
        return run_time([load_timing(folder)], [os.path.basename(folder)])
    runs = sorted({t["run"] for t in tests if t.get("run")})
    parent = os.path.dirname(folder)
    return run_time([load_timing(os.path.join(parent, r)) for r in runs], runs) if runs else None


def esc(s):
    """Slack mrkdwn escaping."""
    return str(s if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def one_line(s, limit=140):
    s = EVIDENCE.sub("[file]", " ".join(str(s or "").split()))
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def build(folder, site, name):
    tests = load_tests(folder)
    if not tests:
        sys.exit(f"no results in {folder} (expected results/*.json or json/*.json)")
    label = os.path.basename(folder.rstrip("/"))
    is_gathered = not os.path.exists(os.path.join(folder, "results"))
    info = load_categories(os.path.join(site, "testcases.xlsx"))
    timing = load_run_timing(folder, tests)

    tot = totals(tests)
    pay = [t for t in tests if is_pay_skip(t)]
    ran_tests = [t for t in tests if not is_pay_skip(t)]
    ran = len(ran_tests)
    tot_ran = totals(ran_tests)
    rate = pct(tot["PASSED"], ran)
    nice = name[:1].upper() + name[1:]
    what = f"results {re.sub(r'^Results_?', '', label) or 'all runs'}" if is_gathered else f"test run {label}"
    title = f"{nice} {what}: {tot['PASSED']} passed, {tot['FAILED']} failed ({rate}%)"

    def passed_of(group):
        p = sum(1 for t in group if t.get("status") == "PASSED")
        return f"{p} of {len(group)} passed ({pct(p, len(group))}%)"

    status_line = " · ".join(f"{k.capitalize()} {tot_ran[k]}" for k in ["PASSED", "FAILED", "BLOCKED", "SKIPPED", "UNSURE"]
                             if tot_ran[k] or k in ("PASSED", "FAILED"))
    if pay:
        status_line += f" · Skipped (payment) {len(pay)}, not run, no money spent"
    lines = [f"*{len(tests)} test{'s' if len(tests) != 1 else ''}:* {status_line}"]
    for m in ("LOGGED OUT", "LOGGED IN"):
        group = [t for t in ran_tests if mode(t) == m]
        if group:
            lines.append(f"*{m.capitalize()}:* {passed_of(group)}")
    cats = sorted({(info.get(t["id"]) or {}).get("category") or "" for t in ran_tests} - {""})
    for c in cats:
        lines.append(f"*{esc(c)}:* {passed_of([t for t in ran_tests if (info.get(t['id']) or {}).get('category') == c])}")
    summary = "\n".join(lines)

    prio_rank = {p: i for i, p in enumerate(PRIOS)}
    st_rank = {k: i for i, k in enumerate(SHOWN + ["UNSURE"])}
    attention = sorted([t for t in ran_tests if t.get("status") != "PASSED"],
                       key=lambda t: (prio_rank.get(t.get("priority"), 9), st_rank.get(t.get("status"), 9), t["id"]))
    att = ""
    if attention:
        rows = [f"• *{esc(t['id'])}* {esc(t.get('status'))}, {esc(t.get('priority') or '?')}: {esc(one_line(short(t), 90))}"
                f"\n      _{esc(one_line(t.get('reason')))}_" for t in attention[:MAX_LISTED]]
        if len(attention) > MAX_LISTED:
            rows.append(f"…and {len(attention) - MAX_LISTED} more in the report")
        att = f"*Needs attention ({len(attention)})*\n" + "\n".join(rows)

    changed = [t for t in tests if changes(t)]
    chg = ""
    if changed:
        rows = [f"• *{esc(t['id'])}*: {esc(one_line('; '.join(changes(t)), 160))}" for t in changed[:MAX_LISTED]]
        if len(changed) > MAX_LISTED:
            rows.append(f"…and {len(changed) - MAX_LISTED} more in the report")
        chg = f"*Changes to the test account ({len(changed)})*\n" + "\n".join(rows)

    facts = []
    if timing:
        facts.append(f"Run time {fmt(timing['full'])} (website-tester {fmt(timing['tester'])})")
        c = timing.get("cost") or {}
        if c.get("total_usd") is not None:
            facts.append(f"website-tester cost {'≈ ' if c.get('estimated') else ''}${c['total_usd']:.2f}")
    report = "results.html" if is_gathered else "report.html"
    try:
        where = os.path.relpath(os.path.join(os.path.abspath(folder), report), PROJECT)
    except ValueError:
        where = report
    footer = " · ".join(facts + [f"Full report: {where} on the computer that ran the tests"])

    blocks = [{"type": "header", "text": {"type": "plain_text", "text": title[:150], "emoji": False}},
              {"type": "section", "text": {"type": "mrkdwn", "text": summary}}]
    for part in (att, chg):
        if part:
            blocks += [{"type": "divider"}, {"type": "section", "text": {"type": "mrkdwn", "text": part[:3000]}}]
    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": esc(footer)[:3000]}]})
    text = "\n\n".join(p for p in (title, summary, att, chg, footer) if p)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return {"text": title, "blocks": blocks}, text


def webhook():
    url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not url and CONFIG.exists():
        m = re.search(r"^[ \t]*-[ \t]*SLACK_WEBHOOK_URL[ \t]*:[ \t]*(\S+)", CONFIG.read_text(encoding="utf-8"), re.M)
        url = m.group(1) if m else ""
    return url if url.startswith("https://hooks.slack.com/") else ""


def send(payload, url):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", "replace").strip()
            return r.status == 200 and body == "ok", f"{r.status} {body[:200]}"
    except urllib.error.HTTPError as e:
        return False, f"{e.code} {e.read().decode('utf-8', 'replace')[:200]}"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return False, f"connection failed: {getattr(e, 'reason', e)}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 3 or flags - {"--send", "--json"}:
        print(__doc__)
        return 2
    folder, site, name = os.path.abspath(args[0]), os.path.abspath(args[1]), args[2]
    payload, text = build(folder, site, name)
    print(json.dumps(payload, indent=2, ensure_ascii=False) if "--json" in flags else text)
    print()

    found = [k for k, v in load_secrets(Path(site)).items() if v in json.dumps(payload, ensure_ascii=False)]
    if found:
        print(f"NOT SENT: the message contains the real value of {', '.join(found)} from settings.local.md. "
              "Run scrub_secrets.py on the site and build the report again.")
        return 1
    if "--send" not in flags:
        print("dry run: not sent (add --send to post it)")
        return 0
    url = webhook()
    if not url:
        print("dry run: not sent, no webhook set (.claude/slack.local.md or SLACK_WEBHOOK_URL)")
        return 0
    ok, why = send(payload, url)
    print("sent to Slack" if ok else f"NOT SENT: Slack answered {why}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
