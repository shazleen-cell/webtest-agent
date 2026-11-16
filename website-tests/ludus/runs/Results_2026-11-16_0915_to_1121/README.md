# Ludus test results: runs 2026-11-16_0915 and 2026-11-16_1121

This folder combines two test runs of the Ludus web shop (https://site.ludus-game.com/) into one report:

- **2026-11-16_0915**: the full run of all 84 test cases (TC-001 to TC-084), written from scratch on 2026-11-16.
- **2026-11-16_1121**: a re-run of TC-009, TC-026, TC-031 and TC-057 after their wording was fixed.

For every test the report shows the newest result, so those four tests come from the re-run and all others from the full run.

## Which file to open first

Open **results.html** in a browser. It starts with an overview (totals, pass rate per category, mode and priority, the tests that need attention, and the changes to the test account), then has one page per test.

Other files:

- **results.xlsx**: the same results as a spreadsheet, with the sheets "Summary", "Results" and "Steps".
- **json/**: the raw result of every test (one file per test).
- **TC-xxx/**: the evidence of one test (only on the computer that ran the tests, not in git).

## What is in a test folder

- **stepNN.png**: a screenshot taken after each step. A failed step also has **stepNN_FAIL.png**, marked in red.
- **TC-xxx_screen.mp4**: a screen recording of the whole test. Phone, tablet and 1280x800 tests have none, because the recorder cannot use a different screen size.
- **TC-xxx_replay.mp4** and **TC-xxx_replay.gif**: a short video made from the step screenshots.
- **TC-xxx_steps.pdf**: every step with its expected answer, actual answer and screenshot.
- **TC-xxx_trace.zip**: a browser trace (open it in the Playwright trace viewer). Share it only with the team.

## What the results mean

- **PASSED**: every check gave the expected answer.
- **FAILED**: at least one check gave a different answer. The report shows which step and why.
- **BLOCKED**: the test could not be finished (for example the page did not load).
- **SKIPPED**: a precondition was not met, so the action could not be tried (for example the reward was already claimed or on cooldown, or the Reward Chain event was not running).
- **UNSURE**: the tester could not tell whether the answer was right.

**[LOGGED OUT]** tests run without logging in. **[LOGGED IN]** tests run as the approved test user ({TEST_USER_ID}), logged in through the user-id link.

**Account changes** lists what a test changed on the test account, for example a claimed reward.

## Totals

84 tests: 71 PASSED, 13 FAILED, 0 BLOCKED, 0 SKIPPED, 0 UNSURE.
LOGGED OUT (69 tests): 56 passed, 13 failed. LOGGED IN (15 tests): 15 passed, 0 failed.

## Tests that did not pass

| TC | Test | Priority | What happened | Bug or test wording? |
|---|---|---|---|---|
| TC-025 | [LOGGED OUT] The French cookie banner button means the same as "Dismiss" | Low | The French button says "Rejeter" ("Reject") while the English one says "Dismiss". | Content bug |
| TC-045 | [LOGGED OUT] Sticky Store tab bar does not cover the "Loyalty shop" heading or highlight a wrong category | Low | The sticky tab bar highlights "Emeralds" while the Loyalty shop is shown. | Bug |
| TC-046 | [LOGGED OUT] Unknown page shows a clear error message | Medium | An unknown address shows the Home page with no "Page not found" message. | Bug |
| TC-050 | [LOGGED OUT] Phone "Add It to Home Screen" banner text has no grammar mistakes | Low | The banner says "To got a quicker access !". | Content bug |
| TC-054 | [LOGGED OUT] Phone sticky tab bar highlights the category that is on screen | Low | While Gold is on screen, the tab bar highlights "Dice of Fortune". | Bug |
| TC-055 | [LOGGED OUT] Phone "Referral program" button shows its icon and opens the panel | Low | The panel opens but covers its own button and has no visible X, so it cannot be closed. | Bug |
| TC-057 | [LOGGED OUT] Store page loads with no failed requests | Medium | Every Store load has 3 failed requests: 404 on store.xsolla.com/api/v2/project/253824/user/offer_chain/1511, 1512 and 1310. | Bug |
| TC-060 | [LOGGED OUT] Page response has the usual security headers | Medium | Strict-Transport-Security is present; Content-Security-Policy, X-Frame-Options, X-Content-Type-Options and Referrer-Policy are missing. | Security finding |
| TC-062 | [LOGGED OUT] Home links and buttons have names for screen readers | Low | 16 of 26 links on Home have no accessible name (logo, app store badges, social icons). | Accessibility |
| TC-063 | [LOGGED OUT] Store footer social icons have names for screen readers | Low | None of the 6 footer social links has a name. | Accessibility |
| TC-064 | [LOGGED OUT] Home and Store each have one h1 heading | Low | Neither Home nor Store has an h1 heading. | SEO |
| TC-065 | [LOGGED OUT] Phone users can zoom the page | Low | The viewport meta tag has "maximum-scale=1", which blocks pinch zoom. | Accessibility |
| TC-066 | [LOGGED OUT] Meta description is real text about LUDUS | Low | The meta description is placeholder text ("Your Game takes players on a grand adventure ..."). | SEO |

## Account changes

- TC-075 claimed "Free Gold" (500 gold); available again about 17h 48m later.
- TC-076 claimed "Free emeralds" (100 emeralds); available again about 6 days 17 hours later.
- TC-079 tried a 160-point Loyalty shop item with 40 points: "Not enough loyalty points" was shown and nothing was spent.
- TC-083 and TC-084 logged out (no stored account data changed).
