#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import pytest
from unittest.mock import MagicMock, patch, mock_open

# Import the dash-containing module dynamically
jira_cli = __import__("jira-cli")


@pytest.fixture
def mock_config():
    return {
        "server": {
            "url": "https://jira.example.com",
            "auth": {"basic_auth": {"username": "user", "token": "token"}},
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
    args.type = "Task"
    args.epic = None
    args.story_points = None
    args.sprint = None
    args.sprint_regexp = None
    args.sprint_current = False
    args.target_start = None
    args.target_end = None
    args.security = None
    args.dry_run = True
    return args


@patch("jira-cli._load_config")
@patch("jira-cli._create_jira_client")
def test_do_create_project_validation_failure(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Make project fetch raise an exception (project doesn't exist)
    mock_jira.project.side_effect = Exception("Project not found")

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Project 'KONFLUX' does not exist or is inaccessible" in str(exc_info.value)


@patch("jira-cli._load_config")
@patch("jira-cli._create_jira_client")
def test_do_create_issue_type_validation_failure(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Project exists but returns no issue types
    mock_project = MagicMock()
    mock_project.issueTypes = []
    mock_jira.project.return_value = mock_project

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Issue type 'Task' is not valid for project 'KONFLUX'" in str(exc_info.value)


@patch("jira-cli._load_config")
@patch("jira-cli._create_jira_client")
def test_do_create_status_validation_failure(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Set up mock project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Set up mock project statuses via REST endpoint mock
    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Task", "statuses": [{"name": "New"}]}]
    mock_jira._session.get.return_value = mock_response

    # Set invalid status in args
    mock_args.status = "InvalidStatus"

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert (
        "Status 'InvalidStatus' is not valid for issue type 'Task' in project 'KONFLUX'"
        in str(exc_info.value)
    )


@patch("jira-cli._load_config")
@patch("jira-cli._create_jira_client")
def test_do_create_assignee_validation_failure(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Assignee search returns 0 matches
    mock_jira.search_users.return_value = []
    mock_args.assignee = "nonexistent-user"

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Expected exactly one user for 'nonexistent-user', but found 0" in str(
        exc_info.value
    )


@patch("jira-cli._load_config")
@patch("jira-cli._create_jira_client")
def test_do_create_valid_validation_flow(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Setup status via REST endpoint mock
    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Task", "statuses": [{"name": "New"}]}]
    mock_jira._session.get.return_value = mock_response

    # Setup security levels
    mock_sec_level = MagicMock()
    mock_sec_level.name = "Red Hat Employee"
    mock_jira.project_issue_security_level.return_value = [mock_sec_level]

    # Setup assignee
    mock_user = MagicMock()
    mock_user.displayName = "Test User"
    mock_user.accountId = "user-id-123"
    mock_jira.search_users.return_value = [mock_user]

    mock_args.status = "New"
    mock_args.security = "Red Hat Employee"
    mock_args.assignee = "test-user"

    doer = jira_cli.Doer(mock_args)
    issue = doer.do_create()

    # In dry-run mode, it shouldn't call create_issue but should validate everything
    assert mock_jira.project.called
    assert mock_jira._session.get.called
    assert mock_jira.project_issue_security_level.called
    assert mock_jira.search_users.called
    assert not mock_jira.create_issue.called
