#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
import re
import tempfile
import subprocess
import jinja2
import jira
import json
import yaml

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

    file_handler = logging.FileHandler("/tmp/jira-cli.log")
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


def _load_config(config_path) -> Dict[str, Any]:
    config_path = Path(config_path).expanduser()

    with open(config_path, "r", encoding="utf-8") as fd:
        config_data = yaml.safe_load(fd)
    assert isinstance(config_data, dict)
    assert "server" in config_data
    assert "url" in config_data["server"]
    assert "auth" in config_data["server"]
    assert "token_auth" in config_data["server"]["auth"]
    return config_data

def _create_jira_client(url, token):
    options = {"server": url}
    return jira.JIRA(
        options=options,
        token_auth=token,
    )

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
        print(f"=== No heading ===")
        data = heading   # no heading provided, use it as data
    print(json.dumps(data, indent=4, default=lambda o: "<" + str(o) + ">"))


class Cache():
    """Object representing file with some cached data.

    Allows to get and set cached data and tracks version of that data by
    last modification date of a file."""
    def __init__(self, filename):
        self._filename = Path(filename).expanduser()
        self._version = None
        self._data = []

    def _load(self):
        try:
            # Yes, we have a small race condition here
            self._version = self._get_version()
            with open(self._filename, "r", encoding="utf-8") as fd:
                self._data = json.load(fd)
        except FileNotFoundError:
            self._version = datetime.datetime.fromtimestamp(0)
            self._data = None

    def _get_version(self):
        return datetime.datetime.fromtimestamp(os.path.getmtime(self._filename))

    def version(self):
        if self._version is None:
            self._load()
        return self._version

    def get(self):
        if self._version is None:
            self._load()
        return self._data

    def set(self, data):
        try:
            last_modified = self._get_version()
        except FileNotFoundError:
            pass
        else:
            if last_modified > self._version:
                raise Exception(f"Cache file {self._filename} was modified after we loaded it, so saving mine data might overwrite changes")

        with open(self._filename, "w", encoding="utf-8") as fd:
            json.dump(data, fd)

        self._version = self._get_version()
        self._data = data

    def empty(self):
        return self.get() is None or len(self.get()) == 0

    def obsolete(self, duration=datetime.timedelta(hours=9)):
        return self.version() < datetime.datetime.now() - duration


class Doer():
    """Do all the work with Jira as per setting in args."""
    def __init__(self, args):
        self._logger = logging.getLogger("jira_cli.Doer")

        self._args = args
        self._config = _load_config(self._args.config)
        self._jira = _create_jira_client(self._config["server"]["url"], self._config["server"]["auth"]["token_auth"])

        # Cache objects
        Path("~/.jira-cli/").expanduser().mkdir(exist_ok=True)
        self._cache_sprints = Cache("~/.jira-cli/sprints.json")

        ###_pretty("jira.project_issue_types", self._jira.project_issue_types(project="KONFLUX"))
        ###_pretty("jira.project_issue_types id", self._jira.project_issue_types(project="KONFLUX")[0].id)
        ###_pretty("jira.project_issue_types name", self._jira.project_issue_types(project="KONFLUX")[0].name)
        ###_pretty("jira.project_issue_types raw", self._jira.project_issue_types(project="KONFLUX")[0].raw)
        ###_pretty("jira.project_issue_fields", self._jira.project_issue_fields(project="KONFLUX", issue_type="1"))
        ###_pretty("dir(issue.fields)", dir(issues[0].fields))

    def execute(self):
        if self._args.subparser_name == "create":
            self.do_create()
        elif self._args.subparser_name == "update":
            self.do_update()
        elif self._args.subparser_name == "list":
            self.do_list()
        else:
            logging.error("What shall we do with a drunken sailor?")

    def _list_sprints(self):
        if not self._cache_sprints.obsolete():
            self._logger.debug("Using sprint data from cache")
            return self._cache_sprints.get()

        self._logger.debug("Populating sprint data cache")
        sprints = []

        if "boards_list" not in self._config or self._config["boards_list"] is None or len(self._config["boards_list"]) == 0:
            self._logger.warning("(Re)populating sprints cache, but it will take ages as we are going through all boards you have access to. If you add `boards_list:` into your config with just a few boards, it will be far faster.")
            for board in self._jira.boards(type="scrum", maxResults=False):
                self._logger.debug(f"Looking for sprints in board {board.id}/{board.name}")
                for sprint in self._jira.sprints(board_id=board.id, maxResults=False):
                    self._logger.debug(f"Found sprint {sprint.id}/{sprint.name}")
                    sprints.append({"board_id": board.id, "id": sprint.id, "name": sprint.name, "state": sprint.state})
        else:
            self._logger.debug(f"Loading sprints from only {len(self._config['boards_list'])} boards specified in config")
            for board_name in self._config["boards_list"]:
                for board in self._jira.boards(name=board_name, type="scrum", maxResults=False):
                    self._logger.debug(f"Looking for sprints in board {board.id}/{board.name}")
                    for sprint in self._jira.sprints(board_id=board.id, maxResults=False):
                        self._logger.debug(f"Found sprint {sprint.id}/{sprint.name}")
                        sprints.append({"board_id": board.id, "id": sprint.id, "name": sprint.name, "state": sprint.state})

        self._cache_sprints.set(sprints)
        return sprints

    def _update_status(self, issue):
        if self._args.status is None:
            return

        if self._args.dry_run:
            _pretty(f"Would transition to {self._args.status}")
        else:
            transitions = self._jira.transitions(issue)
            status_transitions = {t["name"]: t["id"] for t in transitions}
            assert (
                self._args.status in status_transitions
            ), f"Status {self._args.status} not found in available statuses ({', '.join(status_transitions)})"
            self._jira.transition_issue(issue, status_transitions[self._args.status])
            print(f"Transitioned to {self._args.status} status (transition {status_transitions[self._args.status]})")

    def _update_custom(self, issue):
        custom = {}

        if self._args.epic is not None:
            custom[self._config["custom_fields"]["epic"]] = self._args.epic

        if self._args.story_points is not None:
            custom[self._config["custom_fields"]["story_points"]] = self._args.story_points

        if self._args.target_start is not None:
            custom[self._config["custom_fields"]["target_start"]] = self._args.target_start.strftime("%Y-%m-%d")

        if self._args.target_end is not None:
            custom[self._config["custom_fields"]["target_end"]] = self._args.target_end.strftime("%Y-%m-%d")

        if self._args.sprint is not None:
            sprints = self._list_sprints()
            sprints = [i for i in sprints if i["name"] == self._args.sprint]
            assert len(sprints) == 1
            custom[self._config["custom_fields"]["sprint"]] = sprints[0]["id"]
        elif self._args.sprint_regexp is not None:
            sprints = self._list_sprints()
            pattern = re.compile(self._args.sprint_regexp)
            sprints = [i for i in sprints if i["state"] == "active" and pattern.fullmatch(i["name"])]
            assert len(sprints) == 1
            custom[self._config["custom_fields"]["sprint"]] = sprints[0]["id"]

        if custom != {}:
            if self._args.dry_run:
                _pretty(f"Would configure these custom fields:", custom)
            else:
                issue.update(**custom)
                print(f"Configured custom fields {custom}")

    def do_list(self):
        self._logger.debug(f"Searching issues: {self._args.query}")
        issues = self._jira.search_issues(self._args.query, maxResults=False)

        renderer = TemplateRenderer(self._args.template)
        rendered_output = renderer.render({"issues": issues, "query": self._args.query})
        print(rendered_output)

        if self._args.dump:
            output_dir = Path("jira_issue_details")
            output_dir.mkdir(exist_ok=True)
            for issue in issues:
                try:
                    issue_data = issue.raw  # .raw contains the full JSON
                    file_path = output_dir / f"issue-{issue.key}.json"
                    with open(file_path, "w", encoding="utf-8") as fd:
                        json.dump(issue_data, fd, indent=4, sort_keys=False)
                    logger.info(f"Saved details for issue {issue.key} to {file_path}")
                except Exception as e:
                    logger.error(f"Could not save details for issue {issue.key}: {e}")

    def do_create(self):
        # Apply issue template if specified
        if self._args.template is not None:
            assert self._args.template in self._config["issue_templates"]
            template = self._config["issue_templates"][self._args.template]
            for k, v in template.items():
                if getattr(self._args, k) is None:
                    setattr(self._args, k, v)

        # Treat description in its special way
        if self._args.description is None:
            self._args.description = _editor()
        if self._args.description.startswith("@"):
            self._args.description = open(self._args.description[1:], "r").read()

        # Some basic checks
        assert self._args.type is not None
        assert self._args.project is not None
        assert self._args.summary is not None
        assert self._args.description is not None

        # Create issue skeleton
        issue = {
            "issuetype": {"name": self._args.type},
            "project": self._args.project,
            "summary": self._args.summary,
            "description": self._args.description,
        }

        # Set security level if it was set
        if self._args.security is not None:
            issue["security"] = {"name": self._args.security}

        # Set components if it was set
        if self._args.components is not None:
            issue["components"] = [{"name": i} for i in self._args.components if i != ""]

        # Set labels if it was set
        if self._args.labels is not None:
            issue["labels"] = [{"name": i} for i in self._args.labels if i != ""]

        # If creating epic, we need to define epic name
        if self._args.type == "Epic":
            issue[self._config["custom_fields"]["epic_name"]] = args.summary

        if self._args.dry_run:
            _pretty("Would create this issue now:", issue)
        else:
            issue = self._jira.create_issue(fields=issue)
            print(f"Created issue {issue.permalink()}")

        # Load assignee details and set it to issue
        if self._args.assignee is not None:
            assignee_users = self._jira.search_users(
                user=self._args.assignee,
                query=self._args.assignee,
                includeActive=True,
                includeInactive=False,
            )
            assert len(assignee_users) == 1
            assignee = assignee_users[0]
            self._logger.debug(f"Found user {assignee}")
            if self._args.dry_run:
                _pretty("Would assign the issue to:", assignee)
            else:
                self._jira.assign_issue(issue, assignee.name)
                print(f"Assigned to {assignee.displayName} ({assignee.name})")

        # Transition issue to status
        self._update_status(issue)

        # Set custom fields
        self._update_custom(issue)

        return issue

    def do_update(self):
        if self._args.issue is not None:
            issues = []
            for i in self._args.issue.split(","):
                i = i.strip()
                self._logger.debug(f"Loading issue: {i}")
                issues.append(self._jira.issue(i))
        elif self._args.query is not None:
            self._logger.debug(f"Searching issues: {self._args.query}")
            issues = self._jira.search_issues(self._args.query, maxResults=False)
        else:
            raise Exception("Neither --issue nor --query provided")

        # Load comment as needed
        if self._args.comment is not None:
            if self._args.comment == "":
                self._args.comment = _editor()
            if self._args.comment.startswith("@"):
                self._args.comment = open(self._args.description[1:], "r").read()

        for issue in issues:
            self._update_status(issue)

            if self._args.comment is not None:
                if self._args.dry_run:
                    _pretty(f"Would add this comment:", self._args.comment)
                else:
                    self._jira.add_comment(issue, self._args.comment)
                    print(f"Commented on the issue {issue.id}")

            # Update custom fields
            self._update_custom(issue)

def main():
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

    #
    # Listing issues
    #
    parser_list = subparsers.add_parser(
        "list",
        help="List my issues in current sprint",
    )
    parser_list.add_argument(
        "--query",
        help="Jira Query Language (JQL) string.",
    )

    #
    # Creating issue
    #
    parser_create = subparsers.add_parser(
        "create",
        help="Create a ticket",
    )
    parser_create.add_argument(
        "--template",
        help="Template for creating issues",
    )
    parser_create.add_argument(
        "--project",
        help="Project of a new ticket (required)",
    )
    parser_create.add_argument(
        "--summary",
        help="Summary of a new ticket (required)",
    )
    parser_create.add_argument(
        "--description",
        help="Description text of a new ticket, if it starts with '@' it is considered a file to load it from",
    )
    parser_create.add_argument(
        "--assignee",
        help="Assignee of a new ticket (defaults to unassigned)",
    )
    parser_create.add_argument(
        "--components",
        action="append",
        help='Component of a new ticket (can be specified multiple times, set to "" to ignore)',
    )
    parser_create.add_argument(
        "--labels",
        action="append",
        help='Label of a new ticket (can be specified multiple times, set to "" to ignore)',
    )
    parser_create.add_argument(
        "--status",
        help="State of the ticket (there have to be existing transition from default to this target state)",
    )
    parser_create.add_argument(
        "--type",
        choices=["Task", "Bug", "Epic"],
        default="Task",
        help="Issue type",
    )
    parser_create.add_argument(
        "--epic",
        help="Parent epic to put this ticket under",
    )
    parser_create.add_argument(
        "--story-points",
        type=int,
        help="How many story points to set",
    )
    parser_create.add_argument(
        "--sprint",
        help="Add to this sprint",
    )
    parser_create.add_argument(
        "--sprint-regexp",
        help="Add to active sprint whose name matches this regexp",
    )
    parser_create.add_argument(
        "--target-start",
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser_create.add_argument(
        "--target-end",
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )
    parser_create.add_argument(
        "--security",
        default="Red Hat Employee",
        help="Security level of new issue",
    )

    #
    # Updating issues
    #
    parser_update = subparsers.add_parser(
        "update",
        help="Update a ticket(s)",
    )
    parser_update.add_argument(
        "--issue",
        help="Ticket (or coma separated list of tickets) to update (or use --query)",
    )
    parser_update.add_argument(
        "--query",
        help="Jira Query Language (JQL) query to list issues to update (or use --issue)",
    )
    parser_update.add_argument(
        "--status",
        help="New state of the ticket",
    )
    parser_update.add_argument(
        "--comment",
        help="New comment to add (or set to '' to edit with editor)",
    )
    parser_update.add_argument(
        "--epic",
        help="Parent epic to put this ticket under",
    )
    parser_update.add_argument(
        "--story-points",
        type=int,
        help="How many story points to set",
    )
    parser_update.add_argument(
        "--sprint",
        help="Add to this sprint",
    )
    parser_update.add_argument(
        "--sprint-regexp",
        help="Add to active sprint whose name matches this regexp",
    )
    parser_update.add_argument(
        "--target-start",
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser_update.add_argument(
        "--target-end",
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )

    args = parser.parse_args()

    if args.debug:
        logger = setup_logging(logging.DEBUG)
    elif args.debug:
        logger = setup_logging(logging.INFO)
    else:
        logger = setup_logging(logging.WARNING)

    logger.debug(f"Argumets are {args}")

    doer = Doer(args)
    doer.execute()


if __name__ == "__main__":
    main()
