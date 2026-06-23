#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pathlib import Path

from unittest.mock import MagicMock, patch

from jira_cli.commands import sprints
from jira_cli.sprint_resolver import Cache, SprintResolver


MOCK_SPRINTS = [
    {"board_id": 6067, "id": 12040, "name": "Konflux Sprint 10", "state": "active"},
    {"board_id": 6067, "id": 12041, "name": "Konflux Sprint 11", "state": "future"},
    {"board_id": 10332, "id": 13251, "name": "Sat Sprint 84", "state": "active"},
    {"board_id": 10332, "id": 13200, "name": "Sat Sprint 83", "state": "closed"},
]


def test_sprints_filter_by_state_active(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "sprints"
    mock_args.board_id = None
    mock_args.state = "active"
    mock_args.refresh = False

    with patch.object(SprintResolver, "list_sprints", return_value=MOCK_SPRINTS):
        sprints.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Konflux Sprint 10" in output
    assert "Sat Sprint 84" in output
    assert "Konflux Sprint 11" not in output
    assert "Sat Sprint 83" not in output


def test_sprints_filter_by_board_id(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "sprints"
    mock_args.board_id = 6067
    mock_args.state = "all"
    mock_args.refresh = False

    with patch.object(SprintResolver, "list_sprints", return_value=MOCK_SPRINTS):
        sprints.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Konflux Sprint 10" in output
    assert "Konflux Sprint 11" in output
    assert "Sat Sprint 84" not in output
    assert "Sat Sprint 83" not in output


def test_sprints_filter_by_board_id_and_state(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "sprints"
    mock_args.board_id = 10332
    mock_args.state = "closed"
    mock_args.refresh = False

    with patch.object(SprintResolver, "list_sprints", return_value=MOCK_SPRINTS):
        sprints.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Sat Sprint 83" in output
    assert "Sat Sprint 84" not in output
    assert "Konflux Sprint" not in output


def test_sprints_refresh_deletes_cache(mock_ctx, mock_args, tmp_path):
    mock_args.subparser_name = "sprints"
    mock_args.board_id = None
    mock_args.state = "all"
    mock_args.refresh = True

    with patch.object(SprintResolver, "list_sprints", return_value=[]):
        with patch.object(SprintResolver, "refresh") as mock_refresh:
            sprints.run(mock_ctx, mock_args)

    mock_refresh.assert_called_once()
