Pasted from our team chat, Dana (release captain for the `@acme/widgets` npm package):

ok so this is how I cut a release by hand, roughly:

1. get on main and make sure it's current: `git checkout main` then `git pull --ff-only`
2. `git status` has to be clean, otherwise I stop and find out whose stuff that is
3. `npm test` - if anything fails there is no release, period
4. bump the version: `npm version patch` (or `minor` / `major`, that's always my call). this also makes the commit and the `vX.Y.Z` tag
5. `git push origin main --follow-tags`
6. `npm publish --access public`
7. post the new version and the changelog link in #releases on Slack

stuff that goes wrong:
- step 6 times out maybe one time in five and then I never know whether it went out. once I re-ran it and got "You cannot publish over the previously published versions", another time it really had not gone out
- I once ran the whole thing from a feature branch by accident
- only release captains are supposed to publish, and people keep asking the bot to "just ship it"
