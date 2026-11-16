---
description: Some things you Probably Are Gonna Need - know when YAGNI doesn't apply because retrofitting is dramatically more expensive than building it in from the start.
---

# PAGNI: Probably Are Gonna Need It

## The Core Insight

> "When should you override YAGNI? When the cost of adding something later is so dramatically expensive compared with the cost of adding it early on that it's worth taking the risk."

The exceptions are things that touch everything when added late, cannot be added retroactively at all, or lose data for good when missing.

## Common PAGNIs

**Data you can't get back:**
- `created_at` / `updated_at` timestamps on every table
- Audit logs (who did what when)
- Many-to-many from the start if there's any hint you'll need more than one

**Infrastructure that's painful to retrofit:**
- API versioning (even if v1 is the only version)
- API pagination (even if lists are small now)
- Logging infrastructure

**Security fundamentals:**
- Session/password invalidation mechanisms
- Safe ways to move redacted data out of production

## The Test

Before invoking PAGNI, ask:
1. **Is retrofitting dramatically more expensive?** (10x+, not 2x)
2. **Is this a known pattern from experience?** (not speculative)
3. **Is the cost of adding it now actually low?** (minutes/hours, not days)

If yes to all three, it's a PAGNI candidate: keep it (or add it) and say why. Otherwise prefer net deletion. When the answers are contested, name the tension and ask the user.

PAGNI is a short list learned from painful experience, not an escape hatch: when in doubt, YAGNI wins.

## External References

- [PAGNIs: Probably Are Gonna Need Its](https://simonwillison.net/2021/Jul/1/pagnis/) - Simon Willison
- [YAGNI Exceptions](https://lukeplant.me.uk/blog/posts/yagni-exceptions/) - Luke Plant
- [Application Security PAGNIs](https://jacobian.org/2021/jul/8/appsec-pagnis/) - Jacob Kaplan-Moss
