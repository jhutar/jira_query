#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from pathlib import Path

from jira_cli.cli import _translate_content
from jira_cli.pr_utils import enrich_with_prs


def add_arguments(subparsers):
    parser = subparsers.add_parser(
        "view",
        help="View details of a specific issue",
    )
    parser.add_argument(
        "issue_key",
        help="The Jira issue key to view (e.g., 'KONFLUX-123')",
        type=str,
    )
    parser.add_argument(
        "--with-comments",
        action="store_true",
        help="Include issue comments in the output",
    )
    parser.add_argument(
        "--with-enrichment",
        action="store_true",
        help="Fetch and display linked PR/commit/Slack details from GitHub/GitLab/Slack",
    )
    parser.add_argument(
        "--with-diff",
        action="store_true",
        help="Include diffs from PRs/commits in enrichment output (implies --with-enrichment, truncated to 200 lines)",
    )


def run(ctx, args):
    ctx.logger.debug(f"Fetching issue: {args.issue_key}")
    issue = ctx.jira.issue(args.issue_key)

    key = issue.key
    summary = getattr(issue.fields, "summary", "N/A")

    issue_type = "N/A"
    if hasattr(issue.fields, "issuetype") and issue.fields.issuetype:
        issue_type = getattr(issue.fields.issuetype, "name", "N/A")

    status = "N/A"
    if hasattr(issue.fields, "status") and issue.fields.status:
        status = getattr(issue.fields.status, "name", "N/A")

    assignee = "Unassigned"
    if hasattr(issue.fields, "assignee") and issue.fields.assignee:
        name = getattr(issue.fields.assignee, "displayName", "N/A")
        email = getattr(issue.fields.assignee, "emailAddress", "")
        assignee = f"{name} ({email})" if email else name

    reporter = "N/A"
    if hasattr(issue.fields, "reporter") and issue.fields.reporter:
        reporter = getattr(issue.fields.reporter, "displayName", "N/A")

    priority = "N/A"
    if hasattr(issue.fields, "priority") and issue.fields.priority:
        priority = getattr(issue.fields.priority, "name", "N/A")

    story_points = None
    custom_fields = ctx.config.get("custom_fields", {})
    if "story_points" in custom_fields:
        story_points = getattr(issue.fields, custom_fields["story_points"], None)

    sprint_name = None
    if "sprint" in custom_fields:
        sprint_value = getattr(issue.fields, custom_fields["sprint"], None)
        if sprint_value:
            if isinstance(sprint_value, list) and len(sprint_value) > 0:
                last = sprint_value[-1]
                if hasattr(last, "name"):
                    sprint_name = last.name
                elif isinstance(last, dict):
                    sprint_name = last.get("name")
                else:
                    sprint_name = str(last)
            elif hasattr(sprint_value, "name"):
                sprint_name = sprint_value.name
            elif isinstance(sprint_value, str):
                sprint_name = sprint_value

    parent_key = None
    if hasattr(issue.fields, "parent") and issue.fields.parent:
        parent_key = getattr(issue.fields.parent, "key", None)

    raw_desc = issue.raw.get("fields", {}).get("description")
    if raw_desc and isinstance(raw_desc, dict):
        description = _translate_content("to-md", json.dumps(raw_desc))
    else:
        description = getattr(issue.fields, "description", None) or "No description"

    comments = []
    if args.with_comments:
        raw_comments_list = (
            issue.raw.get("fields", {}).get("comment", {}).get("comments", [])
        )
        if hasattr(issue.fields, "comment") and hasattr(
            issue.fields.comment, "comments"
        ):
            for idx, comment in enumerate(issue.fields.comment.comments):
                author = getattr(comment, "author", None)
                author_name = (
                    getattr(author, "displayName", "Unknown") if author else "Unknown"
                )
                created = getattr(comment, "created", "")
                raw_body = (
                    raw_comments_list[idx].get("body")
                    if idx < len(raw_comments_list)
                    else None
                )
                if raw_body and isinstance(raw_body, dict):
                    body = _translate_content("to-md", json.dumps(raw_body))
                elif isinstance(comment.body, str):
                    body = comment.body
                else:
                    body = str(comment.body)
                comments.append(
                    {"author": author_name, "created": created, "body": body or ""}
                )

    separator = "=" * 80
    thin_sep = "-" * 80

    print(separator)

    line1_parts = [f"[{key}]", f"Status: {status}", f"Type: {issue_type}"]
    if story_points is not None:
        line1_parts.append(f"Points: {story_points}")
    print("   ".join(line1_parts))

    print(f"Summary:   {summary}")
    print(f"Assignee:  {assignee}")
    print(f"Reporter:  {reporter}")
    print(f"Priority:  {priority}")

    if sprint_name:
        print(f"Sprint:    {sprint_name}")
    if parent_key:
        print(f"Parent:    {parent_key}")

    print(thin_sep)
    print("Description:")
    print(description)

    if comments:
        print(thin_sep)
        print("Comments:")
        for c in comments:
            print(f"- {c['author']} ({c['created']}):")
            for line in c["body"].splitlines():
                print(f"    {line}")

    if args.with_diff:
        args.with_enrichment = True

    if args.with_enrichment:
        texts = [description]
        for c in comments:
            texts.append(c["body"])
        enrichment = enrich_with_prs("\n".join(texts), with_diff=args.with_diff)
        if enrichment:
            print(thin_sep)
            print("Enrichment:")
            for item in enrichment:
                print(f"- URL: {item['url']}:")
                for line in item["info"].splitlines():
                    print(f"    {line}")

    print(separator)

    if args.dump:
        output_dir = Path("jira_issue_details")
        output_dir.mkdir(exist_ok=True)
        try:
            issue_data = issue.raw
            file_path = output_dir / f"issue-{issue.key}.json"
            with open(file_path, "w", encoding="utf-8") as fd:
                json.dump(issue_data, fd, indent=4, sort_keys=False)
            ctx.logger.info(f"Saved details for issue {issue.key} to {file_path}")
        except Exception as e:
            ctx.logger.error(f"Could not save details for issue {issue.key}: {e}")
