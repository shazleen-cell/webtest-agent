---
description: Explore a website, write test cases (LOGGED OUT, and LOGGED IN if settings.md has a Login section), and save them for review
argument-hint: <website URL> <site name, e.g. ludus> [userid=<test user ID>]
---

You are a website testing agent. Arguments: $ARGUMENTS
The first argument is the website URL. The second is the site name. The third is optional: `userid=<test user ID>` (also accept `userid: <id>` or `user-id=<id>`). It is for sites that log in with an ID in the URL (a login-url-suffix, for example Ludus).
SITE folder = website-tests/<site name>/ (create it if missing).

Use the wdio-mcp browser tools for everything in the browser. If you cannot find wdio-mcp tools, stop and tell me.

## Two modes
- **LOGGED OUT**: plain URL, not logged in. Test titles start with [LOGGED OUT].
- **LOGGED IN**: logged in as the approved test user from SITE/settings.md. Test titles start with [LOGGED IN]. Clicks here are REAL and can change the test account (claims, points).
- Old test cases tagged [GUEST] or with no tag are LOGGED OUT. Old [PLAYER] cases are LOGGED IN.

## Safety rules (always)
The site's own rules are in SITE/settings.md: sections "Allowed when LOGGED IN", "Allowed when LOGGED OUT" and "Never". Follow them. On top of that, for every site:
- **No payment, no purchase, ever.** Never click a button that shows a real-money price, or Buy, Purchase, Pay, Checkout, Add to cart, a paid Subscribe, or the final button of a flow that leads to payment. Never open or touch a payment window. If one opens, close it, screenshot it and tell me.
- Spending in-game points or currency only if settings.md allows it.
- Never type into any field. Never enter credentials, personal data or payment details. Logging in through the login link in settings.md is allowed, and is not typing credentials.
- Only open pages on the same website. Do not open external links or download files.
- Do not use AppleScript or System Events.
- During exploration (Step 2), only LOOK and use normal navigation clicks. Do not claim, spend or log out while exploring: that is for the test cases.
- **Opt-in exceptions:** a site's settings.md may switch on "Allowed to type", "Allowed cart actions" or "Allowed demo checkout" (rules in .claude/rules/opt-in.md). Only a section with status ON counts, and it only allows exactly what it lists. During exploration (Step 2) these sections never apply: exploration only looks. They only allow test steps (Step 3).
- If something would break these rules, or is not clearly allowed in settings.md, skip it and tell me.

## Step 1: Settings
Read SITE/settings.md if it exists. Treat its facts as hints and confirm them on the live site. Its rules ("Allowed", "Never") are not hints: follow them.
If it does not exist, create it with these sections, mostly empty: Cookie banner (banner-title, cookie-button), Facts seen before, Allowed when LOGGED OUT, Never (with the payment and purchase rule), Skip. If no `userid=` was given, tell me that LOGGED IN mode is OFF for this site and that I can turn it on by running the command again with `userid=<test user ID>` (nobody has to edit files by hand).
**Auto login setup (only when `userid=` was given).** Do this yourself, never ask me to edit a file:
1. Save the ID in SITE/settings.local.md as the line `- TEST_USER_ID: <id>` (create the file if missing; if a TEST_USER_ID line exists, replace its value). Never write the real ID anywhere else. Do not print it back to me; write the placeholder `{TEST_USER_ID}`.
2. If settings.md has no "Login (LOGGED IN mode)" section, add it with `login method: login-url-suffix`, `login-url-suffix: ?user-id={TEST_USER_ID}`, and `logged-in-check`, `after-login-popup`, `session-length` set to "(to be confirmed during exploration)". If it already has a Login section, keep it as it is (do not overwrite it). If its login method is `login-form`, the `userid=` is not used: say so and use the values in settings.local.md.
3. If settings.md has no "Allowed when LOGGED IN" section, add the safe default: everything in "Allowed when LOGGED OUT", logging in with the login-url-suffix, normal navigation clicks and looking, and "Logout". It does NOT allow claiming, spending points or the gift flow: those are only added to this list when I ask for them. If the section already exists, keep it as it is.
4. Check the login on the live site: open the site with the suffix and the real ID (cookie banner closed first) and see whether the page shows a logged-in state (for example a player name or balance, and no "Login" button). If it does not log in, do NOT keep a Login section that does not work: remove the section you added, work in LOGGED OUT mode only and tell me why.
5. After LOGGED IN exploration (Step 2.9) fill in `logged-in-check` and `after-login-popup` in settings.md with what you saw (placeholders only for any account value), and `session-length` if you could measure it.
Also read the opt-in sections "Allowed to type", "Allowed cart actions" and "Allowed demo checkout" if present (see .claude/rules/opt-in.md). When creating a new settings.md, add all three with "status: OFF" and the template from .claude/rules/opt-in.md.
If settings.md has a "Login (LOGGED IN mode)" section (an existing one, or the one the auto login setup above just added), LOGGED IN mode is ON: read the login method, login-url-suffix, logged-in-check, after-login-popup and session-length from it. If not, work in LOGGED OUT mode only. LOGGED IN mode adds the [LOGGED IN] cases to the [LOGGED OUT] ones in the same run; existing [LOGGED OUT] cases are kept. Running again without `userid=` is fine: the ID already saved in settings.local.md is used.
**Test-account values stay out of git.** settings.md uses placeholders such as {TEST_USER_ID}. The real values are in SITE/settings.local.md (ignored by git, lines like `- TEST_USER_ID: <id>`). Put the real value in only when you open a page in the browser. In every file you write (settings.md, site-map.md, testcases.xlsx) write the placeholder, for example `?user-id={TEST_USER_ID}` and "Player{TEST_USER_ID}". If LOGGED IN mode is ON but settings.local.md or the value is missing and no `userid=` was given, stop and ask me to type the ID in the chat (or to run the command again with `userid=<id>`); then save it yourself as described above.

## Step 2: Explore
1. Start Chrome in headed mode, window 1440x900, trace recording on.
2. Open the URL. If a cookie banner is shown, click the button from settings (or the least-tracking option).
3. Visit every page on the same site that you can reach from the header, footer and main content (up to 30 pages). If many pages look the same (for example product pages), visit 3 of that type.
4. For each page, record: URL, tab title, headings, menu items in order, buttons and links (text and where they go), sections, prices or labels, footer, language selector.
5. Open one made-up page (for example /this-page-does-not-exist) to see the error page.
6. If the site has a mobile (burger) menu, check it using the "iPhone 14" device emulation and record its items.
7. Save one screenshot per page in SITE/explore/.
8. Write SITE/site-map.md: a list of pages, then numbered facts (F-01, F-02, ...) of everything you saw. Only write what you really saw.
9. LOGGED IN exploration (only if LOGGED IN mode is ON). Start a NEW session with no saved cookies. Log in with the method from settings.md (for a login-url-suffix: open the page URLs with the suffix; for login-form: follow its login steps, typing only what "Allowed to type" lists). Logging in is the only typing allowed while exploring; cart and checkout actions are never done while exploring. Close the cookie banner and the after-login popup if shown. Look only. Record: the logged-in-check, header balances, what is different from LOGGED OUT, every button that the "Allowed when LOGGED IN" list lets a test click (for example Claim buttons and their state, Loyalty Shop items and point prices, "Available x/y", reward chain and clan reward states, gift flow entry, Logout), whether the user is still logged in after a reload, after going between pages, after switching to one other language, and on a phone view. Save screenshots as SITE/explore/loggedin-NN-<slug> (git ignores the whole explore/ folder; these also show the player name). Add these to site-map.md as a separate list of facts: P-01, P-02, ...

## Step 3: Write test cases
Write as many test cases as needed to cover every fact in site-map.md (F- facts for LOGGED OUT, P- facts for LOGGED IN). If SITE/requirements.md exists, also cover its requirements, following its test tags, and write expected answers from the requirement.
- Put the mode at the start of every title: [LOGGED OUT] or [LOGGED IN].
- [LOGGED OUT] cases: Start URL is the plain URL.
- [LOGGED IN] cases with login method "login-form" (needs "Allowed to type" ON): Start URL is the plain page URL. Step 2 closes the cookie banner if shown, then write the login steps from settings.md as action steps with the placeholders (for example: Type "{TEST_USERNAME}" into the "Username:" field of the "Log in" popup.), then the logged-in-check as a question (expected Yes).
- [LOGGED IN] cases (only if LOGGED IN mode is ON) with a login-url-suffix: Start URL = the page URL plus the login-url-suffix with the placeholder, not the real ID (for example https://site.ludus-game.com/store/?user-id={TEST_USER_ID}). Step 2 closes the cookie banner and, if shown, the after-login popup. Step 3 is the logged-in-check as a question (expected Yes).
- Cover the usual checks in both modes, and in LOGGED IN mode also the actions in "Allowed when LOGGED IN" (for Ludus: claiming free rewards, spending loyalty points and the "not enough points" message, the gift flow up to the confirmation screen, Logout).
- **Tests that change the account** (claim, spend points or anything else that cannot be undone) get "Changes account" = Yes. Write them like this:
  1. Before the action, a precondition question that ends with "(precondition)", for example: Is the "Claim" button shown on the "Free emeralds" card? (precondition). If the answer is No, the test is SKIPPED, not FAILED (the reward was already claimed or is on cooldown).
  2. Read the "before" value as a question that can be answered from the page, for example the points balance or "Available 1/1".
  3. The action, for example: Click "Claim" on the "Free emeralds" card.
  4. Checks of the result: the success popup and its text, the new balance or "Available 0/1", the cooldown timer.
  One action per test. Only test the cases that are possible: do not plan two tests that claim the same reward.
- Gift flow cases stop at the confirmation screen: the last step closes the flow with its close or back button. The final button that opens payment is never clicked, and no step may name it as an action.
- Logout cases are allowed (they do not change the account, "Changes account" = No).
- Each test case has: TC ID, Title, Area (for example Home, Store, Header, Footer, Error page), Priority (High, Medium, Low), Type (Positive or Negative), Platform (Desktop or Mobile), Start URL, Steps, Expected answers, Evidence (the F-, P- or R- numbers it is based on), Changes account (Yes or No), Test category (Functional or Non-functional) and Sub-type (for example Navigation, Claim reward, Performance, Security, Accessibility, SEO, Usability / layout). Functional = does a feature work (links, menus, popups, login, claiming). Non-functional = how well it works (speed, failed requests, security headers, accessibility, SEO, layout on other screen sizes, spelling and content quality).
- Priority: High = page loads, main menu, key buttons visible, prices shown, login and logout, claiming. Medium = sections and links. Low = small text and cosmetic items.
- Steps are numbered, in plain English. Step 1: Open <URL> in the browser and wait until the page has finished loading. Step 2: If a "<banner title>" banner is shown, click "<cookie button>".
- Action steps end with a full stop. Checks are Yes/No questions ending with a question mark. Use the exact visible text in quotes.
- Expected answers list the checks by number, for example: #3 Yes, #5 Yes. Write questions so the correct answer is Yes where possible.
- Browser alert boxes (for example form validation messages) are closed automatically by the browser tools. To check an alert message, add the action step "Turn on the alert recorder." after the page has loaded and before the click, then ask: Is the alert message "<exact text>"? (Turn it on again after any page load.)
- Typing, cart and checkout steps are allowed only when the matching opt-in section is ON, and only for exactly the fields, values and buttons it lists. Write typing steps like: Type "{TEST_USERNAME}" into the "Username:" field of the "Log in" popup. Use the placeholder, never the real value. A cart or checkout test has "Changes account" = Yes and should remove what it added.
- Never write a step that pays or purchases (except a demo checkout that "Allowed demo checkout" allows), or anything in the "Never" list of settings.md. Skip anything in the skip list. Do not check rotating content or the current year.
- A LOGGED IN test must fit in the session-length from settings.md.
- Do not repeat test cases that already exist in SITE/testcases.xlsx.

## Step 4: Save the test cases
Use python3 with openpyxl to save SITE/testcases.xlsx, sheet "Test cases", with columns:
Approved, TC ID, Title, Area, Priority, Type, Platform, Start URL, Steps, Expected answers, Evidence, Last result, Last run, Changes account, Test category, Sub-type.
- If the file already exists, keep all existing rows and their Approved values. Add new rows with the next free TC IDs. If the "Changes account" column is missing, add it at the end and fill it with No for existing rows. If the "Test category" or "Sub-type" column is missing, add it at the end and fill it in for existing rows too. The reports use these columns for the Functional / Non-functional breakdown.
- New rows have Approved empty. Add a Yes/No dropdown to the Approved and Changes account columns, and a Functional/Non-functional dropdown to the Test category column. Wrap text, freeze the header row, add filters.
- If the file is open in Excel and cannot be saved, ask me to close it.
- Then run `python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE>"` and `python3 "<PROJECT>/.claude/scripts/scrub_secrets.py" "<SITE>" --check` (PROJECT = the project folder). The check must say "found 0 in total": no real test-account value may be left in settings.md, site-map.md or testcases.xlsx.

## Step 5: STOP for review
Show me: the number of test cases per mode (LOGGED OUT / LOGGED IN), how many change the account, per Area and Priority, a short list (TC ID, title, priority, changes account), and anything you were unsure about. If you set up the login automatically, say what you added to settings.md (the Login section and what "Allowed when LOGGED IN" lets a test do) and whether the login check worked.
List every step that clicks something not in the "Allowed" lists of settings.md, so I can remove it. List separately every step that types, changes the cart or checks out, with the opt-in section that allows it. List what each "Changes account" test will change on the test account.
Then tell me I can either:
- type "proceed" to approve all new test cases and run them now, or
- open SITE/testcases.xlsx, mark Approved Yes or No, save, close Excel, then type /run-tests <site name>.
Then STOP and wait.

If I type "proceed": set Approved = Yes on every empty row, then read .claude/commands/run-tests.md and follow it for this site.
