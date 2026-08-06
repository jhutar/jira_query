# Perf & Scale Quarterly Review for Pipelines
## Top of Mind
* Completed Chains & Pipelines Controller CPT scenario coverage (HA, QBT, nightly).
* Delivered 1.22 regression testing epic; published KB article and blog.
* Redesigned CI cron schedule, cutting concurrency ~3x within Boskos limits.

## Risks/Concerns
* Job-management MR blocked: bot lacks admin access on performance repo.
* Ford's PipelineRun count discrepancy investigation stalled with no updates.
* ResolutionRequest duration metric unreliable — causes false regression alarms.

## Coming up
* Results Controller CPT scenario coverage (new backlog epic).
* Resolver performance regression testing: Pipelines 1.22 vs 1.23.
* Iterate CPT report-generation pipeline and LLM prompt templates.

## Collaboration Opportunities
* Presented 1.21/1.22 regression findings to Engineering team.
* Investigating PipelineRun metrics discrepancy for Ford/console-dashboard team.
* Reused RHDH team's Prow PR-branch-trigger pattern (via Pavel Macik).
