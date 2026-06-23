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

from jira_cli.context import JiraQueryError, create_context

# Configuration
DEFAULT_CONFIG_PATH = "~/.jira_query.yaml"
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
    raw_fields = issue.raw.get("fields", {})
    raw_desc = raw_fields.get("description")
    if raw_desc and isinstance(raw_desc, dict):
        try:
            issue.fields.description = _translate_content("to-md", json.dumps(raw_desc))
        except Exception as e:
            print(f"Error converting description: {e}", file=sys.stderr)
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
                        print(f"Error converting comment: {e}", file=sys.stderr)


def main():
    from jira_cli.commands import create, list, sprints, template, update, view

    commands = {
        "create": create,
        "update": update,
        "list": list,
        "template": template,
        "sprints": sprints,
        "view": view,
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

    ctx = create_context(args)

    cmd = commands.get(args.subparser_name)
    if cmd:
        cmd.run(ctx, args)
    else:
        logging.error("What shall we do with a drunken sailor?")


if __name__ == "__main__":
    main()
