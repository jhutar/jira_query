#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

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
    editor = [os.environ.get("EDITOR", "vim")]
    if editor == ["vim"]:
        editor.append("+set backupcopy=yes")
    logging.debug("Editor detected as %s" % " ".join(editor))
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call(editor + [tf.name])
        tf.seek(0)
        return tf.read().decode("utf-8")


def _ensure(my_dict, my_key, my_default):
    """
    Helper to ensure key exists in a dict and if not set to a given value
    """
    if my_key not in my_dict:
        my_dict[my_key] = my_default


def _pretty(heading, data=None):
    if data is not None:
        print(f"=== {heading} ===")
    else:
        data = heading   # no heading provided, use it as data
    print(json.dumps(data, indent=4, default=lambda o: "<" + str(o) + ">"))


class Cache():
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
    def __init__(self, args):
        self._logger = logging.getLogger("jira_cli.Doer")

        self._args = args
        self._config = _load_config(self._args.config)
        self._jira = _create_jira_client(self._config["server"]["url"], self._config["server"]["auth"]["token_auth"])

        # Caches
        Path("~/.jira-cli/").expanduser().mkdir(exist_ok=True)
        self._cache_sprints = Cache("~/.jira-cli/sprints.json")

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


    def do_list(self):
        self._list_sprints()

        self._logger.debug(f"Searching issues: {self._args.query}")
        issues = self._jira.search_issues(self._args.query, maxResults=False)
        ###_pretty("jira.boards", self._jira.boards(name="Konflux/RHTAP Perf&Scale board", type="scrum"))
        ###_pretty("jira.sprints", self._jira.sprints(board_id=self._jira.boards(name="Konflux/RHTAP Perf&Scale board", type="scrum")[0].id))
        ###_pretty("jira.project_issue_types", self._jira.project_issue_types(project="KONFLUX"))
        ###_pretty("jira.project_issue_types id", self._jira.project_issue_types(project="KONFLUX")[0].id)
        ###_pretty("jira.project_issue_types name", self._jira.project_issue_types(project="KONFLUX")[0].name)
        ###_pretty("jira.project_issue_types raw", self._jira.project_issue_types(project="KONFLUX")[0].raw)
        ###_pretty("jira.project_issue_fields", self._jira.project_issue_fields(project="KONFLUX", issue_type="1"))
        ###_pretty("dir(issue.fields)", dir(issues[0].fields))
        ###_pretty("issue.fields.customfield_12310243", issues[0].fields.customfield_12310243)
        ###_pretty("issue.fields.comment.comments", issues[0].fields.comment.comments)
        ###_pretty("issue.transitions", self._jira.transitions(issues[0]))

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


    def do_create(my_jira, my_config, **kwargs):
        # Load assignee details
        if args.assignee is not None:
            assignee_users = my_jira.search_users(
                user=args.assignee,
                query=args.assignee,
                includeActive=True,
                includeInactive=False,
            )
            assert len(assignee_users) == 1

        # Create issue
        issue = {
            "issuetype": {"name": args.type},
            "project": args.project,
            "summary": args.summary,
            "description": args.description,
        }

        # Set components if it was set or use defaults
        if args.component is not None:
            issue["components"] = [{"name": i} for i in args.component if i != ""]
        else:
            try:
                issue["components"] = [
                    {"name": i}
                    for i in my_config["defaults"]["projects"][args.project][
                        "components"
                    ]
                ]
            except KeyError:
                pass

        # Set labels if it was set or use defaults
        if args.label is not None:
            issue["labels"] = [{"name": i} for i in args.label if i != ""]
        else:
            try:
                issue["labels"] = my_config["defaults"]["projects"][args.project][
                    "labels"
                ]
            except KeyError:
                pass

        # If creating epic, we need to define epic name
        if args.type == "Epic":
            issue[my_config["defaults"]["custom_fields"]["epic_name"]] = args.summary

        issue = create(my_jira, **issue)

        # Set assignee
        if args.assignee is not None:
            issue.update(
                assignee={
                    "name": assignee_users[0].name,
                    "accountId": assignee_users[0].key,
                    "displayName": assignee_users[0].displayName,
                }
            )
            print(
                f"Assigned to {assignee_users[0].displayName} ({assignee_users[0].name})"
            )

        # Set status
        if args.status is not None:
            transitions = my_jira.transitions(issue)
            status_transitions = {t["name"]: t["id"] for t in transitions}
            assert (
                args.status in status_transitions
            ), f"Status {args.status} not found in available statuses ({', '.join(status_transitions)})"
            my_jira.transition_issue(issue, status_transitions[args.status])
            print(
                f"Transitioned to {args.status} status (transition {status_transitions[args.status]})"
            )

        # Set custom fields
        customization = {}
        if args.epic is not None:
            customization[my_config["defaults"]["custom_fields"]["epic"]] = args.epic
        if args.story_points is not None:
            customization[my_config["defaults"]["custom_fields"]["story_points"]] = (
                args.story_points
            )
        issue.update(**customization)
        print(f"Configured custom fields {customization}")

        print(f"Link is {issue.permalink()}")

        if "description" not in kwargs or kwargs["description"] is None:
            kwargs["description"] = _editor()
        if kwargs["description"].startswith("@"):
            kwargs["description"] = open(kwargs["description"][1:], "r").read()

        new_issue = my_jira.create_issue(**kwargs)
        print("Created %s" % new_issue)

        my_jira.assign_issue(new_issue, None)

        return new_issue


    def do_update(jira, args):
        return jira.change_status(args.issue, args.status)


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

    parser_list = subparsers.add_parser(
        "list",
        help="List my issues in current sprint",
    )
    parser_list.add_argument(
        "--query",
        help="Jira Query Language (JQL) string.",
    )

    parser_create = subparsers.add_parser(
        "create",
        help="Create a ticket",
    )
    parser_create.add_argument(
        "--project",
        required=True,
        help="Project of a new ticket (required)",
    )
    parser_create.add_argument(
        "--summary",
        required=True,
        help="Summary of a new ticket (required)",
    )
    parser_create.add_argument(
        "--description",
        help="Description text of a new ticket, if it starts with '@' it is considered a file to load it from",
    )
    parser_create.add_argument(
        "--assignee", help="Assignee of a new ticket (defaults to unassigned)"
    )
    parser_create.add_argument(
        "--component",
        action="append",
        help='Component of a new ticket (can be specified multiple times, set to "" to ignore)',
    )
    parser_create.add_argument(
        "--label",
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
        help="How many story points to add",
    )
    parser_create.add_argument(
        "--sprint",
        help="Add to this sprint",
    )

    parser_update = subparsers.add_parser(
        "update",
        help="Update a ticket(s)",
    )
    parser_update.add_argument(
        "--issue",
        required=True,
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
        help="New comment to add",
    )

    args = parser.parse_args()

    ###warnings.filterwarnings("ignore")

    if args.debug:
        logger = setup_logging(logging.DEBUG)
    elif args.debug:
        logger = setup_logging(logging.INFO)
    else:
        logged = setup_logging(logging.WARNING)

    logger.debug(f"Argumets are {args}")

    doer = Doer(args)
    doer.execute()


if __name__ == "__main__":
    main()
