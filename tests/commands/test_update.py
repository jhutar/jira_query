#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from unittest.mock import MagicMock, patch

from jira_cli.commands import update


def test_update_status_with_resolution(mock_ctx, mock_args):
    """When --resolution is passed, transition_issue receives fields with the resolution."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.status = "Closed"
    mock_args.resolution = "Done"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    mock_ctx.jira.transitions.return_value = [
        {"name": "Closed", "id": "501"},
    ]

    update.run(mock_ctx, mock_args)

    mock_ctx.jira.transition_issue.assert_called_once_with(
        mock_issue,
        "501",
        fields={"resolution": {"name": "Done"}},
    )


def test_update_status_without_resolution(mock_ctx, mock_args):
    """When --resolution is not passed, transition_issue is called without fields."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.status = "In Progress"
    mock_args.resolution = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    mock_ctx.jira.transitions.return_value = [
        {"name": "In Progress", "id": "301"},
    ]

    update.run(mock_ctx, mock_args)

    mock_ctx.jira.transition_issue.assert_called_once_with(mock_issue, "301")


@patch("jira_cli.commands.update._translate_content")
def test_update_converts_comment_to_adf(mock_translate, mock_ctx, mock_args):
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = "my comment"
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"my comment"}]}]}'

    update.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-adf", "my comment")
    add_comment_call = mock_ctx.jira.add_comment.call_args
    assert isinstance(add_comment_call[0][1], dict)
    assert add_comment_call[0][1]["type"] == "doc"
