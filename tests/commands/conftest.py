#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

import pytest
from unittest.mock import MagicMock

from jira_cli.context import Context


@pytest.fixture
def mock_config():
    return {
        "server": {
            "url": "https://jira.example.com",
            "auth": {"basic_auth": {"username": "user", "token": "token"}},  # nosec B105
        },
        "custom_fields": {
            "epic": "customfield_10001",
            "story_points": "customfield_10002",
            "target_start": "customfield_10003",
            "target_end": "customfield_10004",
            "sprint": "customfield_10005",
            "epic_name": "customfield_10006",
        },
        "sprint_regexps": {"KONFLUX": r"Konflux Sprint \d+"},
        "issue_templates": {},
    }


@pytest.fixture
def mock_jira():
    return MagicMock()


@pytest.fixture
def mock_ctx(mock_config, mock_jira):
    return Context(
        config=mock_config,
        jira=mock_jira,
        logger=logging.getLogger("test"),
    )


@pytest.fixture
def mock_args():
    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.template = None
    args.project = "KONFLUX"
    args.summary = "Test issue"
    args.description = "Test description"
    args.assignee = None
    args.components = None
    args.labels = None
    args.status = None
    args.resolution = None
    args.type = "Task"
    args.epic = None
    args.parent = None
    args.story_points = None
    args.sprint = None
    args.sprint_regexp = None
    args.sprint_current = False
    args.target_start = None
    args.target_end = None
    args.security = None
    args.dry_run = True
    args.dump = False
    args.link_relationship = None
    args.link_target = None
    return args
