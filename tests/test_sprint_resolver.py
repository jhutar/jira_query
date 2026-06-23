#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

import pytest
from unittest.mock import MagicMock, patch

from jira_cli.sprint_resolver import SprintResolver


MOCK_SPRINTS = [
    {"board_id": 6067, "id": 12040, "name": "Konflux Sprint 10", "state": "active"},
    {"board_id": 6067, "id": 12041, "name": "Konflux Sprint 11", "state": "future"},
    {"board_id": 10332, "id": 13251, "name": "Sat Sprint 84", "state": "active"},
    {"board_id": 10332, "id": 13200, "name": "Sat Sprint 83", "state": "closed"},
]

CONFIG = {
    "sprint_regexps": {"KONFLUX": r"Konflux Sprint \d+"},
}


@pytest.fixture
def resolver():
    r = SprintResolver(CONFIG, MagicMock(), logging.getLogger("test"))
    r._cache = MagicMock()
    r._cache.obsolete.return_value = False
    r._cache.get.return_value = MOCK_SPRINTS
    return r


def test_resolve_by_exact_name(resolver):
    sprint_id = resolver.resolve(sprint="Konflux Sprint 10")
    assert sprint_id == 12040


def test_resolve_by_exact_name_no_match(resolver):
    with pytest.raises(AssertionError, match="Expected exactly one sprint named"):
        resolver.resolve(sprint="Nonexistent Sprint")


def test_resolve_by_regexp(resolver):
    sprint_id = resolver.resolve(sprint_regexp=r"Sat Sprint \d+")
    assert sprint_id == 13251


def test_resolve_by_regexp_no_match(resolver):
    with pytest.raises(AssertionError, match="Expected exactly one active sprint matching"):
        resolver.resolve(sprint_regexp=r"Nonexistent \d+")


def test_resolve_current(resolver):
    sprint_id = resolver.resolve(sprint_current=True, project="KONFLUX")
    assert sprint_id == 12040


def test_resolve_current_no_project_config(resolver):
    with pytest.raises(AssertionError, match="not configured in 'sprint_regexps'"):
        resolver.resolve(sprint_current=True, project="UNKNOWN")


def test_resolve_none_returns_none(resolver):
    assert resolver.resolve() is None
