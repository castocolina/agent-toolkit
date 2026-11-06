# Clarification notes: Delete conversations in the shared inbox

Session date: 2026-11-03
Stakeholders: Marco (support lead, requester), Aisha (legal counsel)

## Repository facts (inspected)
- Conversations live in the `conversations` table; there is a soft-delete column `archived_at` but no hard delete.
- Workspace roles: `admin`, `agent`.

## Round 1 (score 45/100)
Q: Who can delete a conversation?
A (Marco): Only workspace admins can permanently delete conversations. Agents can only archive.

Q: Why do you need delete at all?
A (Marco): Customers send passwords and card numbers by mistake and we have to remove them.

## Round 2 (score 70/100)
Q: How long is deleted data kept before it is gone for good?
A (Marco): 90 days, then purge everything.
A (Aisha, by email): Billing conversations must be kept for 7 years for tax audits. No purge for those.

## Round 3 (score 88/100)
Q: Can agents undo a deletion?
A (Marco): No undo after 24 hours. Oh, and any agent should be able to delete conversations they own, otherwise admins become a bottleneck.

Q: Should the customer be notified?
A (Marco): No.
