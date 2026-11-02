# Settings: demoblaze-eval (https://www.demoblaze.com/)

Eval copy of website-tests/demoblaze/settings.md: the same site and the same rules, so the eval checks the agent under the real rules. If you change website-tests/demoblaze/settings.md, copy the change here. Do not loosen any rule here to make an eval case run.


## Cookie banner
- banner-title: (none seen on 2026-10-30)
- cookie-button: (none)

## Facts seen before
- (2026-10-30) Demo shop "PRODUCT STORE" by BlazeMeter. Pages: Home (index.html), product pages (prod.html?idp_=N, N = 1 to 15), Cart (cart.html). Contact, About us, Log in and Sign up are popups on the same page.
- (2026-10-30) Log in and Sign up are username/password forms. There is no login link, so LOGGED IN mode is not possible (the agent never types into fields).
- (2026-10-30) The phone header shows the menu already open; the burger button has no visible icon.

## Allowed when LOGGED OUT
- Normal navigation clicks (header, footer, categories, product titles and images, Previous / Next)
- Opening and closing popups (Contact, About us, Log in, Sign up) with "Close", the "×" or Escape, without typing
- Carousel arrows and scrolling

## Login (LOGGED IN mode)
- {TEST_USERNAME} and {TEST_PASSWORD} are placeholders. The real values are in settings.local.md (not in git).
- login method: login-form (allowed by "Allowed to type" below)
- login steps: click "Log in" in the header; type {TEST_USERNAME} into "Username:" and {TEST_PASSWORD} into "Password:" of the "Log in" popup; click "Log in" in the popup.
- logged-in-check: the header shows "Welcome {TEST_USERNAME}" and a "Log out" link, and no "Log in" or "Sign up" links (to be confirmed during exploration)
- after-login-popup: none expected
- session-length: not measured

## Allowed when LOGGED IN
- Everything in "Allowed when LOGGED OUT"
- What the opt-in sections below allow (typing into the Log in form, cart actions, demo checkout)
- "Log out"

## Allowed to type
(Opt-in, see .claude/rules/opt-in.md.)
- status: ON
- approved-by: m.zain, 2026-11-02
- fields:
  - Log in popup, "Username:" = {TEST_USERNAME}
  - Log in popup, "Password:" = {TEST_PASSWORD}
  - Log in popup, "Username:" = no-such-user-12345 (fake, for the "User does not exist." check)
  - Log in popup, "Password:" = wrong-password (fake, for the "Wrong password." and "User does not exist." checks)
- submit-buttons:
  - "Log in" (inside the Log in popup), with the values above or with both fields empty
  - "Sign up" (inside the Sign up popup), only with both fields empty (validation check; nothing is created)
  - "Send message" (inside the Contact popup), only with all fields empty (validation check; approved by m.zain, 2026-11-02)
- Not allowed even when ON: typing anything into the Sign up or Contact fields (that would create an account or send a real message on the shared demo site).
- Needs in settings.local.md: `- TEST_USERNAME: <demo account username>` and `- TEST_PASSWORD: <demo account password>`.

## Allowed cart actions
(Opt-in, see .claude/rules/opt-in.md.)
- status: ON
- site-is-demo: demoblaze.com is BlazeMeter's public practice shop and takes no real payments (confirmed by m.zain, 2026-11-02).
- approved-by: m.zain, 2026-11-02
- buttons:
  - "Add to cart" on product pages
  - "Delete" in the Cart table
- Note: the cart may already contain items from other visitors (seen 2026-10-30). Cart tests must check only the item they added.

## Allowed demo checkout
(Opt-in, see .claude/rules/opt-in.md. Needs "Allowed cart actions" ON as well.)
- status: ON
- site-is-demo: as above.
- approved-by: m.zain, 2026-11-02
- buttons:
  - "Place Order" in the Cart
  - "Purchase" in the order form
- fields (fake values only; check the field names on the live site first, the order form was not opened during exploration):
  - Order form, "Name:" = Test User
  - Order form, "Country:" = Testland
  - Order form, "City:" = Test City
  - Order form, "Credit card:" = 4111 1111 1111 1111 (the standard fake test card number; this demo site does not charge cards)
  - Order form, "Month:" = 01
  - Order form, "Year:" = 2030

## Never
(An opt-in section above with status ON overrides these lines only for exactly what it lists. All three are ON since 2026-11-02.)
- No payment, no purchase, ever: never click a button that shows a real-money price, or Buy, Purchase, Pay, Checkout, Add to cart, a paid Subscribe, or the final button of a flow that leads to payment. On this site that means: never click "Add to cart", "Place Order" or "Purchase".
- Never type into any field. Never enter credentials, personal data or payment details. Never click "Send message", "Log in" (inside the Log in popup) or "Sign up" (inside the Sign up popup).
- Never open external links or download files.

## Skip
- The About us video (do not play it).
- The carousel's current slide (it rotates by itself).
