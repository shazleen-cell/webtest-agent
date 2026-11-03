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
4. You can now run LOGGED OUT tests. For LOGGED IN tests, get the test-account values from a teammate in a private message (never through git or a shared channel), and save them as `website-tests/<site>/settings.local.md`. For a site that logs in with a link:
   ```
   - TEST_USER_ID: <id>
   ```
   and for a site with a login form:
   ```
   - TEST_USERNAME: <username>
   - TEST_PASSWORD: <password>
   ```
   Without this file, LOGGED OUT tests still run, but LOGGED IN tests stop and ask for the val

Test results are not in git, so a fresh clone has no `runs/` folder. `/gather-results` only wo least one run yourself.

## Quick start

Open Claude Code in this folder and run:

| Step | Command | What it does |
|---|---|---|
| 1 | `/website-test <url> <site name>` | Explores the site, creates `settings.md` and `site-mses to `website-tests/<site>/testcases.xlsx`. Then it stops so you can review them. |
| 2 | Type `proceed`, or mark *Approved* = Yes in the Excel file | Approves the test cases. `proceed` approves all new test cases and runs them straight away. |
| 3 | `/run-tests <site name>` | Runs the approved tests and makes `report.html`, `results.xlshat run. |
| 4 | `/gather-results <site name>` | Combines all runs into one `Results/` folder with the newest result of every test. |

The site name is any short name you choose. It becomes the folder `website-tests/<site name>/`.

To check the agent itself after a change to its model, effort, prompts or rules, run `/evaluate-agent` (see [Evaluating the agent](#evaluating-the-agent)).

Example:
```
/test-website https://site.ludus-game.com/ ludus
/run-tests ludus
/gather-results ludus
```

At the end of each command, Claude gives you the command to open the report, for example `open/<date_time>/report.html"`.

`/run-tests` can also run only some of the tests:
```
/run-tests ludus High            # one priority: High, Medium or Low
/run-tests ludus LoggedOut       # LOGGED OUT tests only
/run-tests ludus LoggedIn        # LOGGED IN tests only
/run-tests ludus Changes         # only tests that change the test account
/run-tests ludus TC-001,TC-005   # specific tests
```

Before running, `/run-tests` checks every step against the safety rules. A test with a step that is not allowed is not run, and you are told which step it was.

## How it works

There are two roles:

1. **The main Claude Code session (coordinator).** It follows the slash commands in `.claude/commands/`. It explores the site, writes the test cases, splits the approved tests into batches of 5 and builds the
reports.
2. **The `website-tester` agent (worker),** defined in `.claude/agents/website-tester.md`. It runs on Sonnet (`model: sonnet` in that file), while the coordinator uses the model of your Claude Code session. One
agent is started for each batch, and the batches run one after another. It follows each test'sreenshot after every step, and writes a result JSON plus evidence: a replay GIF, a steps PDFand a browser trace zip.

The opt-in rules are in `.claude/rules/opt-in.md`. The Python scripts in `.claude/scripts/` build the evidence and reports:

| Script | Used by | What it does |
|---|---|---|
| `test_evidence.py` | website-tester | Marks failed screenshots, and makes the replay GIF and steps PDF |
| `build_run_report.py` | `/run-tests` | Makes the report for one run and writes the latest relsx` |
| `gather_results.py` | `/gather-results` | Combines all runs into `Results/` |
| `report_html.py` | both report scripts | The shared HTML report layout |
| `scrub_secrets.py` | all three commands | Replaces real test-account values with their placeholders |
| `eval_score.py` | you, when checking the agent itself | Scores a run against known results (s runs |
| `eval_report_html.py` | `eval_score.py` | The eval report and comparison pages |

Each run folder also has `run_timing.json` (start and end time, and the time, tokens and tool calls of every website-tester batch). The reports use it to show the **full run time**, split into **coordinator** time
(batching, checks, building reports) and **website-tester** time, next to the **test step timests themselves) and the tokens used.

## Folder layout

```
website-tests/<site>/
  settings.md          site rules: cookie banner, login, what may be clicked
  settings.local.md    test-account values (not in git)
  site-map.md          pages and facts found while exploring (F- and P- numbers)
  testcases.xlsx       test cases; the Approved column decides what runs
  explore/             screenshots taken while exploring (not in git)
  runs/                (not in git)
    <date_time>/       one folder per run: report.html, results.xlsx, results.csv, run_timing.
    Results/           newest result of every test from all runs (results.html, results.xlsx, README.md, json/)
```

## settings.md

Each site has its own `website-tests/<site>/settings.md`. `/test-website` creates it on the fiou run the tests. It contains:

- **Cookie banner**: the banner title and the button to click
- **Facts seen before**: facts found while exploring, used as hints next time
- **Login (LOGGED IN mode)**: the login method, how to tell the user is logged in, and any popED IN tests are only written and run when this section exists.
- **Allowed when LOGGED IN / Allowed when LOGGED OUT**: what tests may click
- **Never**: what must never be clicked
- **Skip**: content that changes all the time and should not be tested
- **Allowed to type / Allowed cart actions / Allowed demo checkout**: the opt-in sections, OFFules](#opt-in-rules))

### Login and test-account values

There are two login methods:

- **Login link**: a part added to the page URL, for example `?user-id={TEST_USER_ID}`.
- **Login form**: a username and password typed into the site's login form as `{TEST_USERNAME}` and `{TEST_PASSWORD}`. This needs the **Allowed to type** opt-in switched ON for exactly those fields.

Test-account values work like passwords (on some sites anyone with the login link is logged in), so they are not stored in git. settings.md, site-map.md, testcases.xlsx and the reports use placeholders such as
`{TEST_USER_ID}`. The real values go in `website-tests/<site>/settings.local.md`, which git ig

The commands put the real value in only while the browser runs, and `.claude/scripts/scrub_secthe placeholder in the results. `python3 .claude/scripts/scrub_secrets.py website-tests/<site>--check` lists any real value left in the tracked files.

### Opt-in rules

By default the agent never types, never changes a cart and never checks out. A site can loosen this only through three opt-in sections in its `settings.md`:

| Section | What it allows | Where |
|---|---|---|
| **Allowed to type** | Typing the listed values (placeholders or fake values) into the listed fields, for example a login form | Any site, with approval |
| **Allowed cart actions** | Clicking the listed cart buttons, for example "Add to cart" and "es that take no real payments |
| **Allowed demo checkout** | A fake checkout with fake values | Demo sites only, and only with cart actions ON |

Each section has a `status` (OFF unless someone switches it to ON), who approved it, and the exact fields, values and buttons it allows. A real payment window and real payment or personal details are never allowed
by any section, and live shops keep all three OFF. The full rules and templates are in `.claud

## Test cases

Every test case in `testcases.xlsx` has:

- a title starting with `[LOGGED OUT]` or `[LOGGED IN]`
- an area, a priority (High / Medium / Low), and a platform (Desktop / Mobile / Tablet)
- a category (Functional / Non-functional) and a sub-type
- numbered steps. Action steps end with a full stop, checks are Yes/No questions, and the expected answers are listed by step number (for example `#3 Yes, #5 Yes`).
- *Changes account* = Yes when the test claims a reward or spends points. These tests check a  reward was already claimed or is on cooldown, the result is SKIPPED instead of FAILED.
- *Last result* and *Last run*, filled in after each run

Only rows with *Approved* = Yes are run. You can edit, add or remove test cases in Excel. When you run `/test-website` again, it keeps your rows and your Approved values and only adds new test cases.

## Results

| Status | Meaning |
|---|---|
| PASSED | Every check gave the expected answer |
| FAILED | A check gave the wrong answer, or a step could not be done |
| BLOCKED | The next step would break a safety rule, or the test user was not logged in |
| SKIPPED | The precondition was not met (for example, the reward was already claimed). This i
| UNSURE | The tester could not tell the answer from the page |

`report.html` and `results.html` open with an overview: totals, pass rate by category, mode and priority, the tests that need attention, and the changes made to the test account. Each test has its own page, which
starts with what went wrong: the failed step, the expected and actual answer, and the screensh

A FAILED test is not always a bug on the site. Sometimes the test's wording or expected answerscreenshot of the failed step before reporting a bug.

wdio-mcp cannot record video. Each test has a replay GIF of its step screenshots instead, plusat https://trace.playwright.dev.

## Safety rules

The tester always follows these rules:

- No payment and no purchase: no real-money prices, Buy, Pay or Checkout, and never the final s to payment. If a real payment window opens (for Xsolla sites: Pay Station), it closes it,takes a screenshot and marks the test FAILED.
- It never types into fields and never changes a cart, unless an opt-in section allows exactlynever enters real personal data or payment details.
- It only opens pages on the same website: no external links, no downloads.
- Claiming and spending points happen only when `settings.md` allows them, and only in tests m
- While exploring, it only looks: no claims, no spending, no cart changes.
- If a step needs something that is not clearly allowed, the test is BLOCKED. The tester does
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
/evaluate-agent            # run the eval set, score it, compare with earlier runs
/evaluate-agent score      # score the newest run again (no browser)
/evaluate-agent compare    # compare all runs and find flaky cases (no browser)
```

`/evaluate-agent` runs the cases the same way as `/run-tests`, then scores them with `.claude/scripts/eval_score.py`. You can also run the script yourself: `python3 .claude/scripts/eval_score.py website-tests/demoblaze-eval [--all]`.

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

Test evidence is large (about 1 GB per run), so `.gitignore` keeps it out of git. Git keeps th, `settings.md`, `site-map.md` and `testcases.xlsx`. The `explore/` screenshots, all test runsand results (`runs/`, including `runs/Results/`) and the browser trace zips (`.trace/`) stay on this computer only, and `settings.local.md` (the test-account values) is never in git. To share the full report with screenshots, zip the `runs/Results/` folder. Browser traces can contain typed values such as ahe zip only with the team.

Git also keeps `.mcp.json`, which sets up the wdio-mcp browser tool for everyone who clones thde settings (`.claude/settings.local.json`) stay out of git.
