# Opt-in rules

The default safety rules (no typing, no cart, no purchase) apply to every site. A site can loosen them only
through the three sections below in its own `website-tests/<site>/settings.md`. A section that is missing,
or whose `status` is not `ON`, means the default rule applies. All three are OFF for every site until someone
switches them on.

Each section only ever allows what it lists. Anything not listed stays forbidden.

Order of precedence: an opt-in section with status ON overrides the site's "Never" list and the default rules, but only for exactly the fields, values and buttons it lists. A real payment window (for Xsolla: Pay Station) and real payment or personal details are never allowed by any section.

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

## How the commands use these sections

- `/test-website` reads the sections in Step 1, may write test steps that use exactly what they allow, and
  lists every such step in its review summary (Step 5).
- `/run-tests` passes the sections to the website-tester and, in its safety check, refuses any step that types,
  changes the cart or checks out without a matching ON section.
- `website-tester` follows its default rules and allows an exception only when the matching section is ON
  and lists that exact field, value or button.
