#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json

from jira_cli.cli import (
    _editor,
    _pretty,
    _translate_content,
    assign_issue,
    resolve_assignee,
    update_fields,
    update_status,
)


def add_arguments(subparsers):
    parser = subparsers.add_parser(
        "update",
        help="Update a ticket(s)",
    )
    parser.add_argument(
        "--issue",
        help="Ticket (or coma separated list of tickets) to update (or use --query)",
    )
    parser.add_argument(
        "--query",
        help="Jira Query Language (JQL) query to list issues to update (or use --issue)",
    )
    parser.add_argument(
        "--assignee",
        help="Reassign the ticket to this user (name, email, or accountId)",
    )
    parser.add_argument(
        "--status",
        help="New state of the ticket",
    )
    parser.add_argument(
        "--resolution",
        help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
    )
    parser.add_argument(
        "--comment",
        help="New comment to add in Markdown format (or set to '' to edit with editor), if it starts with '@' it is considered a file to load it from",
    )
    parser.add_argument(
        "--description",
        help="New description text in Markdown format (or set to '' to edit with editor), if it starts with '@' it is considered a file to load it from",
    )
    parser.add_argument(
        "--epic",
        help="Parent epic to put this ticket under",
    )
    parser.add_argument(
        "--parent",
        help="Parent issue key to link this issue under (unifies Epic Link, Parent Link, and Sub-task parents)",
    )
    parser.add_argument(
        "--story-points",
        type=float,
        help="How many story points to set",
    )
    parser.add_argument(
        "--team",
        help="Assigned team (e.g. 'lightwell-performance')",
    )
    parser.add_argument(
        "--sprint",
        help="Add to this sprint",
    )
    parser.add_argument(
        "--sprint-regexp",
        help="Add to active sprint whose name matches this regexp",
    )
    parser.add_argument(
        "--sprint-current",
        action="store_true",
        help="Add to current sprint",
    )
    parser.add_argument(
        "--target-start",
        type=lambda d: __import__("datetime").datetime.strptime(d, "%Y-%m-%d"),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--target-end",
        type=lambda d: __import__("datetime").datetime.strptime(d, "%Y-%m-%d"),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--add-labels",
        action="append",
        help="Label to add (can be specified multiple times)",
    )
    parser.add_argument(
        "--remove-labels",
        action="append",
        help="Label to remove (can be specified multiple times)",
    )
    parser.add_argument(
        "--link-relationship",
        help="Link relationship type (e.g. 'is blocked by', 'blocks', 'relates to')",
    )
    parser.add_argument(
        "--link-target",
        help="Issue key to link to (requires --link-relationship)",
    )


def run(ctx, args):
    if args.issue is not None:
        issues = []
        for i in args.issue.split(","):
            i = i.strip()
            ctx.logger.debug(f"Loading issue: {i}")
            issues.append(ctx.jira.issue(i))
    elif args.query is not None:
        ctx.logger.debug(f"Searching issues: {args.query}")
        issues = ctx.jira.search_issues(args.query, maxResults=False)
    else:
        raise Exception("Neither --issue nor --query provided")

    if args.comment is not None:
        if args.comment == "":
            args.comment = _editor()
        elif args.comment.startswith("@"):
            args.comment = open(args.comment[1:], "r").read()
        else:
            args.comment = args.comment.replace(r"\n", "\n").replace(r"\t", "\t")

    if args.description is not None:
        if args.description == "":
            args.description = _editor()
        elif args.description.startswith("@"):
            args.description = open(args.description[1:], "r").read()
        else:
            args.description = args.description.replace(r"\n", "\n").replace(
                r"\t", "\t"
            )

    assert not (args.parent is not None and args.epic is not None), (
        "Cannot specify both --parent and --epic; use --parent for unified hierarchy linking"
    )
    assert (args.link_relationship is None) == (args.link_target is None), (
        "--link-relationship and --link-target must be specified together"
    )

    if args.parent is not None:
        try:
            ctx.logger.debug(f"Pre-validating parent: {args.parent}")
            ctx.jira.issue(args.parent, fields="issuetype")
        except Exception as e:
            raise AssertionError(
                f"Parent issue '{args.parent}' not found or inaccessible: {e}"
            )

    resolved_assignee = None
    if args.assignee is not None:
        resolved_assignee = resolve_assignee(ctx, args.assignee)
        ctx.logger.debug(f"Pre-validated assignee: {resolved_assignee}")

    for issue in issues:
        update_status(ctx, args, issue)

        if args.comment is not None:
            if args.dry_run:
                _pretty("Would add this comment:", args.comment)
            else:
                adf_comment = json.loads(_translate_content("to-adf", args.comment))
                ctx.jira.add_comment(issue, adf_comment)
                print(f"Commented on the issue {issue.id}")

        if args.description is not None:
            if args.dry_run:
                _pretty("Would set this description:", args.description)
            else:
                adf_description = json.loads(
                    _translate_content("to-adf", args.description)
                )
                issue.update(fields={"description": adf_description})
                print(f"Updated description on the issue {issue.id}")

        update_fields(ctx, args, issue)

        if resolved_assignee is not None:
            assign_issue(ctx, args, issue, resolved_assignee)

        if args.link_relationship is not None:
            if args.dry_run:
                _pretty(
                    f"Would link issue '{args.link_relationship}' to {args.link_target}"
                )
            else:
                ctx.jira.create_issue_link(
                    args.link_relationship, issue.key, args.link_target
                )
                print(f"Linked '{args.link_relationship}' to {args.link_target}")
