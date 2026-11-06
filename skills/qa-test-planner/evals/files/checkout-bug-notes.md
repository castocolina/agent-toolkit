Support ticket #5521, forwarded by the support lead:

> Customer says the Pay button "does nothing" on the checkout page. She clicked it
> several times. Later the order showed up twice in her account and she was charged
> twice. She did not say which browser or phone she used.

QA notes:
- I tried 10 times on staging build 2.4.0-rc2 and saw a double order 2 times.
- Steps I used: add one item to the cart, go to checkout, click Pay twice quickly.
- Expected: one order and one charge. Actual: in 2 of 10 attempts, two orders and two charges.
- I have not checked the console.

Please save this as a bug report file in ./bugs using the bundled script.
