# Card spending budget (example: copy to spend/budget.md and fill in your own amounts)

spend/budget.md is per tester and ignored by git. Only a PERSON edits it; the agent never changes it.
spend_ledger.py also creates it with USD 0 values the first time it runs. Amounts are in USD.
The budget must be lower than the card's own limit, to leave room for holds and fees.

- card-limit: USD 0
- budget: USD 0
- per-payment-cap: USD 0

card-limit: the limit the bank set on your card (for example USD 50).
budget: the most that may be open at once (paid and not yet refunded, plus holds). Below card-limit.
per-payment-cap: the largest single payment the agent may open a payment window for.
