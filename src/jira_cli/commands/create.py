#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import json

from jira_cli.cli import (
    _editor,
    _pretty,
    _translate_content,
    assign_issue,
    resolve_assignee,
    resolve_parent_field,
    update_fields,
    update_status,
)
from jira_cli.sprint_resolver import SprintResolver


def add_arguments(subparsers):
    parser = subparsers.add_parser(
        "create",
        help="Create a ticket",
    )
    parser.add_argument(
        "--template",
        help="Template for creating issues",
    )
    parser.add_argument(
        "--project",
        help="Project of a new ticket (required)",
    )
    parser.add_argument(
        "--summary",
        help="Summary of a new ticket (required)",
    )
    parser.add_argument(
        "--description",
        help="Description text of a new ticket in Markdown format, if it starts with '@' it is considered a file to load it from",
    )
    parser.add_argument(
        "--assignee",
        help="Assignee of a new ticket (defaults to unassigned)",
    )
    parser.add_argument(
        "--components",
        action="append",
        help='Component of a new ticket (can be specified multiple times, set to "" to ignore)',
    )
    parser.add_argument(
        "--labels",
        action="append",
        help='Label of a new ticket (can be specified multiple times, set to "" to ignore)',
    )
    parser.add_argument(
        "--status",
        help="State of the ticket (there have to be existing transition from default to this target state)",
    )
    parser.add_argument(
        "--resolution",
        help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
    )
    parser.add_argument(
        "--type",
        choices=["Task", "Bug", "Epic", "Feature", "Sub-task"],
        default="Task",
        help="Issue type",
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
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--target-end",
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--security",
        help="Security level of new issue (default 'Red Hat Employee', set to \"\" to omit security)",
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
    # Apply issue template if specified
    if args.template is not None:
        assert args.template in ctx.config["issue_templates"]
        template = ctx.config["issue_templates"][args.template]
        for k, v in template.items():
            if getattr(args, k) is None:
                setattr(args, k, v)

    # Apply project-level defaults from configuration
    if args.project is not None:
        proj_defaults = ctx.config.get("project_defaults", {}).get(args.project, {})
        for attr_name, default_value in proj_defaults.items():
            current_value = getattr(args, attr_name, None)
            if current_value is None or current_value is False:
                setattr(args, attr_name, default_value)
                ctx.logger.info(
                    f"Using project default for '{attr_name}': {default_value}"
                )

    # Treat description in its special way
    if args.description is None:
        args.description = _editor()
    elif args.description.startswith("@"):
        args.description = open(args.description[1:], "r").read()
    else:
        args.description = args.description.replace(r"\n", "\n").replace(r"\t", "\t")

    # Some basic checks
    assert args.type is not None
    assert args.project is not None
    assert args.summary is not None
    assert args.description is not None
    assert not (args.parent is not None and args.epic is not None), (
        "Cannot specify both --parent and --epic; use --parent for unified hierarchy linking"
    )
    if args.type == "Sub-task":
        assert args.parent is not None, (
            "A parent issue key (via --parent) is required when creating a Sub-task."
        )
    assert (args.link_relationship is None) == (args.link_target is None), (
        "--link-relationship and --link-target must be specified together"
    )

    # Pre-validation of Jira entities and configurations before issue creation
    # 1. Project validation
    try:
        ctx.logger.debug(f"Pre-validating project: {args.project}")
        project = ctx.jira.project(args.project)
    except Exception as e:
        raise AssertionError(
            f"Project '{args.project}' does not exist or is inaccessible: {e}"
        )

    # 2. Issue Type validation
    try:
        issue_types = project.issueTypes
    except Exception as e:
        raise AssertionError(
            f"Failed to retrieve issue types for project '{args.project}': {e}"
        )
    valid_type_names = [it.name for it in issue_types]
    assert args.type in valid_type_names, (
        f"Issue type '{args.type}' is not valid for project '{args.project}'. "
        f"Available issue types: {', '.join(valid_type_names)}"
    )

    # 3. Status validation
    if args.status is not None:
        try:
            url = f"{ctx.jira._options['server']}/rest/api/2/project/{args.project}/statuses"
            response = ctx.jira._session.get(url)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            project_statuses = response.json()
        except Exception as e:
            raise AssertionError(
                f"Failed to retrieve statuses for project '{args.project}': {e}"
            )

        found_itype = None
        for itype in project_statuses:
            itype_name = (
                itype.name
                if hasattr(itype, "name")
                else itype.get("name")
                if isinstance(itype, dict)
                else None
            )
            if itype_name == args.type:
                found_itype = itype
                break

        if found_itype is not None:
            statuses_list = (
                found_itype.statuses
                if hasattr(found_itype, "statuses")
                else found_itype.get("statuses", [])
                if isinstance(found_itype, dict)
                else []
            )
            valid_statuses = [
                (
                    status.name
                    if hasattr(status, "name")
                    else status.get("name")
                    if isinstance(status, dict)
                    else ""
                )
                for status in statuses_list
            ]
            assert args.status in valid_statuses, (
                f"Status '{args.status}' is not valid for issue type '{args.type}' in project '{args.project}'. "
                f"Valid statuses are: {', '.join(valid_statuses)}"
            )
        else:
            ctx.logger.warning(
                f"Could not find status list for issue type '{args.type}' in project_statuses."
            )

    # 4. Security level validation
    security_is_default = False
    if args.security is None:
        args.security = "Red Hat Employee"
        security_is_default = True
        ctx.logger.info("Using global default for 'security': Red Hat Employee")

    resolved_security_id = None
    if args.security is not None and args.security != "":
        try:
            url = f"{ctx.jira._options['server']}/rest/api/2/project/{args.project}/securitylevel"
            response = ctx.jira._session.get(url)
            if response.status_code == 200:
                data = response.json()
                levels_list = []
                if isinstance(data, list):
                    levels_list = data
                elif isinstance(data, dict) and "levels" in data:
                    levels_list = data["levels"]

                security_map = {
                    item["name"]: item["id"]
                    for item in levels_list
                    if isinstance(item, dict) and "name" in item and "id" in item
                }
            else:
                security_map = {}
        except Exception as e:
            ctx.logger.warning(
                f"Could not retrieve security levels for project {args.project}: {e}"
            )
            security_map = {}

        if args.security in security_map:
            resolved_security_id = security_map[args.security]
        else:
            if security_is_default:
                args.security = ""
            else:
                raise AssertionError(
                    f"Security level '{args.security}' is not valid for project '{args.project}' or could not be retrieved. "
                    f"Available levels: {', '.join(security_map.keys())}"
                )

    # 5. Epic validation
    if args.epic is not None:
        try:
            ctx.logger.debug(f"Pre-validating epic: {args.epic}")
            ctx.jira.issue(args.epic, fields="summary")
        except Exception as e:
            raise AssertionError(
                f"Epic issue '{args.epic}' not found or inaccessible: {e}"
            )

    # 6. Parent validation
    if args.parent is not None:
        try:
            ctx.logger.debug(f"Pre-validating parent: {args.parent}")
            ctx.jira.issue(args.parent, fields="issuetype")
        except Exception as e:
            raise AssertionError(
                f"Parent issue '{args.parent}' not found or inaccessible: {e}"
            )

    # 7. Link target validation
    if args.link_target is not None:
        try:
            ctx.logger.debug(f"Pre-validating link target: {args.link_target}")
            ctx.jira.issue(args.link_target, fields="summary")
        except Exception as e:
            raise AssertionError(
                f"Link target issue '{args.link_target}' not found or inaccessible: {e}"
            )

    # 8. Assignee validation
    resolved_assignee = None
    if args.assignee is not None:
        resolved_assignee = resolve_assignee(ctx, args.assignee)
        ctx.logger.debug(f"Pre-validated assignee: {resolved_assignee}")

    # 9. Sprint validation
    resolved_sprint_id = None
    if (
        args.sprint is not None
        or (args.sprint_regexp is not None and args.sprint_regexp != "")
        or args.sprint_current
    ):
        resolver = SprintResolver(ctx.config, ctx.jira, ctx.logger)
        resolved_sprint_id = resolver.resolve(
            sprint=args.sprint,
            sprint_regexp=args.sprint_regexp,
            sprint_current=args.sprint_current,
            project=args.project,
        )

    # Create issue skeleton
    adf_description = json.loads(_translate_content("to-adf", args.description))
    issue = {
        "issuetype": {"name": args.type},
        "project": args.project,
        "summary": args.summary,
        "description": adf_description,
    }

    # Set parent link (v3 unified parent field) for epic
    if args.epic is not None:
        issue["parent"] = {"key": args.epic}

    # Set parent link via --parent (v3 or legacy routing)
    if args.parent is not None:
        parent_field, parent_value = resolve_parent_field(
            ctx.config, args.type, args.parent
        )
        issue[parent_field] = parent_value

    # Set security level if it was set
    if args.security is not None and args.security != "":
        issue["security"] = {"id": resolved_security_id}

    # Set components if it was set
    if args.components is not None:
        issue["components"] = [{"name": i} for i in args.components if i != ""]

    # If creating epic, we need to define epic name
    if args.type == "Epic":
        issue[ctx.config["custom_fields"]["epic_name"]] = args.summary

    if args.dry_run:
        _pretty("Would create this issue now:", issue)
    else:
        issue = ctx.jira.create_issue(fields=issue)
        print(f"Created issue {issue.permalink()}")

    if resolved_assignee is not None:
        assign_issue(ctx, args, issue, resolved_assignee)

    # Transition issue to status
    update_status(ctx, args, issue)

    # Set custom fields and labels and possibly more
    update_fields(ctx, args, issue, resolved_sprint_id=resolved_sprint_id)

    # Link to another issue
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

    return issue
