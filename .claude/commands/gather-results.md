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
- Results/results.html: all tests in one report, in the same layout as a run's report.html (both come from .claude/scripts/report_html.py), plus the run each result came from and a "How to read this report" page made from README.md. Categories come from the Test category column of SITE/testcases.xlsx, and the "Bug or test wording?" labels from the README table of tests that are not PASSED. It only links to files inside Results/.
- Results/results.xlsx: sheets "Summary", "Results" and "Steps".
- Results/json/<TC ID>.json: the raw result of every test.
It never moves or deletes anything in the run folders.
Then run: python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE>" — it replaces any real test-account value (from SITE/settings.local.md) in Results/README.md, results.xlsx and json/ with its placeholder. If it scrubbed anything, run the Step 2 command again so results.html is rebuilt from the clean JSON.

## Step 3: README
If SITE/runs/Results/README.md does not exist, write one that explains, in plain English for someone new: what the folder is, which file to open first, what every file in a test folder is, what PASSED, FAILED, BLOCKED, SKIPPED (the reward was already claimed or on cooldown, so the action could not be tried) and UNSURE mean, what [LOGGED OUT] and [LOGGED IN] mean, what "Account changes" means, and a table of the tests that are not PASSED under the heading "## Tests that did not pass", with the columns TC, Test, Priority, What happened, Bug or test wording? (Bug, Content bug, Security finding, Accessibility, SEO, or Test wording). If it exists, update only its totals and its table of tests that are not PASSED, keeping that heading and those columns. Then run the Step 2 command again so results.html picks up the new table.

## Step 4: Tell me
Show the number of tests in the report, the totals, and which runs were used.
Check that every link in results.html points to a file inside Results/ and say if any is broken.
End with: open "<SITE>/runs/Results/results.html" (with the real path).
