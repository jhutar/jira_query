#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), "src"))

from jira_cli.cli import TemplateRenderer
from jira_cli.context import (
    _create_jira_client as JiraClient,
    load_server_config,
)
from jira_cli.report.project_configs import ALL_CATEGORIES, PROJECT_CONFIGS
from jira_cli.report.runner import ReportRunner
from jira_cli.report.time_range import parse_explicit_dates, parse_range
from jira_cli.report.user_resolver import UserResolver


def main():
    parser = argparse.ArgumentParser(
        description="Generate Jira team activity report data for AI summarization.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument(
        "--range",
        default=None,
        dest="time_range",
        help=(
            "Time range: Nd (days), Nw (weeks), Nm (calendar months). "
            "Examples: 7d, 1w, 1m, 3m. Default: 1w"
        ),
    )
    time_group.add_argument(
        "--start",
        default=None,
        help="Start date in YYYY-MM-DD format (requires --end)",
    )

    parser.add_argument(
        "--end",
        default=None,
        help="End date in YYYY-MM-DD format (requires --start)",
    )
    parser.add_argument(
        "--projects",
        nargs="+",
        default=None,
        choices=list(PROJECT_CONFIGS.keys()),
        help="Projects to include (default: all)",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=None,
        choices=ALL_CATEGORIES,
        help="Issue categories to include (default: all)",
    )
    parser.add_argument(
        "--assignees",
        nargs="+",
        default=None,
        metavar="EMAIL",
        help="Filter output to issues assigned to these email addresses",
    )
    parser.add_argument(
        "--template",
        default="templates/detailed-list.md.j2",
        help="Path to Jinja2 template for rendering",
    )

    args = parser.parse_args()

    if args.start and not args.end:
        parser.error("--start requires --end")
    if args.end and not args.start:
        parser.error("--end requires --start")

    if args.start:
        start_date, end_date = parse_explicit_dates(args.start, args.end)
    elif args.time_range:
        start_date, end_date = parse_range(args.time_range)
    else:
        start_date, end_date = parse_range("1w")

    projects = args.projects or list(PROJECT_CONFIGS.keys())
    categories = args.categories or ALL_CATEGORIES

    if not os.path.exists(args.template):
        print(
            f"Error: Template not found at {args.template}.",
            file=sys.stderr,
        )
        sys.exit(1)

    server_conf = load_server_config("~/.jira_query.yaml")
    jira = JiraClient(
        server_conf["url"],
        server_conf["auth"]["basic_auth"]["username"],
        server_conf["auth"]["basic_auth"]["token"],
    )

    resolver = UserResolver(jira)
    renderer = TemplateRenderer(args.template)

    runner = ReportRunner(
        jira=jira,
        user_resolver=resolver,
        renderer=renderer,
        start_date=start_date,
        end_date=end_date,
        projects=projects,
        categories=categories,
        assignee_emails=args.assignees,
    )

    print(runner.run())


if __name__ == "__main__":
    main()
