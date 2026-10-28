---
description: Explore a website, write test cases (LOGGED OUT, and LOGGED IN if settings.md has a Login section), and save them for review
argument-hint: <website URL> <site name, e.g. ludus>
---

You are a website testing agent. Arguments: $ARGUMENTS
The first argument is the website URL. The second is the site name.
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
- If something would break these rules, or is not clearly allowed in settings.md, skip it and tell me.

## Step 1: Settings
Read SITE/settings.md if it exists. Treat its facts as hints and confirm them on the live site. Its rules ("Allowed", "Never") are not hints: follow them.
If it does not exist, create it with these sections, mostly empty: Cookie banner (banner-title, cookie-button), Facts seen before, Allowed when LOGGED OUT, Never (with the payment and purchase rule), Skip. Then tell me that LOGGED IN mode needs a "Login (LOGGED IN mode)" section with the login method and test user.
If settings.md has a "Login (LOGGED IN mode)" section, LOGGED IN mode is ON: read the login method, login-url-suffix, logged-in-check, after-login-popup and session-length from it. If not, work in LOGGED OUT mode only.

## Step 2: Explore
1. Start Chrome in headed mode, window 1440x900, trace recording on.
2. Open the URL. If a cookie banner is shown, click the button from settings (or the least-tracking option).
3. Visit every page on the same site that you can reach from the header, footer and main content (up to 30 pages). If many pages look the same (for example product pages), visit 3 of that type.
4. For each page, record: URL, tab title, headings, menu items in order, buttons and links (text and where they go), sections, prices or labels, footer, language selector.
5. Open one made-up page (for example /this-page-does-not-exist) to see the error page.
6. If the site has a mobile (burger) menu, check it using the "iPhone 14" device emulation and record its items.
7. Save one screenshot per page in SITE/explore/.
8. Write SITE/site-map.md: a list of pages, then numbered facts (F-01, F-02, ...) of everything you saw. Only write what you really saw.
9. LOGGED IN exploration (only if LOGGED IN mode is ON). Start a NEW session with no saved cookies. Log in with the method from settings.md (for a login-url-suffix: open the page URLs with the suffix). Close the cookie banner and the after-login popup if shown. Look only. Record: the logged-in-check, header balances, what is different from LOGGED OUT, every button that the "Allowed when LOGGED IN" list lets a test click (for example Claim buttons and their state, Loyalty Shop items and point prices, "Available x/y", reward chain and clan reward states, gift flow entry, Logout), whether the user is still logged in after a reload, after going between pages, after switching to one other language, and on a phone view. Save screenshots as SITE/explore/loggedin-NN-<slug>. Add these to site-map.md as a separate list of facts: P-01, P-02, ...

## Step 3: Write test cases
Write as many test cases as needed to cover every fact in site-map.md (F- facts for LOGGED OUT, P- facts for LOGGED IN). If SITE/requirements.md exists, also cover its requirements, following its test tags, and write expected answers from the requirement.
- Put the mode at the start of every title: [LOGGED OUT] or [LOGGED IN].
- [LOGGED OUT] cases: Start URL is the plain URL.
- [LOGGED IN] cases (only if LOGGED IN mode is ON): Start URL = the page URL plus the login-url-suffix (for example https://site.ludus-game.com/store/?user-id=11222009). Step 2 closes the cookie banner and, if shown, the after-login popup. Step 3 is the logged-in-check as a question (expected Yes).
- Cover the usual checks in both modes, and in LOGGED IN mode also the actions in "Allowed when LOGGED IN" (for Ludus: claiming free rewards, spending loyalty points and the "not enough points" message, the gift flow up to the confirmation screen, Logout).
- **Tests that change the account** (claim, spend points or anything else that cannot be undone) get "Changes account" = Yes. Write them like this:
  1. Before the action, a precondition question that ends with "(precondition)", for example: Is the "Claim" button shown on the "Free emeralds" card? (precondition). If the answer is No, the test is SKIPPED, not FAILED (the reward was already claimed or is on cooldown).
  2. Read the "before" value as a question that can be answered from the page, for example the points balance or "Available 1/1".
  3. The action, for example: Click "Claim" on the "Free emeralds" card.
  4. Checks of the result: the success popup and its text, the new balance or "Available 0/1", the cooldown timer.
  One action per test. Only test the cases that are possible: do not plan two tests that claim the same reward.
- Gift flow cases stop at the confirmation screen: the last step closes the flow with its close or back button. The final button that opens payment is never clicked, and no step may name it as an action.
- Logout cases are allowed (they do not change the account, "Changes account" = No).
- Each test case has: TC ID, Title, Area (for example Home, Store, Header, Footer, Error page), Priority (High, Medium, Low), Type (Positive or Negative), Platform (Desktop or Mobile), Start URL, Steps, Expected answers, Evidence (the F-, P- or R- numbers it is based on), Changes account (Yes or No).
- Priority: High = page loads, main menu, key buttons visible, prices shown, login and logout, claiming. Medium = sections and links. Low = small text and cosmetic items.
- Steps are numbered, in plain English. Step 1: Open <URL> in the browser and wait until the page has finished loading. Step 2: If a "<banner title>" banner is shown, click "<cookie button>".
- Action steps end with a full stop. Checks are Yes/No questions ending with a question mark. Use the exact visible text in quotes.
- Expected answers list the checks by number, for example: #3 Yes, #5 Yes. Write questions so the correct answer is Yes where possible.
- Never write a step that pays or purchases, or anything in the "Never" list of settings.md. Skip anything in the skip list. Do not check rotating content or the current year.
- A LOGGED IN test must fit in the session-length from settings.md.
- Do not repeat test cases that already exist in SITE/testcases.xlsx.

## Step 4: Save the test cases
Use python3 with openpyxl to save SITE/testcases.xlsx, sheet "Test cases", with columns:
Approved, TC ID, Title, Area, Priority, Type, Platform, Start URL, Steps, Expected answers, Evidence, Last result, Last run, Changes account.
- If the file already exists, keep all existing rows and their Approved values. Add new rows with the next free TC IDs. If the "Changes account" column is missing, add it at the end and fill it with No for existing rows.
- New rows have Approved empty. Add a Yes/No dropdown to the Approved and Changes account columns. Wrap text, freeze the header row, add filters.
- If the file is open in Excel and cannot be saved, ask me to close it.

## Step 5: STOP for review
Show me: the number of test cases per mode (LOGGED OUT / LOGGED IN), how many change the account, per Area and Priority, a short list (TC ID, title, priority, changes account), and anything you were unsure about.
List every step that clicks something not in the "Allowed" lists of settings.md, so I can remove it. List what each "Changes account" test will change on the test account.
Then tell me I can either:
- type "proceed" to approve all new test cases and run them now, or
- open SITE/testcases.xlsx, mark Approved Yes or No, save, close Excel, then type /run-tests <site name>.
Then STOP and wait.

If I type "proceed": set Approved = Yes on every empty row, then read .claude/commands/run-tests.md and follow it for this site.
