#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from jira_cli.sprint_resolver import SprintResolver


def add_arguments(subparsers):
    parser = subparsers.add_parser(
        "sprints",
        help="List sprints for a specific board or project",
    )
    parser.add_argument(
        "--board-id",
        help="Filter sprints by board ID",
        type=int,
    )
    parser.add_argument(
        "--state",
        choices=["active", "future", "closed", "all"],
        default="active",
        help="Filter sprints by state",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh the cached sprint data",
    )


def run(ctx, args):
    resolver = SprintResolver(ctx.config, ctx.jira, ctx.logger)

    if args.refresh:
        resolver.refresh()

    sprints = resolver.list_sprints()

    if args.board_id is not None:
        sprints = [s for s in sprints if s["board_id"] == args.board_id]

    if args.state != "all":
        sprints = [s for s in sprints if s["state"] == args.state]

    header = f"{'Board ID':<10} {'Sprint ID':<12} {'Sprint Name':<30} {'State'}"
    print(header)
    print("-" * len(header))
    for s in sprints:
        print(f"{s['board_id']:<10} {s['id']:<12} {s['name']:<30} {s['state']}")
