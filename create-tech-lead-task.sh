#!/bin/sh
#
# Create a recurring "Tech Lead duties" task under a parent epic.
#
# Usage:
#   ./create-tech-lead-task.sh KONFLUX-1234 "Deploy Python pipeline probe to kflux-lw-p01 cluster"

set -eu

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <epic-id> <project-name>" >&2
    echo "Example: $0 KONFLUX-1234 'Deploy Python pipeline probe to kflux-lw-p01 cluster'" >&2
    exit 1
fi

EPIC="$1"
PROJECT_NAME="$2"

# Project key is the part of the epic ID before the dash (e.g. KONFLUX-1234 -> KONFLUX)
PROJECT_KEY="${EPIC%%-*}"

SUMMARY="Tech Lead duties for '$PROJECT_NAME' (reviews, direction, unblocking)"

DESCRIPTION="Summary:
Recurring technical leadership activities for project '$PROJECT_NAME' tracked in epic $EPIC.

Scope:
- Architecture and direction discussions with the team
- Code and PR reviews
- Consultation on design decisions, trade-offs, and priorities
- Helping remove blockers and aligning with other teams
- Spreading context (roadmap, constraints, decisions) across the team

Out of scope:
- Hands-on implementation work (tracked in separate tickets)

Expected outcome:
Team can make sound technical decisions faster and stays aligned
with overall direction."

jira-cli create \
    --project "$PROJECT_KEY" \
    --summary "$SUMMARY" \
    --description "$DESCRIPTION" \
    --assignee "jhutar@redhat.com" \
    --type Task \
    --story-points 2 \
    --epic "$EPIC"
