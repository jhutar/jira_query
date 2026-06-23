#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import json
import os
import re
from pathlib import Path


class Cache:
    """File-based JSON cache with mtime-based version tracking."""

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


class SprintResolver:
    def __init__(self, config, jira, logger):
        self._config = config
        self._jira = jira
        self._logger = logger
        Path("~/.jira-cli/").expanduser().mkdir(exist_ok=True)
        self._cache = Cache("~/.jira-cli/sprints.json")

    def refresh(self):
        cache_path = Path("~/.jira-cli/sprints.json").expanduser()
        if cache_path.exists():
            cache_path.unlink()
        self._cache = Cache("~/.jira-cli/sprints.json")

    def list_sprints(self):
        if not self._cache.obsolete():
            self._logger.debug("Using sprint data from cache")
            return self._cache.get()

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

        self._cache.set(sprints)
        return sprints

    def resolve(
        self, sprint=None, sprint_regexp=None, sprint_current=False, project=None
    ):
        sprints = self.list_sprints()

        if sprint is not None:
            matched = [i for i in sprints if i["name"] == sprint]
            assert len(matched) == 1, (
                f"Expected exactly one sprint named '{sprint}', but found {len(matched)}."
            )
            return matched[0]["id"]

        if sprint_regexp is not None and sprint_regexp != "":
            pattern = re.compile(sprint_regexp)
            matched = [
                i
                for i in sprints
                if i["state"] == "active" and pattern.fullmatch(i["name"])
            ]
            assert len(matched) == 1, (
                f"Expected exactly one active sprint matching regexp '{sprint_regexp}', but found {len(matched)}."
            )
            return matched[0]["id"]

        if sprint_current:
            assert project is not None, "Project is required for sprint_current"
            assert project in self._config["sprint_regexps"], (
                f"Project '{project}' is not configured in 'sprint_regexps' of config file."
            )
            pattern = re.compile(self._config["sprint_regexps"][project])
            matched = [
                i
                for i in sprints
                if i["state"] == "active" and pattern.fullmatch(i["name"])
            ]
            assert len(matched) == 1, (
                f"Expected exactly one active current sprint for project '{project}', but found {len(matched)}."
            )
            return matched[0]["id"]

        return None
