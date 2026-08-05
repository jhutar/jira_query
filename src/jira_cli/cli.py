#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

import jinja2

from jira_cli.context import JiraQueryError, create_context, get_default_config_path

# Configuration
DEFAULT_CONFIG_PATH = get_default_config_path()
DEFAULT_TEMPLATE_PATH = "templates/default.md.j2"


def setup_logging(stderr_level):
    """
    Configures logging to file and stderr.

    Args:
        stderr_level (int): The logging level for stderr output.
    """
    logger = logging.getLogger("jira_cli")
    logger.setLevel(logging.DEBUG)

    urllib_logger = logging.getLogger("urllib3.connectionpool")
    urllib_logger.setLevel(stderr_level)

    file_handler = logging.FileHandler("/tmp/jira-cli.log")  # nosec B108
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(threadName)s %(levelname)s %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(stderr_level)
    stderr_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(threadName)s %(levelname)s %(message)s"
    )
    stderr_handler.setFormatter(stderr_formatter)
    logger.addHandler(stderr_handler)

    return logger


class TemplateRenderer:
    """Renders data using Jinja2 templates."""

    def __init__(self, template_path_str: str):
        self.template_path = Path(template_path_str)
        if not self.template_path.is_file():
            raise JiraQueryError(f"Template file not found: {self.template_path}")

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path.parent),
            autoescape=jinja2.select_autoescape(["html", "xml", "md"]),
        )
        self.template_name = self.template_path.name

    def render(self, data: Dict[str, Any]) -> str:
        try:
            template = self.env.get_template(self.template_name)
            return template.render(data)
        except jinja2.TemplateError as e:
            raise JiraQueryError(
                f"Error rendering template {self.template_name}: {e}"
            ) from e


def _editor():
    """
    From
    https://stackoverflow.com/questions/6309587/call-up-an-editor-vim-from-a-python-script
    """
    logger = logging.getLogger("jira_cli.editor")
    editor = [os.environ.get("EDITOR", "vim")]
    if editor == ["vim"]:
        editor.append("+set backupcopy=yes")
    logger.debug(f"Editor detected as {' '.join(editor)}")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call(editor + [tf.name])
        tf.seek(0)
        data = tf.read().decode("utf-8")
        logger.debug(f"Editor returned {data}")
        return data


def _pretty(heading, data=None):
    if data is not None:
        print(f"=== {heading} ===")
    else:
        print("=== No heading ===")
        data = heading  # no heading provided, use it as data
    print(json.dumps(data, indent=4, default=lambda o: "<" + str(o) + ">"))


def _translate_content(subcommand, input_str):
    try:
        proc = subprocess.run(
            ["adfmd", subcommand],
            input=input_str,
            capture_output=True,
            text=True,
            check=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.getLogger("jira_cli").error(
            f"adfmd {subcommand} failed (exit {e.returncode}): {e.stderr}"
        )
        raise RuntimeError(f"Content translation failed: {e.stderr}") from e


def convert_issue_adf_to_md(issue):
    """Converts Jira v3 ADF description and comments to Markdown string in place."""
    logger = logging.getLogger("jira_cli")
    issue_key = getattr(issue, "key", "unknown")
    issue_url = issue.permalink() if hasattr(issue, "permalink") else issue_key
    raw_fields = issue.raw.get("fields", {})
    raw_desc = raw_fields.get("description")
    if raw_desc and isinstance(raw_desc, dict):
        try:
            issue.fields.description = _translate_content("to-md", json.dumps(raw_desc))
        except Exception as e:
            logger.error(
                "Failed to convert description for %s (%s): %s", issue_key, issue_url, e
            )
            issue.fields.description = ""
    elif getattr(issue.fields, "description", None) is None:
        issue.fields.description = ""

    if hasattr(issue.fields, "comment") and issue.fields.comment:
        raw_comments_list = raw_fields.get("comment", {}).get("comments", [])
        for idx, comment in enumerate(issue.fields.comment.comments):
            if idx < len(raw_comments_list):
                raw_body = raw_comments_list[idx].get("body")
                if raw_body and isinstance(raw_body, dict):
                    try:
                        comment.body = _translate_content("to-md", json.dumps(raw_body))
                    except Exception as e:
                        logger.error(
                            "Failed to convert comment #%d for %s (%s): %s",
                            idx,
                            issue_key,
                            issue_url,
                            e,
                        )
                        comment.body = ""


def resolve_parent_field(config, issue_type_name, parent_key):
    """Return (field_name, value) for parent linking based on config and issue type."""
    custom_fields = config.get("custom_fields", {})
    if "parent_link" in custom_fields:
        if issue_type_name in ("Task", "Bug", "Story", "Spike"):
            return custom_fields["epic"], parent_key
        elif issue_type_name == "Epic":
            return custom_fields["parent_link"], parent_key
    return "parent", {"key": parent_key}


def resolve_assignee(ctx, assignee_query):
    """Resolve an assignee string to a single Jira user object."""
    try:
        assignee_users = ctx.jira.search_users(
            query=assignee_query,
            includeActive=True,
            includeInactive=False,
        )
    except Exception as e:
        raise AssertionError(f"Failed to search for user '{assignee_query}': {e}")

    if len(assignee_users) > 1:
        exact_matches = [
            u
            for u in assignee_users
            if u.displayName == assignee_query
            or getattr(u, "emailAddress", None) == assignee_query
            or getattr(u, "accountId", None) == assignee_query
            or getattr(u, "name", None) == assignee_query
        ]
        if len(exact_matches) == 1:
            assignee_users = exact_matches

    assert len(assignee_users) == 1, (
        f"Expected exactly one user for '{assignee_query}', but found {len(assignee_users)}. "
        f"Please use a more specific name, email, or accountId. "
        f"Found: {[u.displayName + ' (' + getattr(u, 'accountId', 'no-id') + ')' for u in assignee_users]}"
    )
    return assignee_users[0]


def assign_issue(ctx, args, issue, resolved_assignee):
    """Assign an issue to a resolved user, respecting --dry-run."""
    if args.dry_run:
        _pretty("Would assign the issue to:", resolved_assignee)
    else:
        assignee_id = getattr(
            resolved_assignee,
            "accountId",
            getattr(resolved_assignee, "name", None),
        )
        ctx.jira.assign_issue(issue, assignee_id)
        print(f"Assigned to {resolved_assignee.displayName} ({assignee_id})")


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


def update_fields(ctx, args, issue, resolved_sprint_id=None):
    from jira_cli.sprint_resolver import SprintResolver

    custom = {}

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

    if resolved_sprint_id is not None:
        custom[ctx.config["custom_fields"]["sprint"]] = resolved_sprint_id
    elif (
        getattr(args, "sprint", None) is not None
        or (
            getattr(args, "sprint_regexp", None) is not None
            and args.sprint_regexp != ""
        )
        or getattr(args, "sprint_current", False)
    ):
        project_key = None
        if hasattr(issue, "fields") and hasattr(issue.fields, "project"):
            project_key = issue.fields.project.key
        sprint_id = SprintResolver(ctx.config, ctx.jira, ctx.logger).resolve(
            sprint=args.sprint,
            sprint_regexp=getattr(args, "sprint_regexp", None),
            sprint_current=getattr(args, "sprint_current", False),
            project=project_key,
        )
        if sprint_id is not None:
            custom[ctx.config["custom_fields"]["sprint"]] = sprint_id

    if getattr(args, "labels", None) is not None:
        custom["labels"] = issue.fields.labels + [i for i in args.labels if i != ""]

    if (
        getattr(args, "add_labels", None) is not None
        or getattr(args, "remove_labels", None) is not None
    ):
        labels = list(issue.fields.labels)
        if getattr(args, "add_labels", None) is not None:
            labels += [i for i in args.add_labels if i != ""]
        if getattr(args, "remove_labels", None) is not None:
            labels = [lab for lab in labels if lab not in args.remove_labels]
        custom["labels"] = labels

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


def main():
    from jira_cli.commands import create, list, sprints, setup, template, update, view

    commands = {
        "create": create,
        "update": update,
        "list": list,
        "template": template,
        "sprints": sprints,
        "view": view,
        "setup": setup,
    }

    parser = argparse.ArgumentParser(
        description="Work with Jira tickets from command line",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file",
        type=str,
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help="Path to the Jinja2 template file",
        type=str,
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="Also dump JSON files of fetched issues",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do only read actions in Jira and show what would be done",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable info level logging output",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug level logging output",
    )

    subparsers = parser.add_subparsers(
        dest="subparser_name",
        help="sub-command help",
    )

    for cmd in commands.values():
        cmd.add_arguments(subparsers)

    args = parser.parse_args()

    if args.debug:
        logger = setup_logging(logging.DEBUG)
    elif args.verbose:
        logger = setup_logging(logging.INFO)
    else:
        logger = setup_logging(logging.WARNING)

    logger.debug(f"Arguments are {args}")

    if args.subparser_name is None:
        parser.print_help()
        return

    if args.subparser_name == "setup":
        setup.run(None, args)
        return

    try:
        ctx = create_context(args)
    except JiraQueryError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cmd = commands.get(args.subparser_name)
    if cmd:
        cmd.run(ctx, args)
    else:
        logging.error("What shall we do with a drunken sailor?")


if __name__ == "__main__":
    main()
