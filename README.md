# webtest-agent

Automated website testing with Claude Code. It explores a website, writes test cases for you to review, runs them in a real Chrome browser, and builds HTML and Excel reports with a screenshot of every step.

It was built for game web shops (first site: [LUDUS](https://site.ludus-game.com/)) and tests in two modes:

- **LOGGED OUT**: as a visitor who is not logged in.
- **LOGGED IN**: as an approved test user. These tests can claim free rewards and spend loyalty points when the site's settings allow it.

**It never pays or purchases anything.** By default it also never types into fields and never changes a cart (see [Safety rules](#safety-rules)).

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Google Chrome
- [Node.js](https://nodejs.org/) 22 or newer (for `npx`, which starts the browser tool, and for the screen recorder). With Node 18 to 21 the tests still run, but without screen recordings.
- Python 3 with `openpyxl`, `pillow` and `imageio-ffmpeg` (which brings its own ffmpeg, used for the replay videos):
  ```
  pip3 install --user openpyxl pillow imageio-ffmpeg
  ```
  If ffmpeg is already installed (for example with `brew install ffmpeg`), `imageio-ffmpeg` is not needed. Without ffmpeg the tests still run, but each test gets only a replay GIF, not a video.

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

A fresh clone has the summary reports (`runs/Results/results.html` and `results.xlsx`) but no evidence: screenshots, screen recordings, replay videos and GIFs, and traces stay on the computer that ran the tests. To build new reports, do at least one run yourself.

## Quick start

Open Claude Code in this folder and run:

| Step | Command | What it does |
|---|---|---|
| 1 | `/test-website <url> <site name>` | Explores the site, creates `settings.md` and `site-map.md`, and writes test cases to `website-tests/<site>/testcases.xlsx`. Then it stops so you can review them. This writes LOGGED OUT tests (as a visitor who is not logged in). |
| 2 | `/test-website <url> <site name> [userid=<test user ID>]` | Explores the site, creates `settings.md` and `site-map.md`, and writes test cases to `website-tests/<site>/testcases.xlsx`. Then it stops so you can review them. With `userid=` it also sets up the login for LOGGED IN tests and writes those tests too. |
| 3 | Type `proceed`, or mark *Approved* = Yes in the Excel file | Approves the test cases. `proceed` approves all new test cases and runs them straight away. |
| 4 | `/run-tests <site name>` | Runs the approved tests and makes `report.html`, `results.xlsx` and `results.csv` for that run. |
| 5 | `/gather-results <site name> [run ...]` | Combines all runs into one `Results/` folder with the newest result of every test. With run folder names (for example `2026-11-16_0915 2026-11-16_1121`) it combines only those runs into `Results_<first>_to_<last>/` and leaves `Results/` as it is. |

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
2. **The `website-tester` agent (worker),** defined in `.claude/agents/website-tester.md`. It runs on Sonnet (`model: sonnet` in that file), while the coordinator uses the model of your Claude Code session. One agent is started for each batch, and the batches run one after another. It follows each test's steps exactly, takes a screenshot after every step, and writes a result JSON plus evidence: a screen recording of the browser, a replay video (MP4) and GIF of the step screenshots, a steps PDF and a browser trace zip.

The opt-in rules are in `.claude/rules/opt-in.md`. The Python scripts in `.claude/scripts/` build the evidence and reports:

| Script | Used by | What it does |
|---|---|---|
| `test_evidence.py` | website-tester | Marks failed screenshots, and makes the replay video (MP4), replay GIF and steps PDF |
| `browser_recorder.py` + `screen_recorder.mjs` | website-tester | Opens Chrome for one test with a screen recorder, and turns the recording into `<TC ID>_screen.mp4` |
| `build_run_report.py` | `/run-tests` | Makes the report for one run and writes the latest results back to `testcases.xlsx` |
| `gather_results.py` | `/gather-results` | Combines all runs into `Results/`, or only the named runs into `Results_<first>_to_<last>/` |
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
    Results_<a>_to_<b>/ same, but only from the runs named in /gather-results
  archive/<date>-<reason>/  the old site-map.md, testcases.xlsx and runs/ when a test suite is replaced
```

When you replace a site's test suite and the TC IDs get new meanings, move the old `site-map.md`, `testcases.xlsx`, run folders and `Results/` into `archive/<date>-<reason>/`. Otherwise `/gather-results` without run names would mix old and new tests that share a TC ID. Archived runs follow the same git rules as `runs/`: only the `Results` summary files are in git.

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

Each test page in the report has up to three ways to watch the test:

- **Screen recording** (`<TC ID>_screen.mp4`): the real browser while the test ran: pages loading, scrolling, popups opening. wdio-mcp cannot record the screen itself, so `browser_recorder.py` opens Chrome with Chrome's own screencast running, and wdio-mcp attaches to that Chrome. Pauses longer than 1 second (mostly the agent thinking between steps) are shortened to 1 second. It records one browser tab, so a popup that opens a new window is not in it. It shows everything on screen, including the player name and anything typed (password fields show only dots), so like the screenshots and traces it stays on the computer that ran the tests. If Chrome or Node 22 is missing, tests run without it. For Mobile tests the recorder also turns on the phone view itself (`--phone`: iPhone 14, 390x844; `--tablet`: iPad, 768x1024) through Chrome DevTools, so phone tests are recorded too. wdio-mcp's own `emulate_device` is not used, because it places fixed elements such as cookie banners in a 1560x2656 window, off the phone screen. A Desktop test that sets a window size (for example "Set the browser window to 1280x800.") uses `--size 1280x800`: the recorder's window cannot be resized once wdio-mcp is attached, so the recorder sets the page area to that size instead, and the test is recorded like any other. A failed step has a "Watch step N in the screen recording" button that starts the video where that step began (for a failed question, at the action before it), and every step has the same button in its details. The step times come from when each step screenshot was saved, and are kept in `<TC ID>_screen.json`.
- **Replay video** (`<TC ID>_replay.mp4`): the step screenshots, 1.5 seconds per step, with the step number and PASSED or FAILED on each frame. A replay GIF with the same frames is kept for older runs and for places that cannot play video.
- **Trace zip**: open it at https://trace.playwright.dev.

## Payment checks

A new user only types `/test-website <link> <site> userid=...` and then "proceed". The normal run comes first and reports the payment cases as "Skipped (payment)". When it ends, **the payment check starts by itself**. The person's "proceed" is recorded as the approval in `settings.md` (with the git user name), together with the items and price limits taken from the payment cases. A real card stays off.

`/test-website` writes payment cases for every paid part of the shop:

| Kind | One case for | Who acts |
|---|---|---|
| Window-only (`Payment (skip)`) | **every** real-money item the logged-in test user can see: the agent opens the payment window, checks the item and price, closes it | The agent alone |
| Invalid card (`Payment (skip)`, has "A person" steps) | each kind of item (one shop section), cheapest item | A person types an INVALID card when told |
| Login prompt (`Payment login prompt (skip)`) | **every** shop section with prices, logged out: the price button must ask to log in and open no payment window | The agent alone (needs opt-in section 6) |

Sections that show prices logged out but are hidden for the logged-in test user cannot be bought by that user: the review lists them, and covering them needs a test account that sees them.

- The payment check runs the window-only and login-prompt cases first, in batches (nobody touches Chrome). Then, for each invalid-card case, **a person types the card** in the open Chrome window, only after the message "Type the card details…", and clicks "Pay" once if the window lets them. An invalid card is often refused while it is typed and "Pay" stays disabled: the person answers "Pay stayed disabled (error shown)", and the result is `rejected`, the expected result. If the window closes by itself right after "Pay", the person answers "Clicked Pay, then the window closed by itself" and says what message they saw, if any (`rejected` with that message, or `window_closed` without one). Other answers: "Clicked Pay, the window is still open", "Skip", "The window expired". Only the coordinator switches the card guard on and off.
- The person types the card in the open Chrome window and clicks "Pay" once (or answers "Skip"). The agent opens the window, checks the item and price, then waits. It never types, never clicks "Pay" and never sees the values. The first try uses a made-up INVALID card (nothing can be paid). A real card also needs `real: ALLOWED` in the site's "Allowed person-typed card check" section and a second confirmation before the window opens. Nothing is captured while the card is typed: a Claude Code hook (`.claude/scripts/card_guard.py`, registered in `.claude/settings.json`) blocks screenshots, snapshots and typing until the window is closed, and `/run-tests` tests the hook before it opens any window. **Start Claude Code in the project folder** so the hook loads (`/hooks` shows it). You have to be at the computer: the agent waits for you.
- **Spend ledger (real card).** Each tester keeps their own budget and ledger in `spend/` (git ignores it). Before the first real-card run, fill in `spend/budget.md` yourself (the first run creates it with zeros and stops until you do): `card-limit` (your bank's limit on the card), `budget` (lower than the card limit) and `per-payment-cap`. Before every real-card payment window the agent runs `spend_ledger.py check`: it refuses an item above the cap, or one that would take the open spend (paid and not yet refunded, unclear, or held by the bank) above the budget. After every real-card attempt it writes a row to `spend/ledger.csv` (opens in Excel) with date, site, run, test case, item, amount, status, order or transaction ID and refund status. For refunds:
  ```
  python3 .claude/scripts/spend_ledger.py list                          # every row, open spend, what is left
  python3 .claude/scripts/spend_ledger.py set P-0003 --refund requested  # refund asked for
  python3 .claude/scripts/spend_ledger.py set P-0003 --refund confirmed  # money back on the card: no longer counts
  python3 .claude/scripts/spend_ledger.py set P-0001 --status hold       # a declined attempt the bank still holds (--status released when it is gone)
  ```
- `/run-tests <site> payment-invalid`: the older mode where the agent types made-up INVALID values from `settings.card.local.md` (git ignores that file).
Both write `card_check` (rejected, accepted, paid, window_only, window_closed, skipped, timeout or unclear; login_prompt or window_opened for the logged-out price checks) and `card_error` (the window's exact message) to the result. These cases are not counted in the pass rate. Rules: `.claude/rules/opt-in.md`, sections 4, 5 and 6.

## Slack summary

At the end of `/run-tests`, `.claude/scripts/slack_summary.py` posts a short summary of the run to a Slack channel through an incoming webhook. It includes the totals, the pass rate by mode and category, the tests that need attention with one-line reasons (the first 10), the changes to the test account, the number of skipped payment cases, the payment check results (real-card payments count in the pass rate, like in the report; invalid-card, window-only and login-prompt checks are only counted, and a card accepted or a payment window opened while logged out is flagged "Check at once"), the run time and the website-tester cost. It never shows card details or amounts. The script builds the message from the result files, so it costs no AI tokens. `/gather-results` posts its combined report only when you ask.

The message never contains screenshots, videos, traces or links to them. Before sending, the script checks the message against the real test-account values in `settings.local.md`. If it finds one, it sends nothing.

Setup (once per computer):
1. Get the webhook URL from api.slack.com/apps > your app > Incoming Webhooks.
2. Copy `.claude/slack.local.md.example` to `.claude/slack.local.md` and replace `PASTE_WEBHOOK_URL_HERE` with the webhook URL (`cp .claude/slack.local.md.example .claude/slack.local.md`), or set the `SLACK_WEBHOOK_URL` environment variable. Git ignores the file. The URL is a secret: never paste it into chat, Jira, Slack or any other file.

Without a webhook, the script only prints the message. To try it by hand:

```
python3 .claude/scripts/slack_summary.py website-tests/ludus/runs/<RUN> website-tests/ludus ludus          # dry run, prints the message
python3 .claude/scripts/slack_summary.py website-tests/ludus/runs/<RUN> website-tests/ludus ludus --send   # posts it
```

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
| `runs/Results/results.html`, `results.xlsx`, `README.md`, `json/` | Screenshots, screen recordings, replay videos and GIFs, steps PDFs and trace zips |
| `runs/<run>/eval_report.html`, `eval_score.md`, `eval_score.json` | The run folders themselves (`runs/<date_time>/report.html` and evidence) |
| `runs/eval_comparison.html` | `explore/` screenshots, `.trace/`, `settings.local.md`, `.claude/settings.local.json` |

In a clone, `results.html` shows every status, failed step, expected and actual answer and reason, but its screenshot and replay links only work on a computer that has the evidence. To share the full report with screenshots, zip the `runs/Results/` folder. Browser traces can contain typed values such as the demo password, so share the zip only with the team.

Before committing reports, run `python3 .claude/scripts/scrub_secrets.py website-tests/<site> --check`. It must say "found 0 in total".
