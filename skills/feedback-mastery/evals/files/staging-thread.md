# #release-staging, Tue Oct 20 - Thu Oct 22 (excerpt)

**Wed 09:12 Ravi (QA lead):** staging has been 500ing since yesterday afternoon, is someone on this?
**Wed 09:40 Ana (backend):** we assumed QA owns staging deploys after the env split?
**Wed 10:05 Ravi:** no, QA only runs the suites. deploys were always yours
**Thu 11:30 Ana:** found it, a failed migration from Tuesday's deploy. fixed and redeployed
**Thu 11:32 Ravi:** ok. that's two days of regression runs lost again
