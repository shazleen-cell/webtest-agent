#!/usr/bin/env python3
"""Get the person's attention ONLY when Claude Code needs them to answer or do something. Called by the project hooks
in .claude/settings.json (a question, or a permission prompt); never for progress updates.

Usage: notify_person.py "<short message>"

Plays a short chime exactly twice ("ting ting", macOS afplay) and, if `terminal-notifier` is installed
(brew install terminal-notifier), shows a silent desktop notification. No other sound. It never uses AppleScript
or System Events. Never put a card value or a test-account value in the message.
"""
import shutil
import subprocess
import sys

SOUND = "/System/Library/Sounds/Glass.aiff"


def main():
    msg = " ".join(sys.argv[1:]).strip() or "The test run needs you in Claude Code"
    if shutil.which("afplay"):
        for _ in range(2):  # "ting ting": two short chimes, no more
            subprocess.run(["afplay", SOUND], check=False)
    if shutil.which("terminal-notifier"):
        subprocess.run(["terminal-notifier", "-title", "Website tests", "-message", msg], check=False)
    print(f"notified: {msg}")


if __name__ == "__main__":
    main()
