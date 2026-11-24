#!/usr/bin/env python3
"""Card guard for /run-tests <site> payment-human: nothing is captured while a PERSON types a card.

Usage:
  card_guard.py on <RUN> <TC ID>   starts the card step: writes .claude/card_step.flag
  card_guard.py off                ends it: removes the flag
  card_guard.py status             says whether the guard is on
  card_guard.py hook               the Claude Code PreToolUse hook (the tool call arrives as JSON on stdin)
  card_guard.py selftest           checks the rules below without a browser

While the flag exists (and is younger than MAX_AGE), the hook refuses these wdio-mcp calls, so the agent cannot
capture or type even by mistake:
  - get_screenshot and snapshot (a screenshot or an accessibility tree can show what was typed)
  - set_value, perform_actions and select_option (the agent types nothing in the payment window)
  - execute_script, unless it is a read-only script that returns only the visible status or error messages
    (it must contain role=alert, and must not read values, HTML, the whole body, or click, scroll or submit)
  - click_element on a selector that names Pay, Buy, Purchase, Checkout, Submit, Confirm or Subscribe
    (a click by ref such as e12 cannot be checked: the agent is told never to click Pay)
  - start_session with trace on (a trace records typed values)
Calls to other tools are not touched. The hook is set in .claude/settings.json and Claude Code only loads it when it
was started in the project folder: /run-tests checks it before it opens a payment window.
A flag older than MAX_AGE is ignored, so a forgotten flag cannot block later runs for ever."""
import json
import os
import re
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
FLAG = PROJECT / ".claude" / "card_step.flag"
MAX_AGE = 90 * 60  # seconds
PAY_WORDS = re.compile(r"\b(pay|buy|purchase|checkout|submit|confirm|subscribe)\b", re.I)
UNSAFE_SCRIPT = re.compile(
    r"\.value\b|\bvalue\s*[:=]|innerHTML|outerHTML|document\.body|documentElement|FormData|\binput\b|\btextarea\b"
    r"|\.click\s*\(|\.focus\s*\(|\.submit\s*\(|dispatchEvent|scroll|location\s*=|\.select\s*\(|execCommand", re.I)
BLOCKED = {
    "get_screenshot": "no screenshot while a person types the card",
    "snapshot": "no snapshot while a person types the card (it can show typed values)",
    "set_value": "the agent types nothing in the payment window",
    "perform_actions": "the agent types and clicks nothing in bulk in the payment window",
    "select_option": "the agent types nothing in the payment window",
}


def active():
    try:
        return time.time() - FLAG.stat().st_mtime < MAX_AGE
    except OSError:
        return False


def safe_read(script):
    """True for a read-only script that returns only visible status or error messages."""
    return bool(re.search(r"role\s*=\s*['\"]?alert", script or "", re.I)) and not UNSAFE_SCRIPT.search(script or "")


def decide(tool_name, tool_input):
    """None = allowed. Otherwise the reason it is refused."""
    if "wdio" not in tool_name:
        return None
    short = tool_name.split("__")[-1]
    tool_input = tool_input or {}
    if short in BLOCKED:
        return BLOCKED[short]
    if short == "execute_script" and not safe_read(str(tool_input.get("script", ""))):
        return "only the read-only status/error script is allowed (it must contain role=alert and read no values)"
    if short == "click_element" and PAY_WORDS.search(str(tool_input.get("selector", ""))):
        return "never click Pay, Buy, Purchase, Checkout, Submit, Confirm or Subscribe: the person clicks Pay"
    if short == "start_session" and tool_input.get("trace"):
        return "no trace while the card step is on (a trace records typed values)"
    return None


def hook():
    if not active():
        return 0
    try:
        call = json.load(sys.stdin)
    except ValueError:
        return 0
    reason = decide(str(call.get("tool_name", "")), call.get("tool_input"))
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": f"CARD GUARD: {reason}. The card step is on (see .claude/rules/opt-in.md, section 5). "
                                        "Do not work around this."}}))
    return 0


def on(run, tc):
    FLAG.write_text(json.dumps({"run": run, "tc": tc, "since": time.strftime("%Y-%m-%dT%H:%M:%S")}))
    registered = False
    try:
        registered = "card_guard.py" in (PROJECT / ".claude" / "settings.json").read_text()
    except OSError:
        pass
    print(f"card guard ON for {tc}: screenshots, snapshots and typing are blocked until `card_guard.py off`")
    if not registered:
        print("WARNING: .claude/settings.json does not register the hook, so nothing is blocked. Do not open a payment window.")


def off():
    try:
        FLAG.unlink()
        print("card guard OFF")
    except FileNotFoundError:
        print("card guard was already OFF")


def selftest():
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = (got is None) == want
        ok &= good
        print(("ok   " if good else "FAIL ") + name)

    wd = "mcp__wdio-mcp__"
    approved = ("return Array.from(document.querySelectorAll('[role=alert], [role=status], [class*=error i], [class*=success i], h1, h2'))"
                ".map(e => e.innerText.trim()).filter(Boolean)")
    check("screenshot refused", decide(wd + "get_screenshot", {}), False)
    check("snapshot refused", decide(wd + "snapshot", {"find": "x"}), False)
    check("set_value refused", decide(wd + "set_value", {"selector": "e1", "value": "x"}), False)
    check("perform_actions refused", decide(wd + "perform_actions", {"actions": []}), False)
    check("approved read script allowed", decide(wd + "execute_script", {"script": approved}), True)
    check("script reading .value refused", decide(wd + "execute_script", {"script": "return document.querySelector('[role=alert]').value"}), False)
    check("script without role=alert refused", decide(wd + "execute_script", {"script": "return document.title"}), False)
    check("script reading the body refused", decide(wd + "execute_script", {"script": "return document.body.innerText // role=alert"}), False)
    check("script that clicks refused", decide(wd + "execute_script", {"script": "document.querySelector('[role=alert]').click()"}), False)
    check("click Pay by text refused", decide(wd + "click_element", {"selector": "button=Pay"}), False)
    check("click back arrow allowed", decide(wd + "click_element", {"selector": "button=Ludus"}), True)
    check("click by ref allowed", decide(wd + "click_element", {"selector": "e12"}), True)
    check("trace session refused", decide(wd + "start_session", {"trace": True}), False)
    check("session without trace allowed", decide(wd + "start_session", {"trace": False, "attach": True}), True)
    check("switch_frame allowed", decide(wd + "switch_frame", {}), True)
    check("scroll allowed", decide(wd + "scroll", {"direction": "down"}), True)
    check("other tools untouched", decide("Bash", {"command": "ls"}), True)
    return 0 if ok else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "hook":
        sys.exit(hook())
    if cmd == "on" and len(sys.argv) == 4:
        on(sys.argv[2], sys.argv[3])
    elif cmd == "off":
        off()
    elif cmd == "status":
        print("card guard ON" if active() else "card guard OFF")
    elif cmd == "selftest":
        sys.exit(selftest())
    else:
        sys.exit(__doc__)
