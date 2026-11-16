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
| Product grid | Add to cart filled on every card, rendered from one product list, no recommended item, nothing else filled | pass: equal-priority independent product choices (the exception in SKILL.md); cite the list map in the evidence |
| Product grid | Add to cart filled on every card, plus a filled Checkout in the header | fail: the header fill competes with the cards; make Checkout outlined or the cards outlined |
| Orders list | Edit filled on every order row | fail: one task repeated per record is N primaries, not product choices; make it text |
| Auth page | Sign in filled in the sign-in panel, Create account filled in the separate sign-up panel | pass: two bounded panels, each an independent task, are two views |
| Admin app whose design system says "one filled button per toolbar" | two toolbars, one filled each | pass: the documented rule wins; cite the design-system page in the evidence |
| Orders list | icon-only Delete per row, no filled button | pass: zero filled is within "at most one" |

## Judgment aids (never a fail line)

Use these to improve a screen, not to fail it:

- NN/g, for complex designs: about 3 type sizes, about 3 contrast treatments, about 2 large elements.
- Squint test: blurred, the primary action and the page title still stand out.
- Group by proximity first; add a border or background only when spacing does not separate the groups.
- Delete filler copy ("Welcome to your dashboard") and repeated "Overview" headings.

## Gotchas

- Color alone does not mark priority or status: pair it with weight, an icon or text (NN/g). A red text button reads as destructive only to people who see red.
