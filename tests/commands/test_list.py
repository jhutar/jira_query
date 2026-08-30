#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from pathlib import Path

from unittest.mock import MagicMock, patch

from jira_cli.cli import default_template_path
from jira_cli.commands import list as list_cmd


def test_default_template_path_resolves_to_existing_file():
    """Default template must resolve to a file present at runtime."""
    tmpl = Path(default_template_path())
    if not tmpl.is_absolute():
        tmpl = Path.cwd() / tmpl
    assert tmpl.is_file()


@patch("jira_cli.commands.list._translate_content")
def test_list_converts_adf_description_to_md(mock_translate, mock_ctx, mock_args):
    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False
    mock_args.template = "templates/default.md.j2"

    adf_desc = {"type": "doc", "content": []}
    mock_issue = MagicMock()
    mock_issue.fields.description = adf_desc
    mock_issue.fields.comment.comments = []
    mock_ctx.jira.search_issues.return_value = [mock_issue]

    mock_translate.return_value = "# Converted"

    list_cmd.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    assert mock_issue.fields.description == "# Converted"


@patch("jira_cli.commands.list._translate_content")
def test_list_converts_adf_comment_to_md(mock_translate, mock_ctx, mock_args):
    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False
    mock_args.template = "templates/default.md.j2"

    adf_body = {"type": "doc", "content": []}
    mock_comment = MagicMock()
    mock_comment.body = adf_body

    mock_issue = MagicMock()
    mock_issue.fields.description = "plain text"
    mock_issue.fields.comment.comments = [mock_comment]
    mock_ctx.jira.search_issues.return_value = [mock_issue]

    mock_translate.return_value = "comment in markdown"

    list_cmd.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_body))
    assert mock_comment.body == "comment in markdown"


@patch("jira_cli.commands.list._translate_content")
def test_list_skips_string_description(mock_translate, mock_ctx, mock_args):
    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False
    mock_args.template = "templates/default.md.j2"

    mock_issue = MagicMock()
    mock_issue.fields.description = "already a string"
    mock_issue.fields.comment.comments = []
    mock_ctx.jira.search_issues.return_value = [mock_issue]

    list_cmd.run(mock_ctx, mock_args)

    mock_translate.assert_not_called()
    assert mock_issue.fields.description == "already a string"
