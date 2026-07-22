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


def test_get_default_config_path(tmp_path):
    from jira_cli.context import get_default_config_path

    # With XDG_CONFIG_HOME set
    with patch.dict("os.environ", {"XDG_CONFIG_HOME": str(tmp_path)}):
        path = get_default_config_path()
        assert path == str(tmp_path / "jira-cli" / "config.yaml")

    # Without XDG_CONFIG_HOME set
    with patch.dict("os.environ", {}, clear=True):
        path = get_default_config_path()
        assert "jira-cli/config.yaml" in path


def test_load_config_missing_raises_setup_hint(tmp_path):
    from jira_cli.context import load_config, JiraQueryError

    missing_path = tmp_path / "non_existent.yaml"
    with pytest.raises(JiraQueryError) as exc_info:
        load_config(missing_path)

    assert "Configuration file not found" in str(exc_info.value)
    assert "jira-cli setup" in str(exc_info.value)


@patch("builtins.input")
def test_setup_wizard_writes_config(mock_input, tmp_path):
    from jira_cli.commands.setup import run as setup_run
    import yaml

    # Mock inputs: instance URL, username, token
    mock_input.side_effect = [
        "https://test.jira.instance/",
        "test-user",
        "test-token",
    ]

    target_config = tmp_path / "jira-cli" / "config.yaml"
    mock_args = MagicMock()
    mock_args.config = str(target_config)

    setup_run(None, mock_args)

    # Verify directory was created and file was written
    assert target_config.is_file()

    # Load and verify content
    with open(target_config, "r", encoding="utf-8") as fd:
        data = yaml.safe_load(fd)

    assert data["server"]["url"] == "https://test.jira.instance/"
    assert data["server"]["auth"]["basic_auth"]["username"] == "test-user"
    assert data["server"]["auth"]["basic_auth"]["token"] == "test-token"
    assert data["boards_list"] == [
        "Konflux/RHTAP Perf&Scale board",
        "Pipelines Perf&Scale board",
        "Perf&Scale Infra tasks",
        "HCE Perf sprint board",
        "Satellite Perf&Scale scrum board",
    ]
    assert data["issue_templates"] == {}
    assert data["project_defaults"]["KONFLUX"]["type"] == "Task"
    assert data["custom_fields"]["epic"] == "customfield_10014"
    assert data["sprint_regexps"]["KONFLUX"] == "Konflux perf&scale sprint [0-9]+"
