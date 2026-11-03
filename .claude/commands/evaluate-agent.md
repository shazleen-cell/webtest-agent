---
description: Evaluate the web test agent itself, by running the eval set and scoring it against the known right answers
argument-hint: [run | score | compare] [eval site, default demoblaze-eval]
---

Arguments: $ARGUMENTS
The first argument is the mode (default: run):
- **run**: run the eval set, score the new run, and compare it with earlier runs.
- **score**: score the newest existing run again. Runs nothing in the browser.
- **compare**: score every existing run and build the comparison. Runs nothing in the browser.
The second argument is the eval site (default: demoblaze-eval). SITE = PROJECT/website-tests/<eval site>/ (absolute path). PROJECT = the project folder (absolute path).
SCORE SCRIPT = PROJECT/.claude/scripts/eval_score.py.

This command checks **the agent**, not the website. Every case in SITE/testcases.xlsx has a known right result in SITE/golden.json. The eval only works when the agent runs under the real rules, so:
- Never edit SITE/golden.json, SITE/settings.md or SITE/testcases.xlsx to make a case pass.
- Never loosen a safety rule, an opt-in section or the "Never" list for the eval.
- Never re-run a case, work around it or fix its result by hand. A wrong result is what the eval is meant to find.

## Step 1: Check
Make sure SITE/golden.json and SITE/testcases.xlsx exist. If not, stop and tell me this site has no eval set.
For mode run: make sure SITE/settings.local.md exists (git ignores it). If it is missing, stop and tell me to copy it from the matching real site (for demoblaze-eval: website-tests/demoblaze/settings.local.md). Do not create it with made-up values.
For modes score and compare: make sure SITE/runs/ has at least one run folder with results/. If not, stop and tell me to use /evaluate-agent run first.
Read the website-tester's model and effort from the frontmatter of PROJECT/.claude/agents/website-tester.md, and tell me which setup is being evaluated.

## Step 2: Run (mode run only)
Read PROJECT/.claude/commands/run-tests.md and follow its Steps 1 to 4 for this site, with no filter. This includes its safety check: cases it does not run must be listed in "refused" in RUN/run_timing.json, because the score script counts a refused safety trap as stopped. Do not do its Step 5; Step 4 below replaces it.
Use the same batches, evidence checks, timing, secret scrubbing and report building as /run-tests.

## Step 3: Score
- mode run: python3 "<SCORE SCRIPT>" "<SITE>" "<RUN>". If SITE/runs/ has other scored or unscored runs, also run python3 "<SCORE SCRIPT>" "<SITE>" --all for the comparison.
- mode score: python3 "<SCORE SCRIPT>" "<SITE>"
- mode compare: python3 "<SCORE SCRIPT>" "<SITE>" --all
Exit code 1 means the verdict is FAIL. That is a result, not an error: still report it. Any other error from the script: stop and show it to me.
The script writes RUN/eval_report.html, RUN/eval_score.md and RUN/eval_score.json for each scored run, and SITE/runs/eval_comparison.html when it scores more than one run.

## Step 4: Tell me
1. The setup (website-tester model and effort, coordinator model), the run, and the **verdict** (PASS or FAIL).
2. Every check from the scorecard with ✓ or ✗.
3. A short table: right status, right Yes/No answers, false PASSED, false FAILED, wrong expected answers caught, safety traps stopped (and by the coordinator or the website-tester), evidence complete, full run time, website-tester time, tokens.
4. Every case with a wrong result: case, kind, right result, agent's result, and the problem. Say which look like an agent mistake and which may be the site changing: a known case that comes back wrong in every run of every setup may mean the site changed. Then a person must re-check it on the live site before golden.json is changed.
5. For mode run or compare with more than one run: the comparison table and any flaky cases.
6. If all safety traps were stopped by the coordinator, remind me that the website-tester's own safety rules were not tested by this run.
End with the commands to open the reports, with the real paths:
open "<RUN>/eval_report.html"
and, if it was written: open "<SITE>/runs/eval_comparison.html"
To evaluate another setup, tell me to change `model` or `effort` in .claude/agents/website-tester.md and run /evaluate-agent again, then set it back.
