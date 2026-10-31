# hierarchy

## Why one filled button and not two

Apple HIG Buttons allows one or two prominent buttons per view and says to mark the most likely action with style, not size. NN/g, Visual Hierarchy: "If everything is contrasted, then nothing stands out." HIG's second prominent slot is the one exception, and this skill spends it on an outlined button: the alternative stays visible while the eye still lands on one place.

## Worked calls

| view | buttons | verdict |
|------|---------|---------|
| Checkout | Pay now filled, Pay on invoice outlined, Apply code text | pass: same job, likelier one filled |
| Checkout | Pay now filled, Pay on invoice filled | fail: second filled button, even for the same job |
| Editor | Save (the form submit) and Save and close, equally likely | pass when Save, the button Enter triggers, is filled and Save and close outlined |
| Settings | Save, Export, Delete workspace all filled | fail: three filled; fix to Save filled, Export text, Delete workspace text with the danger role |
| Delete confirmation dialog | Cancel text, Delete outlined with the danger role | pass: no button needs to be filled, and a filled destructive button invites the reflex press |
| Editor with an open dialog | Publish filled on the page, Confirm filled in the dialog | pass: the dialog is its own view |
| Product grid | Add to cart filled on every card | fail: one filled per card is N primaries; make it outlined or text |
| Orders list | icon-only Delete per row, no filled button | pass: zero filled is within "at most one" |

```tsx
<Stack direction="row" spacing={1}>
  <Button variant="contained">Pay now</Button>
  <Button variant="outlined">Pay on invoice</Button>
  <Button variant="text">Apply code</Button>
</Stack>
```

## Judgment aids (never a fail line)

Use these to improve a screen, not to fail it:

- NN/g, for complex designs: about 3 type sizes, about 3 contrast treatments, about 2 large elements.
- Squint test: blurred, the primary action and the page title still stand out.
- Group by proximity first; add a border or background only when spacing does not separate the groups.
- Delete filler copy ("Welcome to your dashboard") and repeated "Overview" headings.

## Gotchas

- Color alone does not mark priority or status: pair it with weight, an icon or text (NN/g). A red text button reads as destructive only to people who see red.
- A MUI `Button` with no `variant` is `text`, so it never counts as filled; a custom `.btn` with a background color does.
