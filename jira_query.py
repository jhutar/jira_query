#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import jinja2
from jira import JIRA
from jira.resources import Issue
import json
import yaml

# Configuration
DEFAULT_CONFIG_PATH = "~/.jira_query.yaml"
DEFAULT_TEMPLATE_PATH = "templates/default.md.j2"

# Logging Setup
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class JiraQueryError(Exception):
    """Custom exception for Jira query errors that also logs the error."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        logger.error(message)


class JiraClient:
    """A client to interact with Jira."""

    def __init__(self, server_url: str, token: Optional[str] = None):
        """
        Initializes the Jira client.

        Args:
            server_url: The URL of the Jira server.
            token: The personal access token for authentication.
        """
        try:
            options = {"server": server_url}
            if token:
                self.jira = JIRA(options=options, token_auth=token)
            else:
                self.jira = JIRA(options=options)
            logger.info(f"Successfully connected to Jira server: {server_url}")
        except Exception as e:
            raise JiraQueryError(
                f"Failed to connect to Jira server {server_url}: {e}"
            ) from e

    def search_issues(self, jql_query: str, max_results: Optional[int] = None) -> List[Issue]:
        """
        Searches for issues using a JQL query.

        Args:
            jql_query: The JQL query string.
            max_results: Maximum number of results to return.
                         If None, fetches all results (jira-python default is 50,
                         so explicit False or a high number might be needed for 'all').
                         Using None here for clarity, jira-python's `maxResults=False`
                         is a bit of a special case for "all".

        Returns:
            A list of Jira Issue objects.
        """
        logger.debug(f"Executing JQL query: {jql_query}")
        try:
            issues = self.jira.search_issues(jql_query, maxResults=max_results if max_results is not None else False)
        except Exception as e:
            raise JiraQueryError(
                f"Error executing JQL query '{jql_query}': {e}"
            ) from e
        logger.info(f"Found {len(issues)} issues for query: {jql_query}")
        return issues


class TemplateRenderer:
    """Renders data using Jinja2 templates."""

    def __init__(self, template_path_str: str):
        """
        Initializes the template renderer.

        Args:
            template_path_str: Path to the Jinja2 template file.
        """
        self.template_path = Path(template_path_str)
        if not self.template_path.is_file():
            raise JiraQueryError(f"Template file not found: {self.template_path}")

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path.parent),
            autoescape=jinja2.select_autoescape(["html", "xml", "md"]),
        )
        self.template_name = self.template_path.name

    def render(self, data: Dict[str, Any]) -> str:
        """
        Renders the template with the given data.

        Args:
            data: A dictionary containing data to pass to the template.

        Returns:
            The rendered template as a string.
        """
        try:
            template = self.env.get_template(self.template_name)
            return template.render(data)
        except jinja2.TemplateError as e:
            raise JiraQueryError(
                f"Error rendering template {self.template_name}: {e}"
            ) from e


def setup_arg_parser() -> argparse.ArgumentParser:
    """Sets up and returns the argument parser."""
    parser = argparse.ArgumentParser(
        description="Query Jira and render results using a Jinja2 template.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file.",
        type=str,
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help="Path to the Jinja2 template file.",
        type=str,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to the output file. If not specified, prints to stdout.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--dump",
        "-u",
        action="store_true",
        help="Also dump JSON files of fetched issues.",
    )
    parser.add_argument(
        "--info",
        "-i",
        action="store_true",
        help="Enable info logging output.",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug logging output.",
    )
    parser.add_argument(
        "jql_query",
        help="Jira Query Language (JQL) string.",
        metavar="JQL_QUERY",
    )
    return parser


def load_server_config(config_path) -> Dict[str, Any]:
    config_path = Path(config_path).expanduser()

    try:
        with open(config_path, "r", encoding="utf-8") as fd:
            config_data = yaml.safe_load(fd)
        server_conf = config_data.get("server")
        assert isinstance(server_conf, dict)
        assert "url" in server_conf
        assert "auth" in server_conf
        assert "token_auth" in server_conf["auth"]
    except Exception as e:
        raise JiraQueryError(f"Error reading config {config_path}: {e}") from e
    return server_conf


def main():
    """Main execution function."""
    args = setup_arg_parser().parse_args()

    if args.debug:
        level = logging.DEBUG
    elif args.info:
        level = logging.INFO
    else:
        level = logging.WARNING
    logger.setLevel(level)
    # Update level for all handlers if more are added
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)

    logger.debug(f"Arguments received: {args}")

    try:
        # 1. Load configuration
        server_conf = load_server_config(args.config)
        jira_url = server_conf["url"]
        jira_token = server_conf["auth"]["token_auth"]

        # 2. Initialize Jira client
        jira_client = JiraClient(server_url=jira_url, token=jira_token)

        # 3. Fetch issues
        issues = jira_client.search_issues(args.jql_query)

        # 4. Render output
        renderer = TemplateRenderer(args.template)
        rendered_output = renderer.render({"issues": issues, "query": args.jql_query})

        # 5. Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
            with open(output_path, "w", encoding="utf-8") as fd:
                fd.write(rendered_output)
            logger.info(f"Output successfully written to {output_path}")
        else:
            print(rendered_output)

        # 6. Dump issue details
        if args.dump:
            output_dir = Path("jira_issue_details")
            output_dir.mkdir(exist_ok=True)
            for issue in issues:
                try:
                    issue_data = issue.raw  # .raw contains the full JSON
                    file_path = output_dir / f"issue-{issue.key}.json"
                    with open(file_path, "w", encoding="utf-8") as fd:
                        json.dump(issue_data, fd, indent=4, sort_keys=False)
                    logger.debug(f"Saved details for issue {issue.key} to {file_path}")
                except Exception as e:
                    logger.error(f"Could not save details for issue {issue.key}: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=args.debug)
        exit(1)


if __name__ == "__main__":
    main()
