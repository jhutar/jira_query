#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess

import pytest
from unittest.mock import MagicMock, patch

import jira_cli.cli as jira_cli
from jira_cli.context import _create_jira_client


@patch("jira.JIRA")
def test_create_jira_client_uses_v3(mock_jira_class):
    _create_jira_client("https://jira.example.com", "user", "token")
    mock_jira_class.assert_called_once_with(
        options={"server": "https://jira.example.com", "rest_api_version": "3"},
        basic_auth=("user", "token"),
    )


@patch("subprocess.run")
def test_translate_content_to_adf(mock_run):
    mock_run.return_value = MagicMock(
        stdout='{"type": "doc", "content": []}\n',
    )
    result = jira_cli._translate_content("to-adf", "hello")
    mock_run.assert_called_once_with(
        ["adfmd", "to-adf"],
        input="hello",
        capture_output=True,
        text=True,
        check=True,
    )
    assert result == '{"type": "doc", "content": []}'


@patch("subprocess.run")
def test_translate_content_to_md(mock_run):
    mock_run.return_value = MagicMock(stdout="# Hello\n")
    result = jira_cli._translate_content("to-md", '{"type":"doc"}')
    mock_run.assert_called_once_with(
        ["adfmd", "to-md"],
        input='{"type":"doc"}',
        capture_output=True,
        text=True,
        check=True,
    )
    assert result == "# Hello"


@patch("subprocess.run")
def test_translate_content_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd=["adfmd", "to-adf"], stderr="parse error"
    )
    with pytest.raises(RuntimeError, match="Content translation failed"):
        jira_cli._translate_content("to-adf", "bad input")


@patch.object(jira_cli, "_translate_content")
def test_convert_issue_adf_to_md(mock_translate):
    """Test convert_issue_adf_to_md translates raw ADF fields in place."""
    mock_translate.return_value = "Translated markdown text"

    mock_issue = MagicMock()
    mock_issue.raw = {
        "fields": {
            "description": {"type": "doc", "version": 1, "content": []},
            "comment": {
                "comments": [{"body": {"type": "doc", "version": 1, "content": []}}]
            },
        }
    }

    mock_comment = MagicMock()
    mock_comment.body = "raw adf body"

    mock_issue.fields = MagicMock()
    mock_issue.fields.description = "raw adf desc"
    mock_issue.fields.comment = MagicMock()
    mock_issue.fields.comment.comments = [mock_comment]

    jira_cli.convert_issue_adf_to_md(mock_issue)

    assert mock_issue.fields.description == "Translated markdown text"
    assert mock_comment.body == "Translated markdown text"
    assert mock_translate.call_count == 2
