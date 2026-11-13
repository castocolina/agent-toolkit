# Clarification examples

Read this when writing a first or second clarification response. It holds the two core questions in practice and one worked session in the response format from SKILL.md.

## The two core questions

Ask both before any scoping detail, as product decisions someone owns:

- **Why?** What problem does this solve, and for whom? A requested feature or a technical proposal is not evidence of a need. This is the step 2 question about the problem behind a proposal. Count points for it only once the user states the problem.
- **Simpler?** Would a smaller first version solve the same problem, with the rest deferred? Ask it once, in round 1, as a question about launch scope (a yes/no or a pick between named scopes), never as a design suggestion or an architecture proposal. Log the answer as a decision with its source. What the user defers goes under excluded scope in the PRD, and you add nothing to "later" that they did not name.

Each of the two asks for one decision, like every other question.

## Worked session: "I need a login feature for my app."

The repository was inspected first, so the stack is a logged fact and nobody is asked for it.

### Round 1

```text
I inspected the repository first: a server-rendered web app with a SQL database, a
`users` table with no credential columns, and no sign-in route. The stack is
settled, so I am not asking about it.

Functional 0/30: only a feature name
Technical 12/25: stack and integration points known; security and session policy unstated
Edge cases 0/25: none named
Problem and success 0/20: no stated problem
Advisory score: 12/100

Decisions so far:
- Stack: server-rendered web app with a SQL database (repo: db/schema.sql, app/routes/)

Carried-over open questions: none yet

Next questions:
1. Why: what problem should login solve first: customers cannot see their own
   orders, part of the site must be restricted, or something else?
2. Simpler: is one sign-in method, email with a password, enough for the first
   release, with other methods deferred to a later one?
3. After repeated wrong passwords, what should happen: nothing special, a
   temporary lock, or a password-reset prompt?
```

The user answers: "Customers lose their order history between visits, that is the problem. Yes, email and password only for launch, Google sign-in later. No idea about the wrong passwords, ask me again."

### Round 2

```text
Functional 22/30: behavior and excluded scope stated; failure results unstated
Technical 12/25: unchanged; security and session policy still unstated
Edge cases 0/25: no edge case has an expected behavior yet
Problem and success 10/20: problem and users known; success unmeasured
Advisory score: 44/100

Decisions so far:
- Stack: server-rendered web app with a SQL database (repo: db/schema.sql, app/routes/)
- Problem: customers lose their order history between visits (user, round 1)
- Launch scope: email with a password only; other sign-in methods, starting with
  Google, deferred (user, round 1)

Carried-over open questions:
- After repeated wrong passwords: nothing special, a temporary lock, or a
  password-reset prompt? (asked in round 1, unanswered)

Next questions:
1. Carried over: what should happen after repeated wrong passwords?
2. Must a customer be able to reset a forgotten password at launch?
3. Which measure should show that login is working, or is none defined yet?
```

What the session shows:

- Round 2 scores only what the answers supplied: the Simpler? answer moved Functional from 0 to 22 because it stated excluded scope, and the unanswered wrong-password question earned nothing.
- An unanswered question is carried over each round and counted first among the next questions, because users tend to answer only the newest ones.
- The success measure is asked for, never suggested as a number; any figure in the PRD must come from the user.
- The session stays below 90 and continues; the PRD is generated at 90, or earlier when the user approves a draft.
