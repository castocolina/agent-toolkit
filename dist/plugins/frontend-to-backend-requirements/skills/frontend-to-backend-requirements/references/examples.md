# Writing a need with context

Each need in the document states what the user sees or does (the purpose) and one sentence on where it sits in the product (the context). Backend uses the context to pick a better approach; a bare data request gives it nothing to design against. Neither version names an endpoint, a method or a field.

## Vague request (no context)

> "I need contract data."

Backend cannot tell which screen, how many items, in what order, or what the user does next.

## Contextual request

> **Purpose:** show the most recent contracts at a glance.
> **Context:** on the dashboard, there's a "Recent Contracts" widget showing the 5 most recent contracts. User clicks one to go to the detail page.

From this, backend can see that the widget needs a short, recency-ordered list and that each item must lead to one contract's detail. Write the open parts as questions or uncertainties (for example, what "recent" means: created or last changed; what the widget shows when there are no contracts), and invite pushback as the template's Collaboration note describes.
