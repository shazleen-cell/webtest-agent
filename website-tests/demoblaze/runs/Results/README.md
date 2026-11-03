# demoblaze PRODUCT STORE: all test results

This folder holds the latest result of every test case for the demoblaze practice shop (https://www.demoblaze.com/), collected from all test runs into one place. Each test appears once, with the result from the most recent run that included it.

The original run folders (for example `../2026-11-02_1059/`) are left untouched. This folder only holds copies.

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

Runs used: 2026-11-02_1059 (full run on Sonnet, 47 tests) and 2026-11-02_1250 (TC-044 re-run after the demo account was added to settings.local.md).

| | Tests | PASSED | FAILED | BLOCKED | SKIPPED | UNSURE |
|---|---|---|---|---|---|---|
| All | 47 | 29 | 17 | 0 | 0 | 1 |
| LOGGED OUT | 47 | 29 | 17 | 0 | 0 | 1 |
| LOGGED IN | 0 | 0 | 0 | 0 | 0 | 0 |

## What is in a test folder (for example `TC-044/`)

| File | What it is |
|---|---|
| `step01.png`, `step02.png`, ... | A screenshot taken after each step of the test |
| `stepNN_FAIL.png` | The screenshot of a step that failed, marked in red |
| `TC-xxx_replay.gif` | An animation of all the step screenshots in order. This stands in for a video, since no real video can be recorded. |
| `TC-xxx_steps.pdf` | A printable list of the steps with their answers and screenshots |
| `TC-xxx_trace.zip` | A full browser trace of the test. Open it at https://trace.playwright.dev to see every action, page change and network request. Traces can contain typed values, so this folder must never go to git. |

The `json/` folder has the raw result of every test (`TC-xxx.json`), which the report is built from.

## What the statuses mean

| Status | Meaning |
|---|---|
| **PASSED** | Every check gave the expected answer. |
| **FAILED** | At least one check did not give the expected answer, or a step could not be done. This can be a bug on the site or a test that needs rewording. The table below says which. |
| **BLOCKED** | The test could not continue without breaking a safety rule, a needed test-account value was missing, or the test user was not logged in. Someone needs to look at it. |
| **SKIPPED** | The test's starting condition was not met, so its action could not be tried (on reward sites: the reward was already claimed or is on cooldown). This is not a bug. Run it again later. |
| **UNSURE** | The tester could not tell the answer from the page. |

## [LOGGED OUT] and [LOGGED IN]

- **[LOGGED OUT]**: the test runs as a visitor who is not logged in. Some of these tests still type into the Log in popup (allowed by "Allowed to type" in settings.md), for example a wrong password, to check the error messages.
- **[LOGGED IN]**: the test logs in as the demo account {TEST_USERNAME} through the Log in popup. There are no LOGGED IN tests in this report yet.

## Account changes

Tests that change the account or the cart list what they changed under "Account changes", with before and after values. No test in this report changed anything. No test ever pays real money; demoblaze is a practice shop that takes no payments.

## Tests that did not pass

| TC | Test | Priority | What happened | Bug or test wording? |
|---|---|---|---|---|
| TC-010 | [LOGGED OUT] "Previous" goes back to the first page of products | Medium | After "Next" then "Previous", the list starts at "Nokia lumia 1520" and ends with "Apple monitor 24"; "Samsung galaxy s6" is missing, so it is not the original first page | Bug |
| TC-011 | [LOGGED OUT] Product images on page 2 open the product page | Medium | Page 2 product images link to "#", so clicking one stays on Home; only the titles open the product | Bug |
| TC-015 | [LOGGED OUT] Unknown product shows a clear message instead of "undefined" | Medium | prod.html?idp_=999 shows "undefined", "$undefined", a broken image and an "Add to cart" button | Bug |
| TC-016 | [LOGGED OUT] Product page header has the same layout as Home | Low | The logo starts at 165 px on product pages but at 16 px on Home, and the menu moves too | Bug |
| TC-017 | [LOGGED OUT] Tab title names the product on a product page | Low | The tab title is only "STORE" on every product page | SEO |
| TC-019 | [LOGGED OUT] Cart page does not mark "Home" as the current page | Low | "Home" still has the hidden text "(current)" on Cart | Accessibility |
| TC-020 | [LOGGED OUT] Cart content has a side margin | Low | The "Products" heading and table touch the left edge of the window | Bug |
| TC-025 | [LOGGED OUT] Form fields in the popups have names for screen readers | Low | The Log in labels point to the wrong field ids, and the Contact Email field has no label | Accessibility |
| TC-026 | [LOGGED OUT] Unknown page shows a friendly error with a way back | Medium | The 404 page is a plain "Error: Not Found" server page with no header and no link back | Bug |
| TC-027 | [LOGGED OUT] Phone burger button is visible | Medium | The burger button is there (top right) but nothing is drawn: no icon | Bug |
| TC-028 | [LOGGED OUT] Phone menu is closed until the burger is tapped | Medium | The menu is already open when the page loads and stays open after a tap | Bug |
| TC-029 | [LOGGED OUT] Phone menu items fit on one line each | Low | "About us", "Log in" and "Sign up" each wrap over two lines | Bug |
| TC-030 | [LOGGED OUT] Phone home has no large empty area at the top | Low | About 200 px of empty blue area between the menu and the categories | Bug |
| TC-035 | [LOGGED OUT] http and non-www addresses go to https www with a permanent redirect | Medium | http redirects with a temporary 302, and https://demoblaze.com/ does not redirect to www | Security finding |
| TC-036 | [LOGGED OUT] Page response has the usual security headers | Medium | None of the usual security headers (HSTS, CSP, X-Frame-Options and others) are sent | Security finding |
| TC-038 | [LOGGED OUT] Home has an h1, a meta description and a canonical link | Low | No h1, an empty meta description and no canonical link | SEO |
| TC-039 | [LOGGED OUT] Home images and product links have text for screen readers | Low | The header logo has no alt text and the 9 product image links have no accessible name | Accessibility |
| TC-046 | [LOGGED OUT] Contact form with empty fields asks to fill them in | Medium | UNSURE: the page reloaded after "Send message" and wiped the alert recorder before it was read. The recorder now keeps alerts across a reload; re-run this test | Test wording |
