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
Read SITE/settings.md: the "Login (LOGGED IN mode)" section, "Allowed when LOGGED IN", "Allowed when LOGGED OUT" and "Never". The website-tester agent needs these.
Check that Pillow is installed (python3 -c "import PIL"). If it is missing, run: pip3 install --user pillow
Safety check before running: read the Steps of every approved case. If any action step clicks or presses something that pays or purchases (a button with a real-money price, Buy, Purchase, Pay, Checkout, Add to cart, the final button of the gift flow) or anything in the "Never" list of settings.md, do NOT run that case. List it for me with the TC ID and the step, and run the rest. Claim, spending loyalty points and Logout are allowed if settings.md allows them.

## Step 2: Make the run folder
RUN = SITE/runs/<YYYY-MM-DD_HHMM>/ (absolute path) with a subfolder results/ and one evidence folder per test: RUN/<TC ID>/ (for example RUN/TC-001/).

## Step 3: Run the tests
Order the tests: first [LOGGED OUT], then [LOGGED IN] with Changes account = No, then [LOGGED IN] with Changes account = Yes. This way a claim or a spend does not change what the look-only tests see.
Split the tests into batches of 5, keeping that order. For each batch, start one **website-tester** agent (Agent tool, subagent_type "website-tester"; its rules are in .claude/agents/website-tester.md). Run the batches one after another, never at the same time.
Give each agent: the test cases of its batch (TC ID, Title, Area, Priority, Platform, Start URL, Steps, Expected answers, Changes account), the RUN path, the PROJECT path, the EVIDENCE SCRIPT path, and the settings.md sections listed in Step 1 (paste them as text).
The agent replies with one line per test: TC ID | status | duration | short reason.
After each batch, check that RUN/results/<TC ID>.json, the screenshots, the replay GIF and the trace zip exist for every test in it.
If a test comes back BLOCKED or needs confirmation, do not re-run it or work around it: keep it as it is and list it in Step 5.
A SKIPPED test (its precondition was not met, for example the reward was already claimed) is not re-run either.
If the website-tester agent is not available, use a general-purpose agent and paste the whole content of .claude/agents/website-tester.md into its prompt.

## Step 4: Make the reports
Run: python3 "<PROJECT>/.claude/scripts/build_run_report.py" "<RUN>" "<SITE absolute path>" "<site name>"
It creates from RUN/results/*.json:
1. RUN/report.html: site, date, totals (passed, failed, blocked, skipped, unsure), total time and a note that real video is not available; a summary table (each TC ID links to its section) with a LOGGED OUT / LOGGED IN filter; then per test: what it changed on the test account, links to its evidence folder, steps PDF and trace zip, the replay GIF, and a step table with expected answer, answer, what was seen and a screenshot. Failed steps are shown in red.
2. RUN/results.xlsx: sheets "Summary", "Results" and "Steps".
3. RUN/results.csv: the Results sheet as UTF-8 with BOM.
It also fills "Last result" and "Last run" in SITE/testcases.xlsx. If it prints TESTCASES_OPEN, the file is open in Excel: ask me to close it, then run the script again.

## Step 5: Tell me the results
Show: totals, and the same totals split into LOGGED OUT and LOGGED IN, total time, the failed tests with reasons (and the path to each failed test's stepNN_FAIL.png), and which failures look like real bugs versus test-wording problems.
List the SKIPPED tests with when they can run again (if the page showed it), and everything the run changed on the test account (from each result's account_changes).
End with the command to open the report: open "RUN/report.html" (with the real path).
Tell me I can combine all runs into one report with /gather-results <site name>.
