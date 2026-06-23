#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json

from jira_cli.cli import _editor, _pretty, _translate_content
from jira_cli.parent_resolver import resolve_parent_field
from jira_cli.sprint_resolver import SprintResolver


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
        "--status",
        help="New state of the ticket",
    )
    parser.add_argument(
        "--resolution",
        help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
    )
    parser.add_argument(
        "--comment",
        help="New comment to add in Markdown format (or set to '' to edit with editor)",
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
        "--labels",
        action="append",
        help='Label to add (can be specified multiple times, set to "" to ignore)',
    )
    parser.add_argument(
        "--link-relationship",
        help="Link relationship type (e.g. 'is blocked by', 'blocks', 'relates to')",
    )
    parser.add_argument(
        "--link-target",
        help="Issue key to link to (requires --link-relationship)",
    )


def update_status(ctx, args, issue):
    if args.status is None:
        return

    transition_fields = {}
    if args.resolution is not None:
        transition_fields["resolution"] = {"name": args.resolution}

    if args.dry_run:
        if transition_fields:
            _pretty(
                f"Would transition to {args.status} with fields:",
                transition_fields,
            )
        else:
            _pretty(f"Would transition to {args.status}")
    else:
        transitions = ctx.jira.transitions(issue)
        status_transitions = {t["name"]: t["id"] for t in transitions}
        assert args.status in status_transitions, (
            f"Status {args.status} not found in available statuses ({', '.join(status_transitions)})"
        )
        if transition_fields:
            ctx.jira.transition_issue(
                issue,
                status_transitions[args.status],
                fields=transition_fields,
            )
        else:
            ctx.jira.transition_issue(issue, status_transitions[args.status])
        print(
            f"Transitioned to {args.status} status (transition {status_transitions[args.status]})"
        )


def _update_fields(ctx, args, issue):
    custom = {}
    resolver = SprintResolver(ctx.config, ctx.jira, ctx.logger)

    if args.epic is not None:
        custom["parent"] = {"key": args.epic}

    if args.parent is not None:
        issue_type_name = getattr(args, "type", None)
        if issue_type_name is None:
            issue_type_name = issue.fields.issuetype.name
        parent_field, parent_value = resolve_parent_field(
            ctx.config, issue_type_name, args.parent
        )
        custom[parent_field] = parent_value

    if args.story_points is not None:
        custom[ctx.config["custom_fields"]["story_points"]] = args.story_points

    if args.target_start is not None:
        custom[ctx.config["custom_fields"]["target_start"]] = (
            args.target_start.strftime("%Y-%m-%d")
        )

    if args.target_end is not None:
        custom[ctx.config["custom_fields"]["target_end"]] = args.target_end.strftime(
            "%Y-%m-%d"
        )

    sprint_id = resolver.resolve(
        sprint=args.sprint,
        sprint_regexp=args.sprint_regexp,
        sprint_current=args.sprint_current,
        project=getattr(issue.fields, "project", None)
        and issue.fields.project.key
        or None,
    )
    if sprint_id is not None:
        custom[ctx.config["custom_fields"]["sprint"]] = sprint_id

    if args.labels is not None:
        custom["labels"] = issue.fields.labels + [i for i in args.labels if i != ""]

    if custom != {}:
        if args.dry_run:
            _pretty("Would configure these custom fields:", custom)
        else:
            issue.update(fields=custom)
            custom_out = {}
            for k, v in custom.items():
                try:
                    k_readable = list(ctx.config["custom_fields"].keys())[
                        list(ctx.config["custom_fields"].values()).index(k)
                    ]
                    k_readable = f"{k_readable} ({k})"
                except (KeyError, ValueError):
                    k_readable = k
                custom_out[k_readable] = v
            custom_txt = ", ".join([f"{k}: {v}" for k, v in custom_out.items()])
            print(f"Configured custom fields: {custom_txt}")


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
        if args.comment.startswith("@"):
            args.comment = open(args.comment[1:], "r").read()

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

    for issue in issues:
        update_status(ctx, args, issue)

        if args.comment is not None:
            if args.dry_run:
                _pretty("Would add this comment:", args.comment)
            else:
                adf_comment = json.loads(_translate_content("to-adf", args.comment))
                ctx.jira.add_comment(issue, adf_comment)
                print(f"Commented on the issue {issue.id}")

        _update_fields(ctx, args, issue)

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
