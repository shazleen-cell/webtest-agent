# webtest-agent

Automated website testing with Claude Code. It explores a website, writes test cases for you to review, runs them in a real Chrome browser, and builds HTML and Excel reports with a screenshot of every step.

It was built for game web shops (first site: [LUDUS](https://site.ludus-game.com/)) and tests in two modes:

- **LOGGED OUT**: as a visitor who is not logged in.
- **LOGGED IN**: as an approved test user. These tests can claim free rewards and spend loyalty points when the site's settings allow it.

**It never pays or purchases anything.**

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
3. Claude Code asks whether to use the **wdio-mcp** server from `.mcp.json`. Approve it. Type `/mcp` to check that it shows as connected. The first start can take a minute while `npx` downloads it.
4. Get the test-account values from a teammate in a private message (never through git or a shared channel), and save them as `website-tests/<site>/settings.local.md`. For example, for Ludus:
   ```
   - TEST_USER_ID: <id>
   ```
   and for demoblaze:
   ```
   - TEST_USERNAME: <demo username>
   - TEST_PASSWORD: <demo password>
   ```
   Without this file, LOGGED OUT tests still run, but LOGGED IN tests stop and ask for the value.
5. Run the tests, for example `/run-tests ludus`. The report is written to `website-tests/ludus/runs/<date_time>/report.html`.

Test results are not in git, so a fresh clone has no `runs/` folder. `/gather-results` only works after you have done at least one run yourself.

## Quick start

Open Claude Code in this folder and run:

| Step | Command | What it does |
|---|---|---|
| 1 | `/test-website <url> <site name>` | Explores the site and writes test cases to `website-tests/<site>/testcases.xlsx`, then stops so you can review them. |
| 2 | Type `proceed`, or mark *Approved* = Yes in the Excel file | Approves the test cases. |
| 3 | `/run-tests <site name>` | Runs the approved tests and makes `report.html`, `results.xlsx` and `results.csv` for that run. |
| 4 | `/gather-results <site name>` | Combines all runs into one `Results/` folder with the newest result of every test. |

Example:
```
/test-website https://site.ludus-game.com/ ludus
/run-tests ludus
/gather-results ludus
```

`/run-tests` can also run only some of the tests:
```
/run-tests ludus High            # High priority only
/run-tests ludus LoggedOut       # LOGGED OUT tests only
/run-tests ludus LoggedIn        # LOGGED IN tests only
/run-tests ludus Changes         # only tests that change the test account
/run-tests ludus TC-001,TC-005   # specific tests
```

## How it works

There are two roles:

1. **The main Claude Code session (coordinator).** It follows the slash commands in `.claude/commands/`. It explores the site, writes the test cases, splits the approved tests into batches of 5 and builds the reports.
2. **The `website-tester` agent (worker),** defined in `.claude/agents/website-tester.md`. It runs on Sonnet (`model: sonnet` in that file), while the coordinator uses the model of your Claude Code session (Opus). One agent is started for each batch, and the batches run one after another. It follows each test's steps exactly, takes a screenshot after every step, and writes a result JSON plus evidence: a replay GIF, a steps PDF and a browser trace zip.

The Python scripts in `.claude/scripts/` build the evidence and reports:

| Script | Used by | What it does |
|---|---|---|
| `test_evidence.py` | website-tester | Marks failed screenshots, and makes the replay GIF and steps PDF |
| `build_run_report.py` | `/run-tests` | Makes the report for one run and writes the latest results back to `testcases.xlsx` |
| `gather_results.py` | `/gather-results` | Combines all runs into `Results/` |
| `eval_score.py` | you, after `/run-tests demoblaze-eval` | Scores a run against `golden.json`, writes `eval_report.html`, and compares runs (`eval_comparison.html`) |
| `report_html.py` | both report scripts | The shared HTML report layout |
| `eval_report_html.py` | `eval_score.py` | The eval report and comparison pages |

Each run folder also has `run_timing.json` (start and end time, and the time, tokens and tool calls of every website-tester batch). The reports use it to show the **full run time**, split into **coordinator** time (batching, checks, building reports) and **website-tester** time, next to the **test step time** (the time inside the tests themselves) and the tokens used.

## Folder layout

```
website-tests/<site>/
  settings.md          site rules: cookie banner, login, what may be clicked
  settings.local.md    test-account values such as the test user ID (not in git)
  site-map.md          pages and facts found while exploring (F-, P-, N- numbers)
  testcases.xlsx       test cases; the Approved column decides what runs
  explore/             screenshots taken while exploring
  runs/
    <date_time>/       one folder per run: report.html, results.xlsx, results.csv, evidence
    Results/           newest result of every test from all runs (results.html, results.xlsx, json/)
```

## settings.md

Each site has its own `website-tests/<site>/settings.md`. `/test-website` creates it on the first run. It contains:

- **Cookie banner**: the banner title and the button to click
- **Login (LOGGED IN mode)**: the login method (for example `?user-id={TEST_USER_ID}` added to the URL), the test user, how to tell the user is logged in, and any popup shown after login. LOGGED IN tests are only written and run when this section exists.

The test user ID works like a password on some sites (anyone with the link is logged in), so it is not stored in git. settings.md, site-map.md, testcases.xlsx and the reports use the placeholder `{TEST_USER_ID}`. The real value goes in `website-tests/<site>/settings.local.md`, which git ignores:

```
- TEST_USER_ID: <id>
```

The commands put the real value in only while the browser runs, and `.claude/scripts/scrub_secrets.py` replaces it with the placeholder in the results. `python3 .claude/scripts/scrub_secrets.py website-tests/<site> --check` lists any real value left in the tracked files.
- **Allowed when LOGGED IN / Allowed when LOGGED OUT**: what tests may click
- **Never**: what must never be clicked
- **Skip**: content that changes all the time and should not be tested

### Opt-in rules

By default the agent never types, never changes a cart and never checks out. A site can loosen this only through three opt-in sections in its `settings.md`: **Allowed to type**, **Allowed cart actions** (demo or test sites only) and **Allowed demo checkout** (demo sites only, no real payment). Each section has a `status` (OFF unless someone switches it to ON), who approved it, and the exact fields, values and buttons it allows. The full rules and templates are in `.claude/rules/opt-in.md`. Logins and passwords for "Allowed to type" go in `settings.local.md` as `{TEST_USERNAME}` and `{TEST_PASSWORD}`, like the test user ID.

## Test cases

Every test case in `testcases.xlsx` has:

- a title starting with `[LOGGED OUT]` or `[LOGGED IN]`
- an area, a priority (High / Medium / Low), and a platform (Desktop / Mobile / Tablet)
- a category (Functional / Non-functional) and a sub-type
- numbered steps. Checks are Yes/No questions, and the expected answers are listed by step number.
- *Changes account* = Yes when the test claims a reward or spends points. These tests check a precondition first. If the reward was already claimed or is on cooldown, the result is SKIPPED instead of FAILED.

Only rows with *Approved* = Yes are run.

## Results

| Status | Meaning |
|---|---|
| PASSED | Every check gave the expected answer |
| FAILED | A check gave the wrong answer, or a step could not be done |
| BLOCKED | The next step would break a safety rule, or the test user was not logged in |
| SKIPPED | The precondition was not met (for example, the reward was already claimed) |
| UNSURE | The tester could not tell the answer from the page |

`results.html` opens with an overview: totals, pass rate by category, mode and priority, the tests that need attention, and the changes made to the test account. Each test has its own page, which starts with what went wrong: the failed step, the expected and actual answer, and the screenshot.

wdio-mcp cannot record video. Each test has a replay GIF of its step screenshots instead, plus a trace zip you can open at https://trace.playwright.dev.

## Safety rules

The tester always follows these rules:

- No payment and no purchase: no real-money prices, Buy, Pay, Checkout or Add to cart, and never the final button of a flow that leads to payment.
- It never types into fields, and never enters credentials, personal data or payment details.
- It only opens pages on the same website: no external links, no downloads.
- Claiming and spending points happen only when `settings.md` allows them, and only in tests marked *Changes account*.
- If a step needs something that is not clearly allowed, the test is BLOCKED. The tester does not work around it.

## Evaluating the agent

`website-tests/demoblaze-eval/` tests the agent itself. It has 22 cases on demoblaze where the right result is already known:
- tests that pass
- real bugs
- tests whose expected answer is wrong on purpose (the agent must not just agree)
- safety traps that must be refused or BLOCKED

Run it after changing the model, the effort, `website-tester.md`, the commands or the rules:

```
/run-tests demoblaze-eval
python3 .claude/scripts/eval_score.py website-tests/demoblaze-eval          # newest run
python3 .claude/scripts/eval_score.py website-tests/demoblaze-eval --all    # compare all runs, find flaky cases
```

The scorecard shows:
- safety violations
- false PASSED (bugs the agent missed)
- false FAILED
- status and answer accuracy
- evidence completeness
- leaked test-account values
- time and tokens

Each scored run gets an `eval_report.html`, and `--all` also writes `runs/eval_comparison.html`. Details are in `website-tests/demoblaze-eval/README.md`.

## Git

Test evidence is large (about 1.8 GB for one site), so `.gitignore` keeps it out of git. Git keeps the scripts, commands, `settings.md`, `site-map.md` and `testcases.xlsx`. The `explore/` screenshots and all test runs and results (`runs/`, including `runs/Results/`) stay on this computer only, and `settings.local.md` (the test user ID) is never in git. To share the full report with screenshots, zip the `runs/Results/` folder. Browser traces can contain typed values such as the demo password, so share the zip only with the team.

Git also keeps `.mcp.json`, which sets up the wdio-mcp browser tool for everyone who clones the repo. Personal Claude Code settings (`.claude/settings.local.json`) stay out of git.