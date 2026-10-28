---
description: Combine all test runs of a website into one Results folder with one report
argument-hint: <site name>
---

Arguments: $ARGUMENTS
The first argument is the site name. SITE = website-tests/<site name>/ (absolute path). PROJECT = the project folder (absolute path).
Do not run any tests. Only gather files and build the report.

## Step 1: Check
Make sure SITE/runs/ exists and has at least one run folder with results/*.json, or an existing SITE/runs/Results/json/ folder. If there is nothing, stop and tell me.

## Step 2: Gather
Run: python3 "<PROJECT>/.claude/scripts/gather_results.py" "<SITE>/runs" "<site name>"
It takes the newest result of every test (from every run folder and from the existing Results/json/), COPIES the evidence into SITE/runs/Results/<TC ID>/ and writes:
- Results/results.html: all tests in one report, in the same layout as a run's report.html (both come from .claude/scripts/report_html.py): totals and status filters at the top, LOGGED OUT / LOGGED IN and priority filters, a searchable sidebar of tests, an overview table with the run each result came from, and one view per test with its steps, screenshots, replay GIF and failed steps in red. It only links to files inside Results/.
- Results/results.xlsx: sheets "Summary", "Results" and "Steps".
- Results/json/<TC ID>.json: the raw result of every test.
It never moves or deletes anything in the run folders.

## Step 3: README
If SITE/runs/Results/README.md does not exist, write one that explains, in plain English for someone new: what the folder is, which file to open first, what every file in a test folder is, what PASSED, FAILED, BLOCKED, SKIPPED (the reward was already claimed or on cooldown, so the action could not be tried) and UNSURE mean, what [LOGGED OUT] and [LOGGED IN] mean, what "Account changes" means, and a table of the tests that are not PASSED. If it exists, update only its totals and its table of tests that are not PASSED.

## Step 4: Tell me
Show the number of tests in the report, the totals, and which runs were used.
Check that every link in results.html points to a file inside Results/ and say if any is broken.
End with: open "<SITE>/runs/Results/results.html" (with the real path).
