#!/bin/sh
#
# Create three "Probe results investigation" tasks (Mon/Wed/Fri) for the
# current week, one per assignee.

set -eu

DESCRIPTION=$(cat <<'EOF'
Goal of this task is to regularly ensure our Konflux Probe runs are running
fine, errors are recognized and reported if it makes sense.

We have the docs and tools, so you can leverage AI agents (tested with Claude Code and Gemini).

* Main docs on probe runs: <https://docs.google.com/document/d/1lIWwBXeBxlyHkucNJu__NrAsPtRMgoPGjf_0EbHUhcs/edit?tab=t.0>
* Overview video on probe runs: <https://drive.google.com/file/d/1yh3bIlIxl-ITXiT6Tb4844toyNH5HhoG/view?usp=sharing>
* Recording of a review process: <https://drive.google.com/file/d/1ZNZOhqAVlP-gf_wCHNrQB7AiTeLRH_wp/view?usp=sharing>

h2. Acceptance criteria

* Review probe runs status and report/update issues that were noticed
  * Check Jenkins jobs are running fine (see <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/jenkins-stability-runbook.md>)
  * Check performance degradations and overall system health (see <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/system-health-check.md>)
* Categorize new errors and raise a PR with new error patterns and tests for them and get it merged
  * Categorizing unknown errors (see <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/categorize-unknown-errors.md>)
  * Adding new rule to recognize unknown error (see <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/add-new-rule.md>)
* Let the team know how it went
  * If there is something consistently wrong with Konflux or the cluster itself, consider reporting it to Jira as a bug (see <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/report-konflux-bug-by-probe.md> or <https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/howtos/report-issue-to-jira.md>, these procedures were not tested too much yet with AI agents, so be cautious)
  * Share the summary of what you did with the team on the Slack
EOF
)

jira-cli create --project KONFLUX --summary "Probe results investigation, Mon, week of $(date -I)" --assignee "jhutar@redhat.com" --components Performance --status "In Progress" --type Task --story-points 1 --sprint-current --description "$DESCRIPTION" --epic KONFLUX-14182
jira-cli create --project KONFLUX --summary "Probe results investigation, Wed, week of $(date -I)" --assignee "cmusali@redhat.com" --components Performance --status "New" --type Task --story-points 1 --sprint-current --description "$DESCRIPTION" --epic KONFLUX-14182
jira-cli create --project KONFLUX --summary "Probe results investigation, Fri, week of $(date -I)" --assignee "smodak@redhat.com" --components Performance --status "New" --type Task --story-points 1 --sprint-current --description "$DESCRIPTION" --epic KONFLUX-14182
