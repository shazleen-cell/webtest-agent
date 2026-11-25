# Settings for ludus

Site: https://site.ludus-game.com/

## Cookie banner
- banner-title: How we use cookies
- cookie-button: Dismiss

## Facts seen before
- The shop is a one-page app: the pages are `/` (Home) and `/store` (Store). Languages use a prefix, for example `/de-DE` and `/de-DE/store`. An unknown path answers 404 and then shows the Home page at `/`.
- The chosen language is remembered: after choosing Deutsch, opening `/` goes to `/de-DE` again.
- Every button with a USD price leads to payment (Xsolla Pay Station). The whole shop card is also clickable: only click named buttons, never a card.
- Prices, countdowns, offers, news and the Seasonal cards change; do not test their exact values.
- On a phone a bottom bar "Add It to Home Screen" has a green "Claim" button. It is an install prompt, not a reward: do not click it.
- The site sometimes answers "504 Gateway Time-out" once; opening the page again works.
- LOGGED IN, the current test account sees far fewer shop sections: only Special offers (a carousel) and Gold have price buttons; Free wares has no "Atlantis Tokens"; Gifts to friends is hidden, so the gift flow cannot be tested with this account. The Loyalty shop shows 7 cards and the account has fewer points than the cheapest one.

## Login (LOGGED IN mode)
- login method: login-url-suffix
- login-url-suffix: ?user-id={TEST_USER_ID}
- logged-in-check: the header shows a loyalty points badge (a number) and a green button with a door icon and the player name "Player{TEST_USER_ID}" (cut off as "Player..." in the phone burger menu), and no "Login" button. Wait about 3 seconds after the page loads.
- after-login-popup: none seen (2026-11-24). The login suffix disappears from the address bar after login. The cookie banner is shown again in every new session.
- session-length: not measured; still logged in after a reload without the suffix, after going Store -> Home and after switching to Français (about 10 minutes observed).
- logout: the green player-name button in the header (desktop), "Log out" in the burger menu (phone).

## Allowed when LOGGED OUT
- Looking at pages and normal navigation clicks (header, footer, menus, store category tabs, carousel arrows and dots, language selector).
- Closing the cookie banner.
- Opening and closing popups (Login prompt, News, Referral program panel, burger menu) and FAQ answers.

## Allowed when LOGGED IN
- Everything in "Allowed when LOGGED OUT".
- Logging in with the login-url-suffix.
- Normal navigation clicks and looking.
- "Logout".
- Clicking free "Claim" buttons (rewards that cost nothing).
- Spending in-game points or in-game currency (a button whose price is in points or in-game currency, never a real-money amount).
- NOT allowed: the gift flow, any button with a real-money price, or anything that opens a payment window. If a click that is allowed here leads to a payment window or asks for real money, the test is FAILED; it is never continued.

## Never
- No payment and no purchase, ever: never click a button that shows a real-money price, or Buy, Purchase, Pay, Checkout, Add to cart, a paid Subscribe, or the final button of a flow that leads to payment. Never open or touch a payment window (Pay Station).
- Never type into any field, never enter credentials, personal data or payment details.
- Never open external links (App Store, Google Play, Web-Version, social media, Support, Xsolla, Affiliate Program) or download files.
- Never click "Invite friends" in the Referral program panel.
- Never click the "Claim" button of the phone "Add It to Home Screen" bar.

## Skip
- Rotating content (countdowns, limited-time offers, news) and the current year.

## Allowed to type
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- fields:
  - Log in popup, "Username:" = {TEST_USERNAME}
  - Log in popup, "Password:" = {TEST_PASSWORD}
- submit-buttons:
  - "Log in" (inside the Log in popup)

## Allowed cart actions
- status: OFF
- site-is-demo: <why this site takes no real payments, and who confirmed it>
- approved-by: <name and date>
- buttons:
  - "Add to cart" on product pages
  - "Delete" in the Cart table

## Allowed demo checkout
- status: OFF
- site-is-demo: <why this site takes no real payments, and who confirmed it>
- approved-by: <name and date>
- buttons:
  - "Place Order" in the Cart
  - "Purchase" in the order form
- fields (fake values only):
  - Order form, "Name:" = Test User
  - Order form, "Country:" = Testland
  - Order form, "City:" = Test City
  - Order form, "Credit card:" = <a value the team confirmed is fake for this demo site>

## Allowed invalid-card check
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- payment-window: Xsolla Pay Station
- values: INVALID made-up values in `settings.card.local.md` (git-ignored), never in a tracked file
- fields:
  - card number field = {CARD_NUMBER}
  - expiry date field = {CARD_EXPIRY}
  - security code field = {CARD_CVC}
  - email field = {CARD_EMAIL}
- buttons:
  - "Pay" (once)
  - the control that closes the payment window
- evidence: nothing is captured while the card form is filled

## Allowed person-typed card check
- status: ON
- approved-by: shazleen-cell (by typing "proceed"), 2026-11-24
- payment-window: Xsolla Pay Station
- who-types: a person, in the open Chrome window (the agent types nothing and never clicks "Pay")
- items:
  - "Small welcome bundle", at most USD 5.94
  - "Medium welcome bundle", at most USD 59.40
  - "Big welcome bundle", at most USD 118.80
  - "Small pile of gold", at most USD 3.17
  - "Piggy bank of gold", at most USD 11.79
  - "Carpetbag of gold", at most USD 22.08
  - "Goblet of gold", at most USD 42.57
  - "Strongbox of gold", at most USD 80.74
- card-kinds:
  - invalid: ALLOWED
  - real: ALLOWED
- auto-pay: ALLOWED
- max-total-per-run: USD 50
- agent-buttons:
  - the control that closes the payment window (for Pay Station: the back arrow "Ludus", top left, `[data-testid=return-button]` inside `iframe.paystation-modal__iframe`)
- evidence: nothing is captured from the moment the person starts typing until the payment window is closed

## Allowed logged-out price click
- status: ON
- approved-by: shazleen-cell (by typing "proceed"), 2026-11-24
- mode: LOGGED OUT only (fresh session, no login link)
- buttons:
  - the real-money price button named in the case (once)
  - the control that closes the login prompt
