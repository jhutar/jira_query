#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import os
import sys

from jira_cli.cli import (
    _create_jira_client as JiraClient,
    load_config as load_server_config,
    TemplateRenderer,
)
from pr_utils import enrich_issue_with_prs


# Configure queries from the shell script
TEAMS = {
    "KONFLUX": [
        "5a78c7f73297605c78217f31",
        "712020:4f482a8c-9a94-461a-bd49-3776613160f7",
        "712020:ae13c278-02f4-439e-95b2-baa3d2e50049",
        "5c6d765aca97144c4716967d",
    ],
    "PIPELINES": [
        "rh-ee-sira",
        "rh-ee-dbamandl",
        "557058:3a905916-e478-4e89-be3c-51726725d067",
        "5a78c7f73297605c78217f31",
    ],
    "HCEPERF": [
        "712020:db9a305a-b86c-4c0e-aa67-5d303b654855",
        "712020:742fe929-2f70-4ced-ad2f-464a9ba181a7",
        "712020:a9feda78-c87b-49c5-a0e9-ab848545eac0",
        "712020:d528a513-118b-4b0a-bb87-71e1dddc40db",
        "712020:30a67e72-e47d-4a3a-a43d-5e8ff330f707",
        "70121:2d46d1a6-e85d-4221-b1de-03ce32638494",
        "712020:1117cd10-1326-4e0e-841e-a6a13ff6f8b3",
        "557058:3a905916-e478-4e89-be3c-51726725d067",
        "5a78c7f73297605c78217f31",
    ],
    "SAT": [
        "557058:3a905916-e478-4e89-be3c-51726725d067",
        "rhn-engineering-pablomh",
        "70121:843ee2a6-4309-44bf-8ff5-75c4dd1ada07",
        "5a78c7f73297605c78217f31",
    ],
}


def format_team(team_list):
    return ", ".join(team_list)


PROJECTS = {
    "Konflux": [
        (
            "Finished issues",
            "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status CHANGED TO (Closed, Done) AFTER -7d",
        ),
        (
            "In review issues",
            "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') AFTER -7d",
        ),
        (
            "In progress issues",
            f"project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', {format_team(TEAMS['KONFLUX'])}))",
        ),
        (
            "New issues",
            "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)",
        ),
    ],
    "Pipelines": [
        (
            "Finished issues",
            "project = SRVKP AND component = Performance AND status CHANGED TO (Closed, Done) AFTER -7d",
        ),
        (
            "In review issues",
            "project = SRVKP AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') AFTER -7d",
        ),
        (
            "In progress issues",
            f"project = SRVKP AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', {format_team(TEAMS['PIPELINES'])}))",
        ),
        (
            "New issues",
            "project = SRVKP AND component = Performance AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)",
        ),
    ],
    "ConsoleDot": [
        (
            "Finished issues",
            "project = HCEPERF AND status CHANGED TO (Closed, Done) AFTER -7d",
        ),
        (
            "In review issues",
            "project = HCEPERF AND status in (Review, 'Release Pending') AND status CHANGED TO (Review, 'Release Pending') AFTER -7d",
        ),
        (
            "In progress issues",
            f"project = HCEPERF AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', {format_team(TEAMS['HCEPERF'])}))",
        ),
        (
            "New issues",
            "project = HCEPERF AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)",
        ),
    ],
    "Satellite": [
        (
            "Finished issues",
            "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status CHANGED TO (Closed, Done) AFTER -7d",
        ),
        (
            "In review issues",
            "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status = Review AND status CHANGED TO Review AFTER -7d",
        ),
        (
            "In progress issues",
            f"((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', {format_team(TEAMS['SAT'])}))",
        ),
        (
            "New issues",
            "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)",
        ),
    ],
}


def main():
    server_conf = load_server_config("~/.jira_query.yaml")
    jira = JiraClient(
        server_conf["url"],
        server_conf["auth"]["basic_auth"]["username"],
        server_conf["auth"]["basic_auth"]["token"],
    )

    template_path = "templates/detailed-list.md.j2"

    # Check if we are running from the correct directory
    if not os.path.exists(template_path):
        print(
            f"Error: Template not found at {template_path}. Please run from the jira_query directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    renderer = TemplateRenderer(template_path)

    output = []

    # Threshold for filtering comments (last 7 days)
    # Jira dates are ISO strings, so we can use string comparison
    since_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
        "%Y-%m-%d"
    )

    for project, queries in PROJECTS.items():
        output.append(f"# {project}")
        for title, jql in queries:
            output.append(f"## {title}")
            issues = jira.search_issues(jql)

            for issue in issues:
                enrich_issue_with_prs(issue)
                # Filter comments to only include those from the last 7 days
                if hasattr(issue.fields, "comment") and issue.fields.comment:
                    issue.fields.comment.comments = [
                        c
                        for c in issue.fields.comment.comments
                        if c.created >= since_date
                    ]

            rendered = renderer.render({"issues": issues})
            output.append(rendered)
        output.append("\n")

    print("\n".join(output))


if __name__ == "__main__":
    main()
