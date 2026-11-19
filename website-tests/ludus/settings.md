# Settings for ludus

Site: https://site.ludus-game.com/

## Cookie banner
- banner-title: How we use cookies
- cookie-button: Dismiss

## Facts seen before
- The shop is one page app: pages are `/` and `/store` (languages: `/de-DE`, `/de-DE/store`, ...). Any other path ends on the Home page.
- Payment goes through Xsolla Pay Station: every button with a USD price leads to payment.
- Prices, countdowns, offers and the news change; do not test their exact values.
- On a phone a bottom bar "Add It to Home Screen" has a green "Claim" button. It is an install prompt, not a reward: do not click it.
- The green "Player{TEST_USER_ID}" button in the header is the Logout button (one click logs out, no confirmation).

## Login (LOGGED IN mode)
- login method: login-url-suffix
- login-url-suffix: ?user-id={TEST_USER_ID}
- logged-in-check: the header shows a loyalty points badge (a number) and a green button "Player{TEST_USER_ID}" with a door icon (cut to "Player…" on phones), and no "Login" button
- after-login-popup: none seen during exploration (a "Login successful" popup may appear; close it with "Ok"). The cookie banner is still shown on a new session.
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
