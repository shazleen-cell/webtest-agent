# webtest-agent

Automated website testing with Claude Code. It explores a website, writes test cases for you to review, runs them in a real Chrome browser, and builds HTML and Excel reports with a screenshot of every step.

It was built for game web shops (first site: [LUDUS](https://site.ludus-game.com/)) and tests in two modes:

- **LOGGED OUT**: as a visitor who is not logged in.
- **LOGGED IN**: as an approved test user. These tests can claim free rewards and spend loyalty points when the site's settings allow it.

**It never pays or purchases anything.** By default it also never types into fields and never changes a cart (see [Safety rules](#safety-rules)).

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Google Chrome
- [Node.js](https://nodejs.org/) 18 or newer (for `npx`, which starts the browser tool)
- Python 3 with `openpyxl` and `pillow`:
  ```
  pip3 install --user openpyxl pillow
  ```

The browser tool, the **wdio-mcp** MCP server (`@wdio/mcp`), is set up by `.mcp.json` in this repo. You don't install it yourself.

## Setting up on a new computer

1. Install the requirements above.
2. Clone the repo and open Claude Code in it:
   ```
   git clone https://github.com/shazleen-cell/webtest-agent.git
   cd webtest-agent
   claude
   ```
3. Claude Code asks whether to use the **wdio-mcp** server from `.mcp.json`. Approve it. Type `/mcp` to check that it shows as connected. The first start can take a minute while `npx` downloads it. If it is not connected, quit Claude Code and open it again.
4. You can now run LOGGED OUT tests. For LOGGED IN tests, get the test-account values from a teammate in a private message (never through git or a shared channel).
   - **Site that logs in with a link (for example Ludus):** you don't create any file. Run `/test-website <url> <site name> userid=<test user ID>` and Claude saves the ID in `website-tests/<site>/settings.local.md` for you (git ignores that file), adds the login section to `settings.md`, and checks that the login works. Next time you can leave `userid=` out: the saved ID is used.
   - **Site with a login form:** save the values yourself as `website-tests/<site>/settings.local.md`, and switch on the **Allowed to type** opt-in for exactly those fields (see [Opt-in rules](#opt-in-rules)):
     ```
     - TEST_USERNAME: <username>
     - TEST_PASSWORD: <password>
     ```

   Without the value, LOGGED OUT tests still run, but LOGGED IN tests stop and ask for it.

A fresh clone has the summary reports (`runs/Results/results.html` and `results.xlsx`) but no evidence: screenshots, replay GIFs and traces stay on the computer that ran the tests. To build new reports, do at least one run yourself.

## Quick start

Open Claude Code in this folder and run:

| Step | Command | What it does |
|---|---|---|
| 1 | `/test-website <url> <site name>` | Explores the site, creates `settings.md` and `site-map.md`, and writes test cases to `website-tests/<site>/testcases.xlsx`. Then it stops so you can review them. This writes LOGGED OUT tests (as a visitor who is not logged in). |
| 2 | `/test-website <url> <site name> [userid=<test user ID>]` | Explores the site, creates `settings.md` and `site-map.md`, and writes test cases to `website-tests/<site>/testcases.xlsx`. Then it stops so you can review them. With `userid=` it also sets up the login for LOGGED IN tests and writes those tests too. |
| 3 | Type `proceed`, or mark *Approved* = Yes in the Excel file | Approves the test cases. `proceed` approves all new test cases and runs them straight away. |
| 4 | `/run-tests <site name>` | Runs the approved tests and makes `report.html`, `results.xlsx` and `results.csv` for that run. |
| 5 | `/gather-results <site name>` | Combines all runs into one `Results/` folder with the newest result of every test. |

The site name is any short name you choose. It becomes the folder `website-tests/<site name>/`.

`userid=` is optional. Use it only for sites that log in with an ID in the link. Without it (and without an ID already saved in `settings.local.md`), only LOGGED OUT tests are written, and Claude tells you how to turn LOGGED IN mode on.

To check the agent itself after a change to its model, effort, prompts or rules, run `/evaluate-agent` (see [Evaluating the agent](#evaluating-the-agent)).

Example:
```
/test-website https://site.ludus-game.com/ ludus userid=<test user ID>
/run-tests ludus
/gather-results ludus
```

At the end of each command, Claude gives you the command to open the report, for example `open "website-tests/ludus/runs/<date_time>/report.html"`.

`/run-tests` can also run only some of the tests:
```
/run-tests ludus High            # one priority: High, Medium or Low
/run-tests ludus LoggedOut       # LOGGED OUT tests only
/run-tests ludus LoggedIn        # LOGGED IN tests only
/run-tests ludus Changes         # only tests that change the test account
/run-tests ludus TC-001,TC-005   # specific tests
```

Before running, `/run-tests` checks every step against the safety rules. A test with a step that is not allowed is not run, and you are told which step it was.

LOGGED IN tests that claim a reward or spend points change the test account for real. A reward that was claimed stays on cooldown, and spent points are gone, so those tests are SKIPPED when you run them again before the cooldown ends.

## How it works

There are two roles:

1. **The main Claude Code session (coordinator).** It follows the slash commands in `.claude/commands/`. It explores the site, writes the test cases, splits the approved tests into batches of 5 and builds the reports.
2. **The `website-tester` agent (worker),** defined in `.claude/agents/website-tester.md`. It runs on Sonnet (`model: sonnet` in that file), while the coordinator uses the model of your Claude Code session. One agent is started for each batch, and the batches run one after another. It follows each test's steps exactly, takes a screenshot after every step, and writes a result JSON plus evidence: a replay GIF, a steps PDF and a browser trace zip.

The opt-in rules are in `.claude/rules/opt-in.md`. The Python scripts in `.claude/scripts/` build the evidence and reports:

| Script | Used by | What it does |
|---|---|---|
| `test_evidence.py` | website-tester | Marks failed screenshots, and makes the replay GIF and steps PDF |
| `build_run_report.py` | `/run-tests` | Makes the report for one run and writes the latest results back to `testcases.xlsx` |
| `gather_results.py` | `/gather-results` | Combines all runs into `Results/` |
| `report_html.py` | both report scripts | The shared HTML report layout |
| `scrub_secrets.py` | all three commands | Replaces real test-account values with their placeholders |
| `eval_score.py` | `/evaluate-agent` | Scores a run against known results (`golden.json`), writes `eval_report.html`, and compares runs |
| `eval_report_html.py` | `eval_score.py` | The eval report and comparison pages |
| `run_cost.py` | `/run-tests` | Works out what the website-tester agents of a run cost in dollars (API list prices, cache reads included) and saves it in `run_timing.json` |

Each run folder also has `run_timing.json` (start and end time, and the time, tokens and tool calls of every website-tester batch). The reports use it to show the **full run time**, split into **coordinator** time (batching, checks, building reports) and **website-tester** time, next to the **test step time** (the time inside the tests themselves) and the tokens used.

## Folder layout

```
website-tests/<site>/
  settings.md          site rules: cookie banner, login, what may be clicked
  settings.local.md    test-account values (not in git)
  site-map.md          pages and facts found while exploring (F- and P- numbers)
  testcases.xlsx       test cases; the Approved column decides what runs
  explore/             screenshots taken while exploring (not in git)
  runs/                evidence not in git; summary reports are
    <date_time>/       one folder per run: report.html, results.xlsx, results.csv, run_timing.json, evidence (not in git)
    Results/           newest result of every test from all runs: results.html, results.xlsx, README.md, json/ (in git); evidence folders (not in git)
```

## settings.md

Each site has its own `website-tests/<site>/settings.md`. `/test-website` creates it on the first run, and you can edit it before you run the tests. It contains:

- **Cookie banner**: the banner title and the button to click
- **Facts seen before**: facts found while exploring, used as hints next time
- **Login (LOGGED IN mode)**: the login method, how to tell the user is logged in, and any popup shown after login. LOGGED IN tests are only written and run when this section exists. For a login-link site, `/test-website ... userid=<id>` adds it for you and fills in the login check and popup after exploring.
- **Allowed when LOGGED IN / Allowed when LOGGED OUT**: what tests may click. When `/test-website` adds the LOGGED IN list itself, it allows logging in, normal navigation, Logout, free "Claim" buttons and spending in-game points or currency. It does not allow the gift flow, any button with a real-money price, or anything that opens a payment window. An existing list is never overwritten.
- **Never**: what must never be clicked
- **Skip**: content that changes all the time and should not be tested
- **Allowed to type / Allowed cart actions / Allowed demo checkout**: the opt-in sections, OFF by default (see [Opt-in rules](#opt-in-rules))

### Login and test-account values

There are two login methods:

- **Login link**: a part added to the page URL, for example `?user-id={TEST_USER_ID}`. Set it up with `userid=<id>` on `/test-website` (see [Quick start](#quick-start)).
- **Login form**: a username and password typed into the site's login form as `{TEST_USERNAME}` and `{TEST_PASSWORD}`. This needs the **Allowed to type** opt-in switched ON for exactly those fields.

Test-account values work like passwords (on some sites anyone with the login link is logged in), so they are not stored in git. settings.md, site-map.md, testcases.xlsx and the reports use placeholders such as `{TEST_USER_ID}`. The real values go in `website-tests/<site>/settings.local.md`, which git ignores.

The commands put the real value in only while the browser runs, and `.claude/scripts/scrub_secrets.py` replaces it with the placeholder in the results. `python3 .claude/scripts/scrub_secrets.py website-tests/<site> --check` lists any real value left in the tracked files.

### Opt-in rules

By default the agent never types, never changes a cart and never checks out. A site can loosen this only through three opt-in sections in its `settings.md`:

| Section | What it allows | Where |
|---|---|---|
| **Allowed to type** | Typing the listed values (placeholders or fake values) into the listed fields, for example a login form | Any site, with approval |
| **Allowed cart actions** | Clicking the listed cart buttons, for example "Add to cart" and "Delete" | Demo or test sites that take no real payments |
| **Allowed demo checkout** | A fake checkout with fake values | Demo sites only, and only with cart actions ON |

Each section has a `status` (OFF unless someone switches it to ON), who approved it, and the exact fields, values and buttons it allows. A real payment window and real payment or personal details are never allowed by any section, and live shops keep all three OFF. The full rules and templates are in `.claude/rules/opt-in.md`.

## Test cases

Every test case in `testcases.xlsx` has:

- a title starting with `[LOGGED OUT]` or `[LOGGED IN]`
- an area, a priority (High / Medium / Low), and a platform (Desktop / Mobile / Tablet)
- a category (Functional / Non-functional) and a sub-type
- numbered steps. Action steps end with a full stop, checks are Yes/No questions, and the expected answers are listed by step number (for example `#3 Yes, #5 Yes`).
- *Changes account* = Yes when the test claims a reward or spends points. These tests check a precondition first. If the reward was already claimed or is on cooldown, the result is SKIPPED instead of FAILED.
- *Last result* and *Last run*, filled in after each run

Only rows with *Approved* = Yes are run. You can edit, add or remove test cases in Excel. When you run `/test-website` again, it keeps your rows and your Approved values and only adds new test cases.

## Results

| Status | Meaning |
|---|---|
| PASSED | Every check gave the expected answer |
| FAILED | A check gave the wrong answer, a step could not be done, or an allowed click led to a payment window |
| BLOCKED | The next step would break a safety rule, or the test user was not logged in |
| SKIPPED | The precondition was not met (for example, the reward was already claimed). This is not a bug; run the test again later. |
| UNSURE | The tester could not tell the answer from the page |

`report.html` and `results.html` open with an overview: totals, pass rate by category, mode and priority, the tests that need attention, and the changes made to the test account. Each test has its own page, which starts with what went wrong: the failed step, the expected and actual answer, and the screenshot.

A FAILED test is not always a bug on the site. Sometimes the test's wording or expected answer is wrong, so check the screenshot of the failed step before reporting a bug.

wdio-mcp cannot record video. Each test has a replay GIF of its step screenshots instead, plus a trace zip you can open at https://trace.playwright.dev.

## Safety rules

The tester always follows these rules:

- No payment and no purchase: no real-money prices, Buy, Pay or Checkout, and never the final button of a flow that leads to payment. If a real payment window opens (for Xsolla sites: Pay Station), it closes it, takes a screenshot and marks the test FAILED.
- If a click that the test and `settings.md` allow (a free "Claim" button, or a button priced only in in-game points or currency) opens a payment window or asks for real money, the tester clicks nothing in it, closes it, takes a screenshot, stops the test and marks it FAILED (not BLOCKED, not SKIPPED).
- It never types into fields and never changes a cart, unless an opt-in section allows exactly that field, value or button. It never enters real personal data or payment details.
- It only opens pages on the same website: no external links, no downloads.
- Claiming free rewards and spending in-game points or currency happen only when `settings.md` allows them, and only in tests marked *Changes account*. A confirm button of a purchase that costs only in-game points may be clicked even if it says "Buy" or "Purchase", when the step says to and `settings.md` allows it. Real money is never spent. The gift flow is never done.
- While exploring, it only looks: no claims, no spending, no cart changes, no logout.
- If a step needs something that is not clearly allowed, the test is BLOCKED. The tester does not work around it.

## Evaluating the agent

`website-tests/demoblaze-eval/` tests the agent itself. It has 22 cases on demoblaze where the right result is already known:
- tests that pass
- real bugs
- tests whose expected answer is wrong on purpose (the agent must not just agree)
- safety traps that must be refused or BLOCKED

Run it after changing the model, the effort, `website-tester.md`, the commands or the rules:

```
/evaluate-agent            # run the eval set, score it, compare with earlier runs
/evaluate-agent score      # score the newest run again (no browser)
/evaluate-agent compare    # compare all runs and find flaky cases (no browser)
/evaluate-agent safety     # send only the 4 safety traps straight to the website-tester
```

In a normal run, the coordinator's safety check refuses the 4 safety traps before the browser opens, so the website-tester's own rules are never tested. `/evaluate-agent safety` skips that check for those 4 cases only, on the eval site only, with no real test-account values, and asks you first. Each trap must come back BLOCKED by the website-tester. `/run-tests` never skips the check.

`/evaluate-agent` runs the cases the same way as `/run-tests`, then scores them with `.claude/scripts/eval_score.py`. You can also run the script yourself: `python3 .claude/scripts/eval_score.py website-tests/demoblaze-eval [--all]`.

The scorecard shows:
- safety violations
- false PASSED (bugs the agent missed)
- false FAILED
- status and answer accuracy
- evidence completeness
- leaked test-account values
- time and tokens
- website-tester cost in dollars

Each scored run gets an `eval_report.html`, and `--all` also writes `runs/eval_comparison.html`. Details are in `website-tests/demoblaze-eval/README.md`.

## Git

Git keeps the commands, agent, rules and scripts in `.claude/`, `.mcp.json` (sets up the wdio-mcp browser tool for everyone who clones the repo), and for each site `settings.md`, `site-map.md` and `testcases.xlsx`.

Test evidence is large (about 1 GB per run), so `.gitignore` keeps it out of git. Only the small summary reports go to git (about 1–2 MB per site), so QA can read the results in a fresh clone:

| In git (summary reports) | Not in git (stays on this computer) |
|---|---|
| `runs/Results/results.html`, `results.xlsx`, `README.md`, `json/` | Screenshots, replay GIFs, steps PDFs and trace zips |
| `runs/<run>/eval_report.html`, `eval_score.md`, `eval_score.json` | The run folders themselves (`runs/<date_time>/report.html` and evidence) |
| `runs/eval_comparison.html` | `explore/` screenshots, `.trace/`, `settings.local.md`, `.claude/settings.local.json` |

In a clone, `results.html` shows every status, failed step, expected and actual answer and reason, but its screenshot and replay links only work on a computer that has the evidence. To share the full report with screenshots, zip the `runs/Results/` folder. Browser traces can contain typed values such as the demo password, so share the zip only with the team.

Before committing reports, run `python3 .claude/scripts/scrub_secrets.py website-tests/<site> --check`. It must say "found 0 in total".
