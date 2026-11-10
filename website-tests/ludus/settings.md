# Settings: ludus (https://site.ludus-game.com/)

## Cookie banner
- banner-title: How we use cookies
- cookie-button: Dismiss

## Facts seen before
- (2026-10-28) Only two real pages: Home (/) and Store (/store/, /store since 2026-11-06). Reward chain, Clan reward and Loyalty shop are sections of the Store page.
- (2026-10-28) Language URLs look like /fr-FR. The chosen language is remembered for the next visit.
- (2026-10-28) Mobile shows an "Add It to Home Screen" banner with a "Claim" button and an X. Close it with the X, never with "Claim".
- (2026-11-04) The Rewards Market (Reward chain) is a limited-time event. On 2026-10-30 it showed "Limited time 3d 08h"; by 2026-11-04 it had ended. While no event runs, the Store page has no Rewards Market section, no "Reward chain" item in its header or phone menu, no gold Store points balance (LOGGED IN), and only one point badge on the Special offer card.
- (2026-11-06) The Home header and phone menu no longer show "Reward chain" or "Clan reward" (Home header: Home, Store, Loyalty shop, language, Login). "Clan reward" missing is not explained by the event (asked the Ludus team). The Store page address is now /store (no final "/"). The Store tab order is now: Free wares, Battle Passes, Gifts to friends, Licenses, Might Passes, Ludus Royal, Ethereal Crystals, Spells, Runes, Dice of Fortune, Gold, Emeralds. The logout label is "Log out". On phones the logo is no longer in the header.
- (2026-11-04) The Loyalty Shop offers rotate: on 2026-11-04 there were 13 cards and "Alliance of Light" instead of "Magical Order".
- (2026-10-28) The wdio-mcp emulate_device tool gave a broken layout (header 1560px wide). Chrome mobileEmulation (deviceMetrics 390x844, pixelRatio 3) in start_session worked.

## Login (LOGGED IN mode)
- {TEST_USER_ID} is a placeholder. The real value is in settings.local.md (not in git). Put it in only while a test runs; never write it into a tracked file.
- login method: login-url-suffix (add it to any page URL)
- login-url-suffix: ?user-id={TEST_USER_ID}
- test user: {TEST_USER_ID}
- logged-in-check: the header shows a green button "Player{TEST_USER_ID}" (cut to "Play…" on phones) next to two balances (loyalty points and store points), and no "Login" button
- after-login-popup: sometimes a "Login successful" popup appears after login; close it with "Ok" (seen in the 2026-10-28 run, not during exploration). The cookie banner is still shown on a new session.
- session-length: not measured; the login stayed for the whole ~10 minute exploration, through reloads, page changes and a language switch
- WARNING: the green "Player{TEST_USER_ID}" button IS the logout button on desktop. One click logs out with no confirmation. Do not click it unless the step is a Logout test.
- The ?user-id= part is removed from the address after login (it becomes /store/ or /).

## Allowed when LOGGED IN
- Everything in "Allowed when LOGGED OUT"
- Claim free rewards (Free wares, Rewards Market, Clan reward) when a Claim button is shown
- Spend loyalty points in the Loyalty Shop
- Gift flow up to its confirmation screen, then close it (never the final button that opens payment). Note: on 2026-10-28 the "Gifts to friends" section was NOT shown for user {TEST_USER_ID}.
- Logout

## Allowed when LOGGED OUT
- Normal navigation clicks (header, footer, menu, tabs, language selector)
- Opening and closing popups and info dialogs
- Scrolling, carousels and sliders

## Never
- No payment, no purchase, ever: never click a button that shows a real-money price, or Buy, Purchase, Pay, Checkout, Add to cart, a paid Subscribe, or the final button of a flow that leads to payment. Never open or touch a payment window (Pay Station).
- Never type into any field. Never enter credentials, personal data or payment details.
- Never open external links or download files.

## Skip
- Content that changes: the Special offer bundle name, news text and date, countdown timers, Seasonal offers.
- Event content (limited time): the Rewards Market / Reward chain section, the "Reward chain" item in the Store header and phone menu, the gold Store points balance and the second point badge on the Special offer card. When writing a test case that checks any of these, put this precondition question before the first step that needs the event (before any click on "Reward chain"): Is "Reward chain" shown in the Store page header? (precondition). With no event running the test is then SKIPPED, not FAILED. Keep event checks out of tests that check other things. This is a rule for writing test cases only: when running tests, the website-tester uses only the preconditions written in each test.
- Loyalty Shop offer names and the number of cards (the offers rotate). Check the card layout instead: a name, an amount, an "Available" line and a green button with a point price.
- The About the game video (do not play it).
