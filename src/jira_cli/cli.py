#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict
import re
import tempfile
import subprocess
import jinja2
import jira
import json
import yaml

from jira_cli.pr_utils import enrich_with_prs

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


class JiraQueryError(Exception):
    """Custom exception for Jira query errors."""

    pass


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


def load_config(config_path) -> Dict[str, Any]:
    config_path = Path(config_path).expanduser()

    with open(config_path, "r", encoding="utf-8") as fd:
        config_data = yaml.safe_load(fd)
    assert isinstance(config_data, dict)
    assert "server" in config_data
    assert "url" in config_data["server"]
    assert "auth" in config_data["server"]
    assert "basic_auth" in config_data["server"]["auth"]
    assert "username" in config_data["server"]["auth"]["basic_auth"]
    assert "token" in config_data["server"]["auth"]["basic_auth"]
    return config_data


def load_server_config(config_path) -> Dict[str, Any]:
    return load_config(config_path)["server"]


def _create_jira_client(url, username, token):
    options = {
        "server": url,
        "rest_api_version": "3",
    }
    return jira.JIRA(
        options=options,
        basic_auth=(username, token),
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
            import sys

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
                        import sys

                        print(f"Error converting comment: {e}", file=sys.stderr)


class Cache:
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
                raise Exception(
                    f"Cache file {self._filename} was modified after we loaded it, so saving mine data might overwrite changes"
                )

        with open(self._filename, "w", encoding="utf-8") as fd:
            json.dump(data, fd)

        self._version = self._get_version()
        self._data = data

    def empty(self):
        return self.get() is None or len(self.get()) == 0

    def obsolete(self, duration=datetime.timedelta(hours=9)):
        return self.version() < datetime.datetime.now() - duration


class Doer:
    """Do all the work with Jira as per setting in args."""

    def __init__(self, args):
        self._logger = logging.getLogger("jira_cli.Doer")

        self._args = args
        self._config = load_config(self._args.config)
        auth = self._config["server"]["auth"]["basic_auth"]
        self._jira = _create_jira_client(
            self._config["server"]["url"], auth["username"], auth["token"]
        )

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
        elif self._args.subparser_name == "template":
            self.do_tempate()
        elif self._args.subparser_name == "sprints":
            self.do_sprints()
        elif self._args.subparser_name == "view":
            self.do_view()
        else:
            logging.error("What shall we do with a drunken sailor?")

    def _list_sprints(self):
        if not self._cache_sprints.obsolete():
            self._logger.debug("Using sprint data from cache")
            return self._cache_sprints.get()

        self._logger.debug("Populating sprint data cache")
        sprints = []

        if (
            "boards_list" not in self._config
            or self._config["boards_list"] is None
            or len(self._config["boards_list"]) == 0
        ):
            self._logger.warning(
                "(Re)populating sprints cache, but it will take ages as we are going through all boards you have access to. If you add `boards_list:` into your config with just a few boards, it will be far faster."
            )
            for board in self._jira.boards(type="scrum", maxResults=False):
                self._logger.debug(
                    f"Looking for sprints in board {board.id}/{board.name}"
                )
                for sprint in self._jira.sprints(board_id=board.id, maxResults=False):
                    self._logger.debug(f"Found sprint {sprint.id}/{sprint.name}")
                    sprints.append(
                        {
                            "board_id": board.id,
                            "id": sprint.id,
                            "name": sprint.name,
                            "state": sprint.state,
                        }
                    )
        else:
            self._logger.debug(
                f"Loading sprints from only {len(self._config['boards_list'])} boards specified in config"
            )
            for board_name in self._config["boards_list"]:
                for board in self._jira.boards(
                    name=board_name, type="scrum", maxResults=False
                ):
                    self._logger.debug(
                        f"Looking for sprints in board {board.id}/{board.name}"
                    )
                    for sprint in self._jira.sprints(
                        board_id=board.id, maxResults=False
                    ):
                        self._logger.debug(f"Found sprint {sprint.id}/{sprint.name}")
                        sprints.append(
                            {
                                "board_id": board.id,
                                "id": sprint.id,
                                "name": sprint.name,
                                "state": sprint.state,
                            }
                        )

        self._cache_sprints.set(sprints)
        return sprints

    def _update_status(self, issue):
        if self._args.status is None:
            return

        transition_fields = {}
        if self._args.resolution is not None:
            transition_fields["resolution"] = {"name": self._args.resolution}

        if self._args.dry_run:
            if transition_fields:
                _pretty(
                    f"Would transition to {self._args.status} with fields:",
                    transition_fields,
                )
            else:
                _pretty(f"Would transition to {self._args.status}")
        else:
            transitions = self._jira.transitions(issue)
            status_transitions = {t["name"]: t["id"] for t in transitions}
            assert self._args.status in status_transitions, (
                f"Status {self._args.status} not found in available statuses ({', '.join(status_transitions)})"
            )
            if transition_fields:
                self._jira.transition_issue(
                    issue,
                    status_transitions[self._args.status],
                    fields=transition_fields,
                )
            else:
                self._jira.transition_issue(
                    issue, status_transitions[self._args.status]
                )
            print(
                f"Transitioned to {self._args.status} status (transition {status_transitions[self._args.status]})"
            )

    def _resolve_parent_field(self, issue_type_name):
        """Return (field_name, value) for parent linking based on config and issue type."""
        custom_fields = self._config.get("custom_fields", {})
        if "parent_link" in custom_fields:
            # Legacy fallback: route to Epic Link or Parent Link custom fields
            if issue_type_name in ("Task", "Bug", "Story"):
                return custom_fields["epic"], self._args.parent
            elif issue_type_name == "Epic":
                return custom_fields["parent_link"], self._args.parent
        # v3 default: unified parent field
        return "parent", {"key": self._args.parent}

    def _update_fields(self, issue, resolved_sprint_id=None):
        custom = {}

        if self._args.epic is not None:
            custom["parent"] = {"key": self._args.epic}

        if self._args.parent is not None:
            issue_type_name = getattr(self._args, "type", None)
            if issue_type_name is None:
                issue_type_name = issue.fields.issuetype.name
            parent_field, parent_value = self._resolve_parent_field(issue_type_name)
            custom[parent_field] = parent_value

        if self._args.story_points is not None:
            custom[self._config["custom_fields"]["story_points"]] = (
                self._args.story_points
            )

        if self._args.target_start is not None:
            custom[self._config["custom_fields"]["target_start"]] = (
                self._args.target_start.strftime("%Y-%m-%d")
            )

        if self._args.target_end is not None:
            custom[self._config["custom_fields"]["target_end"]] = (
                self._args.target_end.strftime("%Y-%m-%d")
            )

        if resolved_sprint_id is not None:
            custom[self._config["custom_fields"]["sprint"]] = resolved_sprint_id
        elif self._args.sprint is not None:
            sprints = self._list_sprints()
            sprints = [i for i in sprints if i["name"] == self._args.sprint]
            assert len(sprints) == 1
            custom[self._config["custom_fields"]["sprint"]] = sprints[0]["id"]
        elif self._args.sprint_regexp is not None and self._args.sprint_regexp != "":
            sprints = self._list_sprints()
            pattern = re.compile(self._args.sprint_regexp)
            sprints = [
                i
                for i in sprints
                if i["state"] == "active" and pattern.fullmatch(i["name"])
            ]
            assert len(sprints) == 1
            custom[self._config["custom_fields"]["sprint"]] = sprints[0]["id"]
        elif self._args.sprint_current:
            sprints = self._list_sprints()
            pattern = re.compile(
                self._config["sprint_regexps"][issue.fields.project.key]
            )
            sprints = [
                i
                for i in sprints
                if i["state"] == "active" and pattern.fullmatch(i["name"])
            ]
            assert len(sprints) == 1
            custom[self._config["custom_fields"]["sprint"]] = sprints[0]["id"]

        if self._args.labels is not None:
            custom["labels"] = issue.fields.labels + [
                i for i in self._args.labels if i != ""
            ]

        if custom != {}:
            if self._args.dry_run:
                _pretty("Would configure these custom fields:", custom)
            else:
                issue.update(fields=custom)
                custom_out = {}
                for k, v in custom.items():
                    try:
                        k_readable = list(self._config["custom_fields"].keys())[
                            list(self._config["custom_fields"].values()).index(k)
                        ]
                        k_readable = f"{k_readable} ({k})"
                    except (KeyError, ValueError):
                        k_readable = k
                    custom_out[k_readable] = v
                custom_txt = ", ".join([f"{k}: {v}" for k, v in custom_out.items()])
                print(f"Configured custom fields: {custom_txt}")

    def do_list(self):
        self._logger.debug(f"Searching issues: {self._args.query}")
        issues = self._jira.search_issues(self._args.query, maxResults=False)

        for issue in issues:
            if isinstance(issue.fields.description, dict):
                issue.fields.description = _translate_content(
                    "to-md", json.dumps(issue.fields.description)
                )
            if hasattr(issue.fields, "comment") and hasattr(
                issue.fields.comment, "comments"
            ):
                for comment in issue.fields.comment.comments:
                    if isinstance(comment.body, dict):
                        comment.body = _translate_content(
                            "to-md", json.dumps(comment.body)
                        )

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
                    self._logger.info(
                        f"Saved details for issue {issue.key} to {file_path}"
                    )
                except Exception as e:
                    self._logger.error(
                        f"Could not save details for issue {issue.key}: {e}"
                    )

    def do_create(self):
        # Apply issue template if specified
        if self._args.template is not None:
            assert self._args.template in self._config["issue_templates"]
            template = self._config["issue_templates"][self._args.template]
            for k, v in template.items():
                if getattr(self._args, k) is None:
                    setattr(self._args, k, v)

        # Apply project-level defaults from configuration
        if self._args.project is not None:
            proj_defaults = self._config.get("project_defaults", {}).get(
                self._args.project, {}
            )
            for attr_name, default_value in proj_defaults.items():
                current_value = getattr(self._args, attr_name, None)
                if current_value is None or current_value is False:
                    setattr(self._args, attr_name, default_value)
                    self._logger.info(
                        f"Using project default for '{attr_name}': {default_value}"
                    )

        # Treat description in its special way
        if self._args.description is None:
            self._args.description = _editor()
        elif self._args.description.startswith("@"):
            self._args.description = open(self._args.description[1:], "r").read()
        else:
            self._args.description = self._args.description.replace(
                r"\n", "\n"
            ).replace(r"\t", "\t")

        # Some basic checks
        assert self._args.type is not None
        assert self._args.project is not None
        assert self._args.summary is not None
        assert self._args.description is not None
        assert not (self._args.parent is not None and self._args.epic is not None), (
            "Cannot specify both --parent and --epic; use --parent for unified hierarchy linking"
        )
        if self._args.type == "Sub-task":
            assert self._args.parent is not None, (
                "A parent issue key (via --parent) is required when creating a Sub-task."
            )

        # Pre-validation of Jira entities and configurations before issue creation
        # 1. Project validation
        try:
            self._logger.debug(f"Pre-validating project: {self._args.project}")
            project = self._jira.project(self._args.project)
        except Exception as e:
            raise AssertionError(
                f"Project '{self._args.project}' does not exist or is inaccessible: {e}"
            )

        # 2. Issue Type validation
        try:
            issue_types = project.issueTypes
        except Exception as e:
            raise AssertionError(
                f"Failed to retrieve issue types for project '{self._args.project}': {e}"
            )
        valid_type_names = [it.name for it in issue_types]
        assert self._args.type in valid_type_names, (
            f"Issue type '{self._args.type}' is not valid for project '{self._args.project}'. "
            f"Available issue types: {', '.join(valid_type_names)}"
        )

        # 3. Status validation
        if self._args.status is not None:
            try:
                url = f"{self._jira._options['server']}/rest/api/2/project/{self._args.project}/statuses"
                response = self._jira._session.get(url)
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                project_statuses = response.json()
            except Exception as e:
                raise AssertionError(
                    f"Failed to retrieve statuses for project '{self._args.project}': {e}"
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
                if itype_name == self._args.type:
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
                assert self._args.status in valid_statuses, (
                    f"Status '{self._args.status}' is not valid for issue type '{self._args.type}' in project '{self._args.project}'. "
                    f"Valid statuses are: {', '.join(valid_statuses)}"
                )
            else:
                self._logger.warning(
                    f"Could not find status list for issue type '{self._args.type}' in project_statuses."
                )

        # 4. Security level validation
        security_is_default = False
        if self._args.security is None:
            self._args.security = "Red Hat Employee"
            security_is_default = True
            self._logger.info("Using global default for 'security': Red Hat Employee")

        self._resolved_security_id = None
        if self._args.security is not None and self._args.security != "":
            try:
                url = f"{self._jira._options['server']}/rest/api/2/project/{self._args.project}/securitylevel"
                response = self._jira._session.get(url)
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
                self._logger.warning(
                    f"Could not retrieve security levels for project {self._args.project}: {e}"
                )
                security_map = {}

            if self._args.security in security_map:
                self._resolved_security_id = security_map[self._args.security]
            else:
                if security_is_default:
                    # If it was just the global default fallback and it's not valid, clear it
                    self._args.security = ""
                else:
                    # If the user explicitly provided it, raise AssertionError with zero silent fallbacks
                    raise AssertionError(
                        f"Security level '{self._args.security}' is not valid for project '{self._args.project}' or could not be retrieved. "
                        f"Available levels: {', '.join(security_map.keys())}"
                    )

        # 5. Epic validation
        if self._args.epic is not None:
            try:
                self._logger.debug(f"Pre-validating epic: {self._args.epic}")
                self._jira.issue(self._args.epic, fields="summary")
            except Exception as e:
                raise AssertionError(
                    f"Epic issue '{self._args.epic}' not found or inaccessible: {e}"
                )

        # 6. Parent validation
        if self._args.parent is not None:
            try:
                self._logger.debug(f"Pre-validating parent: {self._args.parent}")
                self._jira.issue(self._args.parent, fields="issuetype")
            except Exception as e:
                raise AssertionError(
                    f"Parent issue '{self._args.parent}' not found or inaccessible: {e}"
                )

        # 7. Assignee validation
        resolved_assignee = None
        if self._args.assignee is not None:
            try:
                assignee_users = self._jira.search_users(
                    query=self._args.assignee,
                    includeActive=True,
                    includeInactive=False,
                )
            except Exception as e:
                raise AssertionError(
                    f"Failed to search for user '{self._args.assignee}': {e}"
                )

            # If we found multiple, try to find an exact match to be helpful
            if len(assignee_users) > 1:
                exact_matches = [
                    u
                    for u in assignee_users
                    if u.displayName == self._args.assignee
                    or getattr(u, "emailAddress", None) == self._args.assignee
                    or getattr(u, "accountId", None) == self._args.assignee
                    or getattr(u, "name", None) == self._args.assignee
                ]
                if len(exact_matches) == 1:
                    assignee_users = exact_matches

            assert len(assignee_users) == 1, (
                f"Expected exactly one user for '{self._args.assignee}', but found {len(assignee_users)}. "
                f"Please use a more specific name, email, or accountId. "
                f"Found: {[u.displayName + ' (' + getattr(u, 'accountId', 'no-id') + ')' for u in assignee_users]}"
            )
            resolved_assignee = assignee_users[0]
            self._logger.debug(f"Pre-validated assignee: {resolved_assignee}")

        # 8. Sprint validation
        resolved_sprint_id = None
        if (
            self._args.sprint is not None
            or (self._args.sprint_regexp is not None and self._args.sprint_regexp != "")
            or self._args.sprint_current
        ):
            sprints = self._list_sprints()

            if self._args.sprint is not None:
                matched_sprints = [i for i in sprints if i["name"] == self._args.sprint]
                assert len(matched_sprints) == 1, (
                    f"Expected exactly one sprint named '{self._args.sprint}', but found {len(matched_sprints)}."
                )
                resolved_sprint_id = matched_sprints[0]["id"]
            elif (
                self._args.sprint_regexp is not None and self._args.sprint_regexp != ""
            ):
                pattern = re.compile(self._args.sprint_regexp)
                matched_sprints = [
                    i
                    for i in sprints
                    if i["state"] == "active" and pattern.fullmatch(i["name"])
                ]
                assert len(matched_sprints) == 1, (
                    f"Expected exactly one active sprint matching regexp '{self._args.sprint_regexp}', but found {len(matched_sprints)}."
                )
                resolved_sprint_id = matched_sprints[0]["id"]
            elif self._args.sprint_current:
                assert self._args.project in self._config["sprint_regexps"], (
                    f"Project '{self._args.project}' is not configured in 'sprint_regexps' of config file."
                )
                pattern = re.compile(self._config["sprint_regexps"][self._args.project])
                matched_sprints = [
                    i
                    for i in sprints
                    if i["state"] == "active" and pattern.fullmatch(i["name"])
                ]
                assert len(matched_sprints) == 1, (
                    f"Expected exactly one active current sprint for project '{self._args.project}', but found {len(matched_sprints)}."
                )
                resolved_sprint_id = matched_sprints[0]["id"]

        # Create issue skeleton
        adf_description = json.loads(
            _translate_content("to-adf", self._args.description)
        )
        issue = {
            "issuetype": {"name": self._args.type},
            "project": self._args.project,
            "summary": self._args.summary,
            "description": adf_description,
        }

        # Set parent link (v3 unified parent field) for epic
        if self._args.epic is not None:
            issue["parent"] = {"key": self._args.epic}

        # Set parent link via --parent (v3 or legacy routing)
        if self._args.parent is not None:
            parent_field, parent_value = self._resolve_parent_field(self._args.type)
            issue[parent_field] = parent_value

        # Set security level if it was set
        if self._args.security is not None and self._args.security != "":
            issue["security"] = {"id": self._resolved_security_id}

        # Set components if it was set
        if self._args.components is not None:
            issue["components"] = [
                {"name": i} for i in self._args.components if i != ""
            ]

        # If creating epic, we need to define epic name
        if self._args.type == "Epic":
            issue[self._config["custom_fields"]["epic_name"]] = self._args.summary

        if self._args.dry_run:
            _pretty("Would create this issue now:", issue)
        else:
            issue = self._jira.create_issue(fields=issue)
            print(f"Created issue {issue.permalink()}")

        # Load assignee details and set it to issue
        if resolved_assignee is not None:
            if self._args.dry_run:
                _pretty("Would assign the issue to:", resolved_assignee)
            else:
                # In Jira Cloud, we must use accountId instead of name
                assignee_id = getattr(
                    resolved_assignee,
                    "accountId",
                    getattr(resolved_assignee, "name", None),
                )
                self._jira.assign_issue(issue, assignee_id)
                print(f"Assigned to {resolved_assignee.displayName} ({assignee_id})")

        # Transition issue to status
        self._update_status(issue)

        # Set custom fields and labels and possibly more
        self._update_fields(issue, resolved_sprint_id=resolved_sprint_id)

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

        assert not (self._args.parent is not None and self._args.epic is not None), (
            "Cannot specify both --parent and --epic; use --parent for unified hierarchy linking"
        )

        if self._args.parent is not None:
            try:
                self._logger.debug(f"Pre-validating parent: {self._args.parent}")
                self._jira.issue(self._args.parent, fields="issuetype")
            except Exception as e:
                raise AssertionError(
                    f"Parent issue '{self._args.parent}' not found or inaccessible: {e}"
                )

        for issue in issues:
            self._update_status(issue)

            if self._args.comment is not None:
                if self._args.dry_run:
                    _pretty("Would add this comment:", self._args.comment)
                else:
                    adf_comment = json.loads(
                        _translate_content("to-adf", self._args.comment)
                    )
                    self._jira.add_comment(issue, adf_comment)
                    print(f"Commented on the issue {issue.id}")

            # Update custom fields and labels and possibly more
            self._update_fields(issue)

    def do_sprints(self):
        if self._args.refresh:
            cache_path = Path("~/.jira-cli/sprints.json").expanduser()
            if cache_path.exists():
                cache_path.unlink()
            self._cache_sprints = Cache("~/.jira-cli/sprints.json")

        sprints = self._list_sprints()

        if self._args.board_id is not None:
            sprints = [s for s in sprints if s["board_id"] == self._args.board_id]

        if self._args.state != "all":
            sprints = [s for s in sprints if s["state"] == self._args.state]

        header = f"{'Board ID':<10} {'Sprint ID':<12} {'Sprint Name':<30} {'State'}"
        print(header)
        print("-" * len(header))
        for s in sprints:
            print(f"{s['board_id']:<10} {s['id']:<12} {s['name']:<30} {s['state']}")

    def do_view(self):
        self._logger.debug(f"Fetching issue: {self._args.issue_key}")
        issue = self._jira.issue(self._args.issue_key)

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
        custom_fields = self._config.get("custom_fields", {})
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
        if self._args.with_comments:
            raw_comments_list = (
                issue.raw.get("fields", {}).get("comment", {}).get("comments", [])
            )
            if hasattr(issue.fields, "comment") and hasattr(
                issue.fields.comment, "comments"
            ):
                for idx, comment in enumerate(issue.fields.comment.comments):
                    author = getattr(comment, "author", None)
                    author_name = (
                        getattr(author, "displayName", "Unknown")
                        if author
                        else "Unknown"
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

        if self._args.with_enrichment:
            texts = [description]
            for c in comments:
                texts.append(c["body"])
            enrichment = enrich_with_prs("\n".join(texts))
            if enrichment:
                print(thin_sep)
                print("Enrichment:")
                for item in enrichment:
                    print(f"- URL: {item['url']}:")
                    for line in item["info"].splitlines():
                        print(f"    {line}")

        print(separator)

        if self._args.dump:
            output_dir = Path("jira_issue_details")
            output_dir.mkdir(exist_ok=True)
            try:
                issue_data = issue.raw
                file_path = output_dir / f"issue-{issue.key}.json"
                with open(file_path, "w", encoding="utf-8") as fd:
                    json.dump(issue_data, fd, indent=4, sort_keys=False)
                self._logger.info(f"Saved details for issue {issue.key} to {file_path}")
            except Exception as e:
                self._logger.error(f"Could not save details for issue {issue.key}: {e}")

    def do_tempate(self):
        for name, data in self._config["issue_templates"].items():
            print(f"Template {name}")
            for k, v in data.items():
                if type(v) is list:
                    v = ", ".join(v)
                print(f"  {k}: {v}")


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
        help="Description text of a new ticket in Markdown format, if it starts with '@' it is considered a file to load it from",
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
        "--resolution",
        help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
    )
    parser_create.add_argument(
        "--type",
        choices=["Task", "Bug", "Epic", "Feature", "Sub-task"],
        default="Task",
        help="Issue type",
    )
    parser_create.add_argument(
        "--epic",
        help="Parent epic to put this ticket under",
    )
    parser_create.add_argument(
        "--parent",
        help="Parent issue key to link this issue under (unifies Epic Link, Parent Link, and Sub-task parents)",
    )
    parser_create.add_argument(
        "--story-points",
        type=float,
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
        "--sprint-current",
        action="store_true",
        help="Add to current sprint",
    )
    parser_create.add_argument(
        "--target-start",
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser_create.add_argument(
        "--target-end",
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )
    parser_create.add_argument(
        "--security",
        help="Security level of new issue (default 'Red Hat Employee', set to \"\" to omit security)",
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
        "--resolution",
        help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
    )
    parser_update.add_argument(
        "--comment",
        help="New comment to add in Markdown format (or set to '' to edit with editor)",
    )
    parser_update.add_argument(
        "--epic",
        help="Parent epic to put this ticket under",
    )
    parser_update.add_argument(
        "--parent",
        help="Parent issue key to link this issue under (unifies Epic Link, Parent Link, and Sub-task parents)",
    )
    parser_update.add_argument(
        "--story-points",
        type=float,
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
        "--sprint-current",
        action="store_true",
        help="Add to current sprint",
    )
    parser_update.add_argument(
        "--target-start",
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target start date (provide date in YYYY-MM-DD format)",
    )
    parser_update.add_argument(
        "--target-end",
        type=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"),
        help="Change target end date (provide date in YYYY-MM-DD format)",
    )
    parser_update.add_argument(
        "--labels",
        action="append",
        help='Label to add (can be specified multiple times, set to "" to ignore)',
    )

    #
    # Templates
    #
    subparsers.add_parser(
        "template",
        help="Work with issue templates",
    )

    #
    # Sprints
    #
    parser_sprints = subparsers.add_parser(
        "sprints",
        help="List sprints for a specific board or project",
    )
    parser_sprints.add_argument(
        "--board-id",
        help="Filter sprints by board ID",
        type=int,
    )
    parser_sprints.add_argument(
        "--state",
        choices=["active", "future", "closed", "all"],
        default="active",
        help="Filter sprints by state",
    )
    parser_sprints.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh the cached sprint data",
    )

    #
    # Viewing an issue
    #
    parser_view = subparsers.add_parser(
        "view",
        help="View details of a specific issue",
    )
    parser_view.add_argument(
        "issue_key",
        help="The Jira issue key to view (e.g., 'KONFLUX-123')",
        type=str,
    )
    parser_view.add_argument(
        "--with-comments",
        action="store_true",
        help="Include issue comments in the output",
    )
    parser_view.add_argument(
        "--with-enrichment",
        action="store_true",
        help="Fetch and display linked PR/commit/Slack details from GitHub/GitLab/Slack",
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
