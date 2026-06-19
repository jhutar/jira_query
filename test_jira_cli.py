#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
from unittest.mock import MagicMock, patch

# Import the dash-containing module dynamically
jira_cli = __import__("jira-cli")


@patch("jira.JIRA")
def test_create_jira_client_uses_v3(mock_jira_class):
    jira_cli._create_jira_client("https://jira.example.com", "user", "token")
    mock_jira_class.assert_called_once_with(
        options={"server": "https://jira.example.com", "rest_api_version": "3"},
        basic_auth=("user", "token"),
    )


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
    args.parent = None
    args.story_points = None
    args.sprint = None
    args.sprint_regexp = None
    args.sprint_current = False
    args.target_start = None
    args.target_end = None
    args.security = None
    args.dry_run = True
    return args


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
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


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
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


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
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


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
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


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
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
    doer.do_create()

    # In dry-run mode, it shouldn't call create_issue but should validate everything
    assert mock_jira.project.called
    assert mock_jira._session.get.called
    assert mock_jira.project_issue_security_level.called
    assert mock_jira.search_users.called
    assert not mock_jira.create_issue.called


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_uses_parent_field_for_epic(
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

    # Setup epic validation
    mock_jira.issue.return_value = MagicMock()

    # Set epic and disable dry_run to actually call create_issue
    mock_args.epic = "KONFLUX-100"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    # Verify create_issue was called with parent field (v3 format)
    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert "parent" in create_call_fields
    assert create_call_fields["parent"] == {"key": "KONFLUX-100"}


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_validation_failure(
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

    # Parent issue lookup fails
    mock_jira.issue.side_effect = Exception("Issue not found")
    mock_args.parent = "NONEXIST-999"

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Parent issue 'NONEXIST-999' not found or inaccessible" in str(
        exc_info.value
    )


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_uses_parent_field_v3(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """When --parent is specified under v3 config, payload contains parent: {key: ...}."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Parent issue lookup succeeds
    mock_jira.issue.return_value = MagicMock()

    mock_args.parent = "PARENT-123"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert "parent" in create_call_fields
    assert create_call_fields["parent"] == {"key": "PARENT-123"}


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_legacy_fallback_epic_link(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """When config has parent_link and issue type is Task, --parent routes to Epic Link custom field."""
    mock_config["custom_fields"]["parent_link"] = "customfield_10018"
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Parent issue lookup succeeds
    mock_jira.issue.return_value = MagicMock()

    mock_args.parent = "EPIC-100"
    mock_args.type = "Task"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    # Should use Epic Link custom field, not v3 parent
    assert "parent" not in create_call_fields
    assert create_call_fields["customfield_10001"] == "EPIC-100"


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_legacy_fallback_parent_link(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """When config has parent_link and issue type is Epic, --parent routes to Parent Link custom field."""
    mock_config["custom_fields"]["parent_link"] = "customfield_10018"
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Epic"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Parent issue lookup succeeds
    mock_jira.issue.return_value = MagicMock()

    mock_args.parent = "FEATURE-50"
    mock_args.type = "Epic"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["customfield_10018"] == "FEATURE-50"


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_and_epic_conflict(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.parent = "PARENT-1"
    mock_args.epic = "EPIC-1"

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Cannot specify both --parent and --epic" in str(exc_info.value)
