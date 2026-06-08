#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import re
import subprocess
import sys

from jira_query import JiraClient, load_server_config, TemplateRenderer


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


# For monthly report, we want the previous month
START = "startOfMonth(-1)"
END = "startOfMonth()"

PROJECTS = {
    ###"Konflux": [
    ###    (
    ###        "Finished issues",
    ###        f"project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status CHANGED TO (Closed, Done) DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In review issues",
    ###        f"project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In progress issues",
    ###        f"project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' DURING ({START}, {END}) OR issuekey IN commented('{START}', '{END}', {format_team(TEAMS['KONFLUX'])}))",
    ###    ),
    ###    (
    ###        "New issues",
    ###        f"project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND created >= {START} AND created < {END} AND assignee is not EMPTY AND status not in (Closed, Done)",
    ###    ),
    ###],
    "Pipelines": [
        (
            "Finished issues",
            f"project = SRVKP AND component = Performance AND status CHANGED TO (Closed, Done) DURING ({START}, {END})",
        ),
        (
            "In review issues",
            f"project = SRVKP AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') DURING ({START}, {END})",
        ),
        (
            "In progress issues",
            f"project = SRVKP AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' DURING ({START}, {END}) OR issuekey IN commented('{START}', '{END}', {format_team(TEAMS['PIPELINES'])}))",
        ),
        (
            "New issues",
            f"project = SRVKP AND component = Performance AND created >= {START} AND created < {END} AND assignee is not EMPTY AND status not in (Closed, Done)",
        ),
    ],
    ###"ConsoleDot": [
    ###    (
    ###        "Finished issues",
    ###        f"project = HCEPERF AND status CHANGED TO (Closed, Done) DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In review issues",
    ###        f"project = HCEPERF AND status in (Review, 'Release Pending') AND status CHANGED TO (Review, 'Release Pending') DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In progress issues",
    ###        f"project = HCEPERF AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' DURING ({START}, {END}) OR issuekey IN commented('{START}', '{END}', {format_team(TEAMS['HCEPERF'])}))",
    ###    ),
    ###    (
    ###        "New issues",
    ###        f"project = HCEPERF AND created >= {START} AND created < {END} AND assignee is not EMPTY AND status not in (Closed, Done)",
    ###    ),
    ###],
    ###"Satellite": [
    ###    (
    ###        "Finished issues",
    ###        f"((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status CHANGED TO (Closed, Done) DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In review issues",
    ###        f"((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status = Review AND status CHANGED TO Review DURING ({START}, {END})",
    ###    ),
    ###    (
    ###        "In progress issues",
    ###        f"((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' DURING ({START}, {END}) OR issuekey IN commented('{START}', '{END}', {format_team(TEAMS['SAT'])}))",
    ###    ),
    ###    (
    ###        "New issues",
    ###        f"((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND created >= {START} AND created < {END} AND assignee is not EMPTY AND status not in (Closed, Done)",
    ###    ),
    ###],
}


def get_pr_info(url):
    try:
        if "github.com" in url:
            cmd = [
                "gh",
                "pr",
                "view",
                url,
                "--json",
                "title,body",
                "--jq",
                '."Title: \\(.title)\\n\\(.body)"',
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        elif "gitlab" in url:
            # Setting GL_HOST to gitlab.cee.redhat.com handles instances for this specific context
            env = os.environ.copy()
            if "gitlab.cee.redhat.com" in url:
                env["GL_HOST"] = "gitlab.cee.redhat.com"
            cmd = ["glab", "mr", "view", url, "-F", "json"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, env=env
            )
            data = json.loads(result.stdout)
            return f"Title: {data.get('title')}\n{data.get('description')}"
    except Exception as e:
        return f"(Failed to fetch PR info: {e})"
    return ""


def enrich_with_prs(text):
    if not text:
        return ""
    # Find PR links
    urls = re.findall(r"https://github.com/[^/\s]+/[^/\s]+/pull/\d+", text)
    urls += re.findall(r"https://gitlab[^\s]*/-/merge_requests/\d+", text)
    urls = list(set(urls))

    enrichment = []
    for url in urls:
        info = get_pr_info(url)
        if info:
            enrichment.append(f"\n--- PR/MR: {url} ---\n{info}")

    return "".join(enrichment)


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

    for project, queries in PROJECTS.items():
        output.append(f"# {project}")
        for title, jql in queries:
            output.append(f"* {title}")
            issues = jira.search_issues(jql)
            rendered = renderer.render({"issues": issues})

            # Enrich the rendered text with PR infos
            pr_info = enrich_with_prs(rendered)
            if pr_info:
                rendered += "\n\n### Linked Pull Requests & Merge Requests\n" + pr_info

            output.append(rendered)
        output.append("\n")

    print("\n".join(output))


if __name__ == "__main__":
    main()
