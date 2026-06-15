#!/bin/sh

set -eu

./jira-cli.py create --project KONFLUX --summary "Probe results investigation, Mon, week of $(date -I)" --assignee "jhutar@redhat.com" --components Performance --status "In Progress" --type Task --story-points 1 --sprint-current --description @description-probe-errors-check.md --epic KONFLUX-14182
./jira-cli.py create --project KONFLUX --summary "Probe results investigation, Wed, week of $(date -I)" --assignee "cmusali@redhat.com" --components Performance --status "New" --type Task --story-points 1 --sprint-current --description @description-probe-errors-check.md --epic KONFLUX-14182
./jira-cli.py create --project KONFLUX --summary "Probe results investigation, Fri, week of $(date -I)" --assignee "smodak@redhat.com" --components Performance --status "New" --type Task --story-points 1 --sprint-current --description @description-probe-errors-check.md --epic KONFLUX-14182
