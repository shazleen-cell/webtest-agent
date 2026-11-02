# LUDUS web shop: all test results

This folder holds the latest result of every test case for the LUDUS web shop (https://site.ludus-game.com/), collected from all test runs into one place. Each test appears once, with the result from the most recent run that included it.

The original run folders (for example `../2026-10-28_1132/`) are left untouched. This folder only holds copies.

## Start here

Open **`results.html`** in a browser. It has:
- an Overview with the totals, the pass rate by category (Functional / Non-functional), mode and priority, the tests that need attention, the changes made to the test account, and a list of all tests with the run each result came from. Click a category, mode or priority to show only those tests.
- a list of all tests on the left, with search and filters for status, mode, priority and category
- one page per test. It starts with what went wrong: the failed step, its expected and actual answer, and its screenshot. Below that are the evidence files, a replay animation and every step. Failed steps are shown in red.

**`results.xlsx`** has the same data as a spreadsheet, in three sheets:
- "Summary": the totals
- "Results": one row per test
- "Steps": one row per step

## Totals

Runs used: 2026-10-30_0829 (full run on Sonnet, 86 tests), 2026-10-30_1003 (TC-037 and TC-059 re-run after their steps were fixed) and 2026-10-30_1016 (TC-072 re-run with the no-script-click rule).

| | Tests | PASSED | FAILED | BLOCKED | SKIPPED | UNSURE |
|---|---|---|---|---|---|---|
| All | 89 | 66 | 23 | 0 | 0 | 0 |
| LOGGED OUT | 73 | 52 | 21 | 0 | 0 | 0 |
| LOGGED IN | 16 | 14 | 2 | 0 | 0 | 0 |

## What is in a test folder (for example `TC-051/`)

| File | What it is |
|---|---|
| `step01.png`, `step02.png`, ... | A screenshot taken after each step of the test |
| `stepNN_FAIL.png` | The screenshot of a step that failed, marked in red |
| `TC-xxx_replay.gif` | An animation of all the step screenshots in order. This stands in for a video, since no real video can be recorded. |
| `TC-xxx_steps.pdf` | A printable list of the steps with their answers and screenshots |
| `TC-xxx_trace.zip` | A full browser trace of the test. Open it at https://trace.playwright.dev to see every action, page change and network request. |

The `json/` folder has the raw result of every test (`TC-xxx.json`), which the report is built from.

## What the statuses mean

| Status | Meaning |
|---|---|
| **PASSED** | Every check gave the expected answer. |
| **FAILED** | At least one check did not give the expected answer, or a step could not be done. This can be a bug on the site or a test that needs rewording. The table below says which. |
| **BLOCKED** | The test could not continue without breaking a safety rule (for example, the next step would pay real money), or the test user was not logged in. Someone needs to look at it. |
| **SKIPPED** | The test's starting condition was not met, so its action could not be tried. Usually a free reward was already claimed or is on cooldown. This is not a bug. Run it again later. |
| **UNSURE** | The tester could not tell the answer from the page. |

## [LOGGED OUT] and [LOGGED IN]

- **[LOGGED OUT]**: the test runs as a visitor who is not logged in.
- **[LOGGED IN]**: the test logs in as the approved test user {TEST_USER_ID}, by adding `?user-id={TEST_USER_ID}` to the page address. Clicks in these tests are real and can change that user's account.

## Account changes

Some LOGGED IN tests change the test account on purpose: claiming a free reward or spending loyalty points. Each test's page lists what it changed under "Account changes", with before and after values. Changes so far:

- TC-051: bought "Unique Frame" for 160 loyalty points (loyalty points 200 -> 40)
- TC-052: claimed Free Gold (500), available again about 16 hours later
- TC-053: claimed Free emeralds (100), available again about 4.5 days later

No test ever pays real money.

## Tests that did not pass

| TC | Test | Priority | What happened | Bug or test wording? |
|---|---|---|---|---|
| TC-008 | [LOGGED OUT] Header "Clan reward" on Home opens a clan reward section | Medium | Opens the Store page at the top; there is no Clan reward section anywhere | Bug (or the feature is turned off) |
| TC-009 | [LOGGED OUT] Header "Loyalty shop" on Home opens the Store at the Loyalty Shop section | Medium | Opens the Store page at the top, not at the Loyalty Shop | Bug |
| TC-010 | [LOGGED OUT] Header "Reward chain" on Home opens the Store at the Rewards Market section | Medium | Opens the Store page at the top, not at the Rewards Market | Bug |
| TC-024 | [LOGGED OUT] The news date is the same in English and French | Low | The same news card says "October 15" in English but "10 mars" in French | Content bug |
| TC-026 | [LOGGED OUT] Top of the "Referral program" panel is fully visible at 1440x900 | Low | The first line "Invite friends —" is cut off at the top of the window | Bug |
| TC-029 | [LOGGED OUT] Store header shows the same menu items as Home, including "Clan reward" | High | The Store header has no "Clan reward" item, although Home has one | Bug |
| TC-033 | [LOGGED OUT] Last Store tab "Gift to friends" is fully visible at 1440x900 | Low | Only "Gift" of the last tab "Gift to friends" is visible; the rest is cut off | Bug |
| TC-042 | [LOGGED OUT] Loyalty Shop offers have different names | Low | Two cards are called "Astral hero" and "Astral Hero" | Content bug |
| TC-048 | [LOGGED OUT] Unknown page shows a clear error message | Medium | The unknown address silently shows Home; no not-found message | Bug |
| TC-051 | [LOGGED OUT] Phone cookie "Dismiss" button is not covered by other elements | Low | The "Add It to Home Screen" banner partly covers "Dismiss" (it can still be clicked) | Bug |
| TC-053 | [LOGGED OUT] Phone "Add It to Home Screen" banner text has no spelling mistakes | Low | The banner says "To got a quicker access !" | Content bug |
| TC-057 | [LOGGED OUT] Phone Store burger menu shows "Clan reward" like on Home | Medium | The phone menu on the Store page has no "Clan reward" item | Bug |
| TC-058 | [LOGGED OUT] Phone "Referral program" button shows its icon and opens the panel | Low | On a phone the Referral panel covers its own close X, so it cannot be closed with it | Bug |
| TC-060 | [LOGGED OUT] Store page loads with no failed requests | Medium | 404 errors for manifest.json and store.xsolla.com offer_chain / bundle requests | Bug |
| TC-063 | [LOGGED OUT] Page response has the usual security headers | Medium | Only Strict-Transport-Security is sent; CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy and Permissions-Policy are missing | Security finding |
| TC-065 | [LOGGED OUT] Home images and links have text for screen readers | Low | Images without alt text, and links and buttons without a name | Accessibility |
| TC-066 | [LOGGED OUT] Store images have alt text and the page has one h1 heading | Low | 46 of 293 images have no alt text and the page has no h1 heading | Accessibility |
| TC-068 | [LOGGED OUT] Phone users can zoom the page | Low | The viewport meta tag has maximum-scale=1, which blocks zooming | Accessibility |
| TC-069 | [LOGGED OUT] Meta description is real text about LUDUS | Low | The meta description is placeholder text and a hidden "Your game title" heading exists | SEO |
| TC-072 | [LOGGED OUT] Layout works on a tablet (768x1024) | Medium | On a 768x1024 tablet the Referral button covers the cookie "Dismiss" button, so it cannot be clicked. The layout itself is fine | Bug |
| TC-073 | [LOGGED OUT] Phone burger menu close button has a name for screen readers | Low | The close (x) is an image in plain divs: no button role, no name, not reachable by keyboard | Accessibility |
| TC-087 | [LOGGED IN] Gift flow can be started from the Store | Medium | This test user has no "Gifts to friends" section, so the gift flow cannot start | Test wording (account limit, to confirm with the team) |
| TC-089 | [LOGGED IN] Logout with "Logout" in the phone burger menu | High | Logout works, but the menu stays open and covers the header Login button | Bug (minor) |

