#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
from unittest.mock import MagicMock, patch

from jira_cli.commands import update


def test_update_status_with_resolution(mock_ctx, mock_args):
    """When --resolution is passed, transition_issue receives fields with the resolution."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
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
    mock_args.description = None
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
    mock_args.description = None
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


@patch("jira_cli.commands.update._translate_content")
def test_update_converts_description_to_adf(mock_translate, mock_ctx, mock_args):
    """--description is translated to ADF and pushed via issue.update()."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = "my description"
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"my description"}]}]}'

    update.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-adf", "my description")
    update_call = mock_issue.update.call_args[1]["fields"]
    assert isinstance(update_call["description"], dict)
    assert update_call["description"]["type"] == "doc"


def test_update_with_link(mock_ctx, mock_args):
    """When --link-relationship and --link-target are set, create_issue_link is called."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False
    mock_args.link_relationship = "blocks"
    mock_args.link_target = "KONFLUX-100"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-42"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    update.run(mock_ctx, mock_args)

    mock_ctx.jira.create_issue_link.assert_called_once_with(
        "blocks", "KONFLUX-42", "KONFLUX-100"
    )


def test_update_link_requires_both_args(mock_ctx, mock_args):
    """Specifying only --link-target without --link-relationship raises AssertionError."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.link_relationship = None
    mock_args.link_target = "KONFLUX-100"

    with pytest.raises(AssertionError, match="must be specified together"):
        update.run(mock_ctx, mock_args)


def test_update_add_labels(mock_ctx, mock_args):
    """--add-labels appends labels to existing ones."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False
    mock_args.add_labels = ["new-label", "another"]

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = ["existing"]
    mock_ctx.jira.issue.return_value = mock_issue

    update.run(mock_ctx, mock_args)

    update_call = mock_issue.update.call_args[1]["fields"]
    assert update_call["labels"] == ["existing", "new-label", "another"]


def test_update_assignee_validation_failure(mock_ctx, mock_args):
    """When --assignee matches no users, an AssertionError is raised."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False

    mock_ctx.jira.search_users.return_value = []
    mock_args.assignee = "nonexistent-user"

    with pytest.raises(AssertionError) as exc_info:
        update.run(mock_ctx, mock_args)

    assert "Expected exactly one user for 'nonexistent-user', but found 0" in str(
        exc_info.value
    )


def test_update_assignee_success(mock_ctx, mock_args):
    """When --assignee resolves to exactly one user, assign_issue is called."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    mock_user = MagicMock()
    mock_user.displayName = "Test User"
    mock_user.accountId = "user-id-123"
    mock_ctx.jira.search_users.return_value = [mock_user]
    mock_args.assignee = "test-user"

    update.run(mock_ctx, mock_args)

    mock_ctx.jira.assign_issue.assert_called_once_with(mock_issue, "user-id-123")


def test_update_remove_labels(mock_ctx, mock_args):
    """--remove-labels removes matching labels from existing ones."""
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False
    mock_args.remove_labels = ["to-remove"]

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = ["keep", "to-remove", "also-keep"]
    mock_ctx.jira.issue.return_value = mock_issue

    update.run(mock_ctx, mock_args)

    update_call = mock_issue.update.call_args[1]["fields"]
    assert update_call["labels"] == ["keep", "also-keep"]


@patch("builtins.open")
@patch("jira_cli.commands.update._translate_content")
def test_update_comment_from_file(mock_translate, mock_open, mock_ctx, mock_args):
    """When --comment starts with '@', it reads the comment from the specified file."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = "@my_comment_file.txt"
    mock_args.description = None
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    # Mock open and read
    mock_file = MagicMock()
    mock_file.read.return_value = "comment content from file"
    mock_open.return_value = mock_file

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"comment content from file"}]}]}'

    update.run(mock_ctx, mock_args)

    mock_open.assert_called_once_with("my_comment_file.txt", "r")
    mock_translate.assert_called_once_with("to-adf", "comment content from file")


@patch("builtins.open")
@patch("jira_cli.commands.update._translate_content")
def test_update_description_from_file(mock_translate, mock_open, mock_ctx, mock_args):
    """When --description starts with '@', it reads the description from the specified file."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = "@my_description_file.txt"
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    # Mock open and read
    mock_file = MagicMock()
    mock_file.read.return_value = "description content from file"
    mock_open.return_value = mock_file

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"description content from file"}]}]}'

    update.run(mock_ctx, mock_args)

    mock_open.assert_called_once_with("my_description_file.txt", "r")
    mock_translate.assert_called_once_with("to-adf", "description content from file")


def test_update_sets_team_custom_field(mock_ctx, mock_args):
    """When --team is passed, the issue is updated with the team custom field."""
    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = None
    mock_args.description = None
    mock_args.status = None
    mock_args.resolution = None
    mock_args.team = "lightwell-performance"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.issue.return_value = mock_issue

    update.run(mock_ctx, mock_args)

    update_fields = mock_issue.update.call_args[1]["fields"]
    assert update_fields["customfield_10007"] == {"value": "lightwell-performance"}
