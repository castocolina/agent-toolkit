# Clarification notes: Customer referral program

Session date: 2026-11-03
Stakeholders: Priya (product manager, requester), marketing team (reward budget)

## Repository facts (inspected)
- Signup flow in `app/signup/page.tsx`; accounts table has no referral columns.
- Stripe is used for subscriptions (`lib/billing/stripe.ts`).

## Round 1 (score 55/100)
Q: What problem does the referral program solve?
A (Priya): Paid acquisition is getting expensive; we want existing customers to bring in new ones.

Q: Who can refer?
A (Priya): Any logged-in customer gets a personal referral link on their account page.

Q: What does the referrer get?
A (Priya): Not decided. Marketing owns the reward amount and hasn't picked one.

Q: How do we stop abuse (self-referral, fake accounts)?
A (Priya): No idea yet.

Still open:
- Reward amount and form (owner: marketing).
- Whether free-plan customers can refer, or only paying ones (owner: Priya).
- Fraud limits (owner: unknown).
- Success measure (owner: Priya; no target given).

Priya, end of round 1: "I know this is thin. Draft the PRD now anyway, marketing needs something to react to on Friday."
