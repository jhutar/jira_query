#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from pathlib import Path

from jira_cli.cli import TemplateRenderer, _translate_content


def add_arguments(subparsers):
    parser = subparsers.add_parser(
        "list",
        help="List my issues in current sprint",
    )
    parser.add_argument(
        "--query",
        help="Jira Query Language (JQL) string.",
    )


def run(ctx, args):
    ctx.logger.debug(f"Searching issues: {args.query}")
    issues = ctx.jira.search_issues(args.query, maxResults=False)

    for issue in issues:
        if isinstance(issue.fields.description, dict):
            issue.fields.description = _translate_content(
                "to-md", json.dumps(issue.fields.description)
            )
        if hasattr(issue.fields, "comment") and hasattr(
            issue.fields.comment, "comments"
        ):
            for comment in issue.fields.comment.comments:
                if isinstance(comment.body, dict):
                    comment.body = _translate_content("to-md", json.dumps(comment.body))

    renderer = TemplateRenderer(args.template)
    rendered_output = renderer.render({"issues": issues, "query": args.query})
    print(rendered_output)

    if args.dump:
        output_dir = Path("jira_issue_details")
        output_dir.mkdir(exist_ok=True)
        for issue in issues:
            try:
                issue_data = issue.raw
                file_path = output_dir / f"issue-{issue.key}.json"
                with open(file_path, "w", encoding="utf-8") as fd:
                    json.dump(issue_data, fd, indent=4, sort_keys=False)
                ctx.logger.info(f"Saved details for issue {issue.key} to {file_path}")
            except Exception as e:
                ctx.logger.error(f"Could not save details for issue {issue.key}: {e}")
