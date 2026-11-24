# Settings for ludus

Site: https://site.ludus-game.com/

## Cookie banner
- banner-title: How we use cookies
- cookie-button: Dismiss

## Facts seen before
- The shop is one page app: pages are `/` and `/store` (languages: `/de-DE`, `/de-DE/store`, ...). Any other path answers 404 and then shows the Home page.
- Payment goes through Xsolla Pay Station: every button with a USD price leads to payment.
- Prices, countdowns, offers, news and the Seasonal cards change; do not test their exact values.
- On a phone a bottom bar "Add It to Home Screen" has a green "Claim" button. It is an install prompt, not a reward: do not click it.
- The green button with a door icon and the player name in the header is the Logout button (on a phone, "Log out" is in the burger menu).
- After opening a page with the login suffix the header can still show "Login" for about 3 seconds: wait before checking the login.
- For the current test account the Loyalty shop is hidden (no cards), so spending loyalty points cannot be tested.

## Login (LOGGED IN mode)
- login method: login-url-suffix
- login-url-suffix: ?user-id={TEST_USER_ID}
- logged-in-check: the header shows a loyalty points badge (a number) and a green button with a door icon and the player name (cut off on phones), and no "Login" button (wait about 3 seconds after the page loads)
- after-login-popup: none seen during exploration (a "Login successful" popup may appear; close it with "Ok"). The cookie banner is shown again on every new session.
- session-length: (not measured)

## Allowed when LOGGED OUT
- Looking at pages and normal navigation clicks (header, footer, menus, tabs, carousel arrows, language selector).
- Closing the cookie banner.
- Opening and closing popups and FAQ answers.

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
- Never open external links or download files.

## Skip
- Rotating content (countdowns, limited-time offers) and the current year.

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
- approved-by: shazleen-cell, 2026-11-23 (approved in the chat; invalid card only); items extended to every logged-in paid item at shazleen-cell's request, 2026-11-24
- payment-window: Xsolla Pay Station
- who-types: a person, in the open Chrome window (the agent types nothing and never clicks "Pay")
- items:
  - "Small pile of gold", at most USD 3.00
  - "Small welcome bundle", at most USD 5.50
  - "Medium welcome bundle", at most USD 59.40
  - "Big welcome bundle", at most USD 118.80
  - "Piggy bank of gold", at most USD 11.79
  - "Carpetbag of gold", at most USD 22.08
  - "Goblet of gold", at most USD 42.57
  - "Strongbox of gold", at most USD 80.74
- card-kinds:
  - invalid: ALLOWED
  - real: NOT ALLOWED
- agent-buttons:
  - the control that closes the payment window (for Pay Station: the back arrow "Ludus", top left)
- evidence: nothing is captured from the moment the person starts typing until the payment window is closed

## Allowed logged-out price click
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- mode: LOGGED OUT only (fresh session, no login link)
- buttons:
  - the real-money price button named in the case (once)
  - the control that closes the login prompt
