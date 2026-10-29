# Settings: ludus (https://site.ludus-game.com/)

## Cookie banner
- banner-title: How we use cookies
- cookie-button: Dismiss

## Facts seen before
- (2026-10-28) Only two real pages: Home (/) and Store (/store/). Reward chain, Clan reward and Loyalty shop are sections of the Store page.
- (2026-10-28) Language URLs look like /fr-FR. The chosen language is remembered for the next visit.
- (2026-10-28) Mobile shows an "Add It to Home Screen" banner with a "Claim" button and an X. Close it with the X, never with "Claim".
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
- The About the game video (do not play it).
