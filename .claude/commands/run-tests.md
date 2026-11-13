---
description: Run the approved test cases for a website and make HTML and Excel reports
argument-hint: <site name> [High | LoggedOut | LoggedIn | Changes | TC-01,TC-05]
---

Arguments: $ARGUMENTS
The first argument is the site name. SITE = website-tests/<site name>/.
The optional second argument is a filter: a priority (High, Medium, Low), a mode (LoggedOut or LoggedIn, matching the [LOGGED OUT] / [LOGGED IN] tag at the start of the title; old tags: [GUEST] and no tag = LoggedOut, [PLAYER] = LoggedIn; Guest and Player also work as filter names), Changes (only the cases with Changes account = Yes), or a list of TC IDs.
PROJECT = the project folder (absolute path). EVIDENCE SCRIPT = PROJECT/.claude/scripts/test_evidence.py.

## Step 1: Load the approved tests
Use python3 with openpyxl to read SITE/testcases.xlsx and take only rows where Approved is Yes, then apply the filter.
If there are none, stop and tell me.
Read SITE/settings.md: the "Login (LOGGED IN mode)" section, "Allowed when LOGGED IN", "Allowed when LOGGED OUT", "Never", and the opt-in sections "Allowed to type", "Allowed cart actions" and "Allowed demo checkout" if present (see .claude/rules/opt-in.md). The website-tester agent needs these.
Also read SITE/settings.local.md (ignored by git). It holds the real test-account values, for example `- TEST_USER_ID: <id>`, for the placeholders such as {TEST_USER_ID} in settings.md and in the Start URLs and Steps. If an approved [LOGGED IN] case uses a placeholder whose value is missing, stop and ask me for it.
Check that Pillow is installed (python3 -c "import PIL"). If it is missing, run: pip3 install --user pillow
Safety check before running (never skipped by /run-tests, whatever the arguments or the site): read the Steps of every approved case. If any action step clicks or presses something that pays or purchases (a button with a real-money price, Buy, Purchase, Pay, Checkout, Add to cart, the final button of the gift flow) or anything in the "Never" list of settings.md, do NOT run that case. List it for me with the TC ID and the step, and run the rest. Claim, spending loyalty points and Logout are allowed if settings.md allows them. A step that types, changes the cart or checks out may run only if the matching opt-in section has status ON and lists that exact field, value or button; otherwise do NOT run that case and list it for me.

## Step 2: Make the run folder
RUN = SITE/runs/<YYYY-MM-DD_HHMM>/ (absolute path) with a subfolder results/ and one evidence folder per test: RUN/<TC ID>/ (for example RUN/TC-001/).
Write RUN/run_timing.json: {"started": "<now, ISO 8601 local time, from `date +%Y-%m-%dT%H:%M:%S`>", "coordinator_model": "<your model>", "tester_model": "<the website-tester model and effort>", "batches": [], "refused": [<one {"tc": "<TC ID>", "step": <step number>, "reason": "<why>"} for every case the safety check in Step 1 did not run>]}. The reports use it to show the full run time split into coordinator and website-tester time; the eval script uses "refused".

## Step 3: Run the tests
Order the tests: first [LOGGED OUT], then [LOGGED IN] with Changes account = No, then [LOGGED IN] with Changes account = Yes. This way a claim or a spend does not change what the look-only tests see.
Split the tests into batches of 5, keeping that order. For each batch, start one **website-tester** agent (Agent tool, subagent_type "website-tester"; its rules are in .claude/agents/website-tester.md). Run the batches one after another, never at the same time.
Give each agent: the test cases of its batch (TC ID, Title, Area, Priority, Platform, Start URL, Steps, Expected answers, Changes account), the RUN path, the PROJECT path, the EVIDENCE SCRIPT path, the RECORDER SCRIPT path (PROJECT/.claude/scripts/browser_recorder.py), the settings.md sections listed in Step 1 (paste them as text), and the placeholder values from SITE/settings.local.md (for example "{TEST_USER_ID} = <id>"). Pass the test cases with their placeholders as they are.
The agent replies with one line per test: TC ID | status | duration | short reason.
After each batch, check that RUN/results/<TC ID>.json, the screenshots, the replay video (or, if it says "mp4 skipped", the replay GIF) and the trace zip exist for every test in it (the screen recording <TC ID>_screen.mp4 is expected too, unless the agent said recording was not available or "screen video skipped"; a missing one is noted in Step 5, not a reason to re-run). Also check that no recorder Chrome is left open: `pgrep -f webtest-chrome-` should print nothing; if it does, run `python3 "<PROJECT>/.claude/scripts/browser_recorder.py" stop "<RUN>" "<TC ID>"` for each test of the batch, and add the batch to "batches" in RUN/run_timing.json: {"batch": <n>, "tests": [<TC IDs>], "agent_sec": <agent duration in seconds>, "tokens": <agent tokens>, "tool_calls": <agent tool uses>}, taken from the usage the agent run reports when it finishes.
If a test comes back BLOCKED or needs confirmation, do not re-run it or work around it: keep it as it is and list it in Step 5.
A SKIPPED test (its precondition was not met, for example the reward was already claimed) is not re-run either.
If the website-tester agent is not available, use a general-purpose agent and paste the whole content of .claude/agents/website-tester.md into its prompt.

## Step 4: Make the reports
Set "finished" in RUN/run_timing.json to the current time (`date +%Y-%m-%dT%H:%M:%S`).
First take the real test-account values out of the results: python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE absolute path>" "<RUN>/results"
Work out what the website-tester agents cost: python3 "<PROJECT>/.claude/scripts/run_cost.py" "<RUN>". It finds the agent transcripts that name RUN, prices them per model and writes "cost" into RUN/run_timing.json; the reports show it. If it finds no transcripts, say so and continue.
Run: python3 "<PROJECT>/.claude/scripts/build_run_report.py" "<RUN>" "<SITE absolute path>" "<site name>"
It creates from RUN/results/*.json:
1. RUN/report.html (layout from .claude/scripts/report_html.py): an Overview with totals, the pass rate by category (Functional / Non-functional, from the Test category column of testcases.xlsx), mode and priority, a "Needs attention" table of tests that did not pass, the changes to the test account and a table of all tests; a sidebar with search and status, mode, priority and category filters; then one page per test that starts with what went wrong (the failed step, expected and actual answer, and its screenshot), then account changes, links to its evidence folder, steps PDF and trace zip, the screen recording (when there is one), the replay video of the step screenshots (the GIF for older runs), and every step with expected answer, answer, what was seen and a screenshot. Failed steps are shown in red. A note explains the screen recording, the replay video and the trace zip.
2. RUN/results.xlsx: sheets "Summary", "Results" and "Steps".
3. RUN/results.csv: the Results sheet as UTF-8 with BOM.
It also fills "Last result" and "Last run" in SITE/testcases.xlsx. Then run python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE absolute path>" --check; it must say "found 0 in total". If it prints TESTCASES_OPEN, the file is open in Excel: ask me to close it, then run the script again.

## Step 5: Tell me the results
Show: totals, and the same totals split into LOGGED OUT and LOGGED IN, total time, the failed tests with reasons (and the path to each failed test's stepNN_FAIL.png), and which failures look like real bugs versus test-wording problems.
List the SKIPPED tests with when they can run again (if the page showed it), and everything the run changed on the test account (from each result's account_changes).
End with the command to open the report: open "RUN/report.html" (with the real path).
Tell me I can combine all runs into one report with /gather-results <site name>.
