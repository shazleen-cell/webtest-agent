---
description: Combine test runs of a website into one Results folder with one report (all runs, or only the runs you name)
argument-hint: <site name> [run folder ...]
---

Arguments: $ARGUMENTS
The first argument is the site name. SITE = website-tests/<site name>/ (absolute path). PROJECT = the project folder (absolute path).
The other arguments are optional run folder names inside SITE/runs/ (for example 2026-11-16_0915 2026-11-16_1121).
- No run names: combine ALL runs. OUT = SITE/runs/Results/.
- With run names: combine ONLY those runs. OUT = SITE/runs/Results_<first run>_to_<last run>/ (the date is left out of the last run when both runs are on the same day, for example Results_2026-11-16_0915_to_1121; one run gives Results_<run>/). SITE/runs/Results/ is not touched.
Do not run any tests. Only gather files and build the report.

## Step 1: Check
Without run names: make sure SITE/runs/ exists and has at least one run folder with results/*.json, or an existing SITE/runs/Results/json/ folder.
With run names: make sure every named folder exists in SITE/runs/ and has results/*.json. If a name looks wrong, list the run folders in SITE/runs/ so I can pick.
If there is nothing to gather, stop and tell me.

## Step 2: Gather
Run: python3 "<PROJECT>/.claude/scripts/gather_results.py" "<SITE>/runs" "<site name>" [run folder ...]
(pass the run names exactly as given). The script prints the output folder as its last line ("output: ..."); that is OUT.
It takes the newest result of every test (without run names: from every run folder and from the existing Results/json/; with run names: only from those runs), COPIES the evidence into OUT/<TC ID>/ and writes:
- OUT/results.html: all tests in one report, in the same layout as a run's report.html (both come from .claude/scripts/report_html.py), plus the run each result came from and a "How to read this report" page made from README.md. Categories come from the Test category column of SITE/testcases.xlsx, and the "Bug or test wording?" labels from the README table of tests that are not PASSED. It only links to files inside OUT.
- OUT/results.xlsx: sheets "Summary", "Results" and "Steps".
- OUT/json/<TC ID>.json: the raw result of every test.
It never moves or deletes anything in the run folders.
Then run: python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE>" — it replaces any real test-account value (from SITE/settings.local.md) in README.md, results.xlsx and json/ of runs/Results/ and every runs/Results_*/ folder with its placeholder. If it scrubbed anything, run the Step 2 command again so results.html is rebuilt from the clean JSON.

## Step 3: README
If OUT/README.md does not exist, write one that explains, in plain English for someone new: what the folder is (and, with run names, which runs it combines), which file to open first, what every file in a test folder is, what PASSED, FAILED, BLOCKED, SKIPPED (the reward was already claimed or on cooldown, so the action could not be tried) and UNSURE mean, what [LOGGED OUT] and [LOGGED IN] mean, what "Account changes" means, and a table of the tests that are not PASSED under the heading "## Tests that did not pass", with the columns TC, Test, Priority, What happened, Bug or test wording? (Bug, Content bug, Security finding, Accessibility, SEO, or Test wording). If it exists, update only its totals and its table of tests that are not PASSED, keeping that heading and those columns. Then run the Step 2 command again so results.html picks up the new table.

## Step 4: Tell me
Show the number of tests in the report, the totals, which runs were used and the OUT folder.
Check that every link in results.html points to a file inside OUT and say if any is broken.
End with: open "<OUT>/results.html" (with the real path).
