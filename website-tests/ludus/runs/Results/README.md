# LUDUS web shop: all test results

This folder holds the latest result of every test case for the LUDUS web shop (https://site.ludus-game.com/), collected from all test runs into one place. Each test appears once, with the result from the most recent run that included it.

The original run folders (for example `../2026-10-28_1132/`) are left untouched. This folder only holds copies.

## Start here

Open **`results.html`** in a browser. It has:
- totals at the top, with filters for status, LOGGED OUT / LOGGED IN and priority
- a searchable list of all tests on the left
- an overview table showing which run each result came from
- one page per test with its steps, the expected and actual answer for each step, screenshots, and a replay animation. Failed steps are shown in red.

**`results.xlsx`** has the same data as a spreadsheet, in three sheets:
- "Summary": the totals
- "Results": one row per test
- "Steps": one row per step

## Totals

Runs used: 2026-10-28_1132 (TC-001 to TC-057) and 2026-10-28_1426 (TC-058 to TC-079).

| | Tests | PASSED | FAILED | BLOCKED | SKIPPED | UNSURE |
|---|---|---|---|---|---|---|
| All | 79 | 56 | 23 | 0 | 0 | 0 |
| LOGGED OUT | 62 | 43 | 19 | 0 | 0 | 0 |
| LOGGED IN | 17 | 13 | 4 | 0 | 0 | 0 |

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
- **[LOGGED IN]**: the test logs in as the approved test user 12580628, by adding `?user-id=12580628` to the page address. Clicks in these tests are real and can change that user's account.

## Account changes

Some LOGGED IN tests change the test account on purpose: claiming a free reward or spending loyalty points. Each test's page lists what it changed under "Account changes", with before and after values. Changes so far:

- TC-051: bought "Unique Frame" for 160 loyalty points (loyalty points 200 -> 40)
- TC-052: claimed Free Gold (500), available again about 16 hours later
- TC-053: claimed Free emeralds (100), available again about 4.5 days later

No test ever pays real money.

## Tests that did not pass

| TC | Test | Priority | What happened | Bug or test wording? |
|---|---|---|---|---|
| TC-014 | [LOGGED OUT] Header "Reward chain" on Home opens the Rewards Market section | Medium | Opens the Store page at the top, not at the Rewards Market | Bug |
| TC-015 | [LOGGED OUT] Header "Loyalty shop" on Home opens the Loyalty Shop section | Medium | Opens the Store page at the top, not at the Loyalty Shop | Bug |
| TC-016 | [LOGGED OUT] Header "Clan reward" on Home opens a Clan reward section | Medium | No Clan reward section anywhere on the Store page | Bug (or the feature is turned off) |
| TC-019 | [LOGGED OUT] Referral program panel fits in a 1440x900 window | Low | The top of the panel title "Invite friends —" is cut off | Bug |
| TC-021 | [LOGGED OUT] Store header menu also has "Clan reward" like the Home header | Medium | The Store header has no "Clan reward" item | Bug |
| TC-025 | [LOGGED OUT] Loyalty Shop item names are not duplicated | Low | "Astral hero" and "Astral Hero" both exist | Content bug |
| TC-027 | [LOGGED OUT] Store tab bar fits in a 1440x900 window | Low | The "Gift to friends" tab is cut to "Gift" | Bug |
| TC-039 | [LOGGED OUT] Mobile "Add It to Home Screen" banner text has no spelling mistake | Low | Says "To got a quicker access !" | Content bug |
| TC-045 | [LOGGED IN] Home "Clan reward" opens a Clan reward section when logged in | Medium | No Clan reward section when logged in either | Bug (or the feature is turned off) |
| TC-047 | [LOGGED IN] "Might Passes" category shows items | Low | The tab shows "The store is empty for now. Come back later!" | Possibly on purpose |
| TC-051 | [LOGGED IN] Spend 160 loyalty points on "Unique Frame" | High | The purchase worked, but the card disappears instead of showing "Available: 0/1" | Test wording (now fixed in testcases.xlsx) |
| TC-056 | [LOGGED IN] Phone header shows the full player name | Low | Shows "Play…" | Bug |
| TC-060 | [LOGGED OUT] Home and Store load without failed network requests | Medium | The Store page gets 404s (manifest.json, Xsolla store API calls) | Bug |
| TC-065 | [LOGGED OUT] Basic security headers are sent | Medium | X-Content-Type-Options, X-Frame-Options, Content-Security-Policy and Referrer-Policy are missing | Security finding |
| TC-067 | [LOGGED OUT] Home images have alt text | Medium | 2 images (the header logo) have no alt text | Accessibility |
| TC-068 | [LOGGED OUT] Store images have alt text | Medium | 46 of 321 images have no alt text | Accessibility |
| TC-069 | [LOGGED OUT] Icon-only links on Home have an accessible name | Medium | 14 links (logo, app badges, social icons) have no name a screen reader can read | Accessibility |
| TC-070 | [LOGGED OUT] Buttons on Home and Store have an accessible name | Medium | 7 buttons on Home and 12 on Store have no readable name | Accessibility |
| TC-072 | [LOGGED OUT] Keyboard focus is visible on header menu items | Low | Tab never reached the header, so the focus style was not checked | Test wording (now fixed in testcases.xlsx) |
| TC-073 | [LOGGED OUT] Pinch zoom is allowed on phones | Low | The page blocks zoom (maximum-scale=1) | Accessibility |
| TC-074 | [LOGGED OUT] Each page has exactly one h1 heading | Low | The Store page has no h1 heading | Accessibility / SEO |
| TC-075 | [LOGGED OUT] Meta description describes Ludus | Low | Still template text ("Your Game takes players on a grand adventure…") | SEO |
| TC-076 | [LOGGED OUT] Canonical link and og:url point to site.ludus-game.com | Low | They point to ludus-merge-battle-arena-pvp-landing.xsolla.site | SEO |
