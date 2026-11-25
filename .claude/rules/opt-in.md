# Opt-in rules

The default safety rules (no typing, no cart, no purchase) apply to every site. A site can loosen them only
through the six sections below in its own `website-tests/<site>/settings.md`. A section that is missing,
or whose `status` is not `ON`, means the default rule applies. All six are OFF for every site until someone
switches them on.

Each section only ever allows what it lists. Anything not listed stays forbidden.

Order of precedence: an opt-in section with status ON overrides the site's "Never" list and the default rules, but only for exactly the fields, values and buttons it lists. A real payment window (for Xsolla: Pay Station) and real payment or personal details are never allowed by sections 1 to 3. The only exceptions are section 4 (the agent types a made-up INVALID card) and section 5 (a person types the card; a real card only if that section says so). The agent never types a real or valid card.

## 1. Allowed to type

Lets tests type into specific fields, for example a login form.

```
## Allowed to type
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- fields:
  - Log in popup, "Username:" = {TEST_USERNAME}
  - Log in popup, "Password:" = {TEST_PASSWORD}
- submit-buttons:
  - "Log in" (inside the Log in popup)
```

Rules:
- Type only into the listed fields, and only the listed value for each field.
- A value is either a placeholder from `settings.local.md` (for example `{TEST_USERNAME}`) or a fake value
  written in the list (for example `test@example.com`, `Test User`). Never real personal data, never real
  payment details.
- Click only the listed submit buttons. Forms that send something to real people (contact or support forms)
  need their submit button listed explicitly and the team's approval in `approved-by`.
- Real usernames and passwords live only in `settings.local.md`, which git ignores. In steps, test cases and
  result JSON, write the placeholder, never the real value. `scrub_secrets.py` removes any real value it finds.
- A browser trace can record typed values, including passwords. Traces stay in `runs/`, which never goes to git.

With this section ON, the Login section of settings.md may use `login method: login-form`, listing the fields
and the submit button above, instead of a login link.

## 2. Allowed cart actions (demo or test sites only)

Lets tests change the cart, for example add an item and remove it again.

```
## Allowed cart actions
- status: OFF
- site-is-demo: <why this site takes no real payments, and who confirmed it>
- approved-by: <name and date>
- buttons:
  - "Add to cart" on product pages
  - "Delete" in the Cart table
```

Rules:
- Only on a site confirmed to be a demo or test site that takes no real payments. Never on a real shop
  (Ludus and every other live Xsolla web shop stay OFF).
- Click only the listed buttons.
- A test that adds or removes items has "Changes account" = Yes, a "(precondition)" question and a "before"
  value, like any other test that changes state. It should leave the cart as it found it (remove what it added).
- "Place Order", "Purchase", "Checkout" and anything that opens a payment window stay forbidden unless
  section 3 is ON.

## 3. Allowed demo checkout (demo sites only, no real payment)

Lets tests go through a fake checkout on a practice site.

```
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
```

Rules:
- Only when section 2 is also ON, and only on a site confirmed to take no real payments.
- Type only the listed fake values. Never a real card number or real personal data.
- Never on a live shop, never in a real payment window (for Xsolla: Pay Station).
- If a real payment window, a real payment provider or a request for real card details appears, stop at once,
  close it, take a screenshot and mark the test FAILED.

## 4. Allowed invalid-card check (live payment window, INVALID card only, nothing can be paid)

Lets `/run-tests <site> payment-invalid` open the real payment window of a live shop and type a made-up INVALID card,
to see what error the window shows. The payment must not be possible.

```
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
```

Rules:
- Only with `/run-tests <site> payment-invalid`, only for payment cases (Sub-type "Payment (skip)"), and only when status is ON and approved-by names a person. A normal `/run-tests` never uses this section.
- Type only the listed INVALID values from `settings.card.local.md` (card, expiry, code and an INVALID email such as one without @). Never a real card, never a valid test card number, never a real email address, never anything from `settings.local.md`.
- **Nothing is captured while the card form is filled** (the Confluence card plan): from the first typed value until the card step ends, take no screenshot and no snapshot, run no screen recording and no trace, and write no typed value anywhere (steps, saw, reason, report). Those steps get an "evidence withheld" image. Read the window's answer with a read-only script that returns only the error messages, never field values.
- Before typing, look at the window: it must be the listed payment window, for the item the case names, with the price the shop showed. If not, close it and stop.
- One attempt per case: click "Pay" once, never retry, never change the values, never try another card or another payment method.
- If the window asks for anything else (a one-time code, 3-D Secure, an email address, a name or an address), do not fill it: close the window and mark the check "unclear".
- If anything looks like the payment went through, do nothing more, screenshot it and tell the reviewer at once.
- The result JSON gets `card_check` (rejected, accepted, window_only or unclear) and `card_error` (the exact error text). These cases are not counted in the pass rate.

Section 4 is the older mode, where the agent types made-up values from `settings.card.local.md`. Payment cases written by `/test-website` now use section 5 (a person types), so use `payment-human` for them.

## 5. Allowed person-typed card check (live payment window, a PERSON types the card)

Lets the payment check at the end of a full `/run-tests` (the payment-human flow) open the real payment window of a live shop, and lets a person type the card and click "Pay" in the open Chrome window. The agent types nothing, never clicks "Pay", never learns the values, and captures nothing while the card form is filled. A REAL card is the normal case: it needs the switch `real: ALLOWED` (written by a person) and really pays. A made-up INVALID card is only an optional rehearsal.

```
## Allowed person-typed card check
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- payment-window: Xsolla Pay Station
- who-types: a person, in the open Chrome window (the agent types nothing and never clicks "Pay")
- items:
  - "<item name>", at most USD <maximum price>
- card-kinds:
  - invalid: ALLOWED
  - real: NOT ALLOWED
- auto-pay: NOT ALLOWED
- max-total-per-run: USD 0
- agent-buttons:
  - the control that closes the payment window
  - "Pay" with the saved card (only with auto-pay: ALLOWED)
- evidence: nothing is captured from the moment the person starts typing until the payment window is closed
```

Rules:
- Only in the payment check (Step 6 of a full `/run-tests`, which runs the payment-human flow), only for payment cases (Sub-type "Payment (skip)"), and only when status is ON and approved-by names a person. A normal `/run-tests` never uses this section. The person writes the approval in `settings.md`, or Step 6 of a full `/run-tests` records their "proceed" as the approval (with the git user name, or the name they type when git has none; never a made-up name).
- **The agent never types in the payment window and never clicks "Pay"** (or any button that pays). The person types the card, expiry, security code and email, and clicks "Pay" once. No tool call, result file, report or message may contain a card value. Nobody pastes card details into the chat.
- Items: only an item listed in `items`, and only if the price the shop shows is not above the listed maximum. Otherwise the agent does not click the price button and the case is BLOCKED.
- Card kinds: `real` is the normal case and needs `real: ALLOWED` (the team's approval in approved-by; only a person writes it, never the agent). `invalid` is an optional rehearsal. Before the first payment window of a run is opened, the coordinator asks the person ONCE to confirm the list of items, each maximum price, the total, and that a real card really pays; that one answer covers every item in the list for that run. The person says which kind they will type; the agent cannot check it.
- **AUTO-PAY with the saved card (only with `auto-pay: ALLOWED`, written by a person, and a `max-total-per-run`):** after the person's first payment SUCCEEDED and the window saved the card, the agent pays the remaining listed items itself: in a hidden Chrome it opens the payment window, reads the item and price with a script that returns only those texts, and clicks "Pay" once with the saved card. It never types, never sees or reads a card field, and takes no screenshot or snapshot of the payment window: the coordinator switches the guard on with `card_guard.py on <RUN> <TC ID> --autopay` before the price click, which blocks all of that and allows only the "Pay" click. The agent stops, pays nothing more and hands the case back to the person if: the item or price differs from the case or is above its maximum; the next payment would take the run above `max-total-per-run`; no saved card is selected ("Pay" disabled, or the window asks for a card number, security code, email, one-time code or 3-D Secure); or the result is unclear. One "Pay" click per case, never a retry.
- **Type once, then the saved card:** in the first card case the person types the card and email and ticks the payment window's own "save card" option if it offers one. The payment provider (for Xsolla: Pay Station) stores it, never the agent and never a file. In the next cases the saved card is already selected: the person only checks it, types what the window asks (for example the security code) and clicks "Pay". The agent still never types, never clicks "Pay" and never sees the card. Delete the saved card from the test account when testing is done.
- Before the handoff the agent looks at the still empty window: it must be the listed payment window, for the item the case names, with the price the shop showed. If not, it closes the window and stops. Then the coordinator switches the card guard on (`card_guard.py on`).
- **Nothing is captured during the card step**, from the guard being switched on until the payment window is closed: no screenshot, snapshot, screen recording or trace, and no script that reads a field value. A Claude Code hook (`card_guard.py hook`, registered in `.claude/settings.json`) refuses screenshots, snapshots, typing and clicks on pay buttons while the guard is on. The hook only loads when Claude Code was started in the project folder, so `/run-tests` tests it before it opens a payment window. The steps of the card step get an "evidence withheld" image. The agent reads the answer with a read-only script that returns only the visible messages.
- **The person touches the payment window only after the coordinator writes "Type the card details in the Chrome window yourself…"** (the guard is on from then). Before that, and in every case that has no "A person" step (window-only), nobody types: a value typed earlier can show up in the agent's screenshots. If that happens, the agent takes no further screenshot, the step gets the "evidence withheld" image, and the coordinator (after asking the person) deletes the cached screenshot files the agent names without opening them.
- **Spend ledger and budget (real card):** every real-card attempt (paid, declined or unclear) is written to the tester's own spend ledger `spend/ledger.csv` with date, site, run, test case, item, amount, status, order or transaction ID and refund status, so it can be refunded later. The tester's budget is in `spend/budget.md`: `card-limit` (the bank's limit), `budget` (must be lower than the card limit) and `per-payment-cap`. Both files are per tester and ignored by git, and only a person writes the budget. Before each real-card payment window is opened, `spend_ledger.py check` must say OK: the item's maximum must not be above the per-payment cap, and the open spend (paid and not yet refunded, unclear, or held by the bank) plus that maximum must stay within the budget. Otherwise the case is not run. A payment counts until its refund is confirmed on the card (`spend_ledger.py set <ID> --refund confirmed`), which only a person decides. Only the coordinator runs `spend_ledger.py`, never the website-tester.
- One attempt per case: the person clicks "Pay" once. No retry, no other card, no other payment method. If the window asks for something else (a one-time code, 3-D Secure, a name, an address), the agent does not fill it: it writes what the window asked as `card_error`, uses `unclear` and closes the window.
- **"Pay" stays disabled:** the payment window checks the card while it is typed, so with an invalid card "Pay" often cannot be clicked. The person then answers "Pay stayed disabled (error shown)". The agent reads only the visible error messages, and the result is `rejected` with `card_error` "<message> (shown while typing; Pay stayed disabled)". This is the expected, correct result for an invalid card.
- **The window closes by itself after "Pay":** with an invalid card Pay Station may close right after "Pay" without a readable message, so the agent finds no window to read. The person answers "Clicked Pay, then the window closed by itself" and says whether they saw a message. With an error message the result is `rejected` (the message, reported by the person); without one it is `window_closed` (a refused card should show an error: the reviewer decides whether that is a bug).
- **Only the coordinator switches the card guard on and off** (`card_guard.py on` before the handoff, `card_guard.py off` once the window is confirmed closed). The website-tester never runs `card_guard.py`: it reads and closes the window with the guard on (Phase B), and takes the store-page screenshots after the coordinator switched it off (Phase C).
- If the person does not type, the case stays open and nothing happens. The person can answer "Skip" (the agent closes the window, nothing is paid, `skipped`) or "The window expired" (`timeout`).
- If a payment looks as if it went through after the person said they typed an `invalid` card, the agent does nothing more, screenshots only the store page after the window is closed, and the coordinator tells the reviewer at once.
- The result JSON gets `card_check` (rejected, accepted, paid, window_only, window_closed, skipped, timeout or unclear), `card_kind` (invalid, real or none, as told by the person) and `card_error` (the exact visible message, never a typed value). For a real card that was paid: `card_check` "paid" and `account_changes`. **A real-card case is a normal test:** PASSED only when the payment succeeded, FAILED when the card was declined or anything else happened, and counted in the pass rate. Invalid-card, window-only and login-prompt checks are not counted in the pass rate.

## 6. Allowed logged-out price click (login prompt only)

Lets the payment check click a real-money price button while LOGGED OUT, only to see that the shop asks the visitor to
log in and opens no payment window. One price button per store section. Nothing can be paid: a logged-out visitor has
no account to pay with.

```
## Allowed logged-out price click
- status: OFF
- approved-by: <name of the person who approved it, and the date>
- mode: LOGGED OUT only (fresh session, no login link)
- buttons:
  - the real-money price button named in the case (once)
  - the control that closes the login prompt
```

Rules:
- Only in the payment check (the payment-human flow), only for cases with Sub-type "Payment login prompt (skip)", only in
  LOGGED OUT mode, and only when status is ON and approved-by names a person. A normal `/run-tests` never uses it.
  Step 6 of a full `/run-tests` records the person's "proceed" as the approval, the same way as for section 5.
- Click the named price button once. A login prompt is any dialog that asks the visitor to log in or sign in (for
  example "LOG IN TO MAKE PURCHASES" with a QR code, or a gift dialog with a "Sign in" button). Inside it, click nothing
  except its close control: never log in, never sign in, never type.
- If a payment window (for Xsolla: Pay Station) opens instead of a login prompt, touch nothing inside it, close it at once
  with its closing control, take a screenshot after it is closed and mark the test FAILED.
- The result JSON gets `card_check` ("login_prompt" when the shop asked to log in, "window_opened" when a payment window
  opened), `card_kind` "none" and `card_error` (the prompt's visible text). These cases are not counted in the pass rate.

## How the commands use these sections

- `/test-website` reads the sections in Step 1, may write test steps that use exactly what they allow, and
  lists every such step in its review summary (Step 5).
- `/run-tests` passes the sections to the website-tester and, in its safety check, refuses any step that types,
  changes the cart or checks out without a matching ON section. `/run-tests <site> payment-invalid` also needs section 4,
  and the payment check at the end of a full run needs section 5 (and section 6 for its "Payment login prompt" cases).
- `website-tester` follows its default rules and allows an exception only when the matching section is ON
  and lists that exact field, value or button.
