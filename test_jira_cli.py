#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import subprocess

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


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_subtask_requires_parent(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """Creating a Sub-task without --parent must raise AssertionError."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.type = "Sub-task"
    mock_args.parent = None

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert (
        "A parent issue key (via --parent) is required when creating a Sub-task."
        in str(exc_info.value)
    )


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_subtask_with_parent_passes_validation(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """Creating a Sub-task with --parent should pass the Sub-task validation."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.type = "Sub-task"
    mock_args.parent = "KONFLUX-200"

    # Setup valid project and issue types (including Sub-task)
    mock_itype_subtask = MagicMock()
    mock_itype_subtask.name = "Sub-task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype_subtask]
    mock_jira.project.return_value = mock_project

    # Parent issue lookup succeeds
    mock_jira.issue.return_value = MagicMock()

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    # dry_run is True, so create_issue should not be called, but validation passed
    assert not mock_jira.create_issue.called


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_feature_type_accepted(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """Feature issue type should pass issue type validation when project supports it."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.type = "Feature"

    # Setup valid project with Feature issue type
    mock_itype_feature = MagicMock()
    mock_itype_feature.name = "Feature"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype_feature]
    mock_jira.project.return_value = mock_project

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    # dry_run is True, so create_issue should not be called, but validation passed
    assert not mock_jira.create_issue.called


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_update_status_with_resolution(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """When --resolution is passed, transition_issue receives fields with the resolution."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

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
    mock_jira.issue.return_value = mock_issue

    mock_jira.transitions.return_value = [
        {"name": "Closed", "id": "501"},
    ]

    doer = jira_cli.Doer(mock_args)
    doer.do_update()

    mock_jira.transition_issue.assert_called_once_with(
        mock_issue,
        "501",
        fields={"resolution": {"name": "Done"}},
    )


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_update_status_without_resolution(
    mock_create_client, mock_load_config_fn, mock_config, mock_args
):
    """When --resolution is not passed, transition_issue is called without fields."""
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

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
    mock_jira.issue.return_value = mock_issue

    mock_jira.transitions.return_value = [
        {"name": "In Progress", "id": "301"},
    ]

    doer = jira_cli.Doer(mock_args)
    doer.do_update()

    mock_jira.transition_issue.assert_called_once_with(mock_issue, "301")


MOCK_SPRINTS = [
    {"board_id": 6067, "id": 12040, "name": "Konflux Sprint 10", "state": "active"},
    {"board_id": 6067, "id": 12041, "name": "Konflux Sprint 11", "state": "future"},
    {"board_id": 10332, "id": 13251, "name": "Sat Sprint 84", "state": "active"},
    {"board_id": 10332, "id": 13200, "name": "Sat Sprint 83", "state": "closed"},
]


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_state_active(
    mock_create_client, mock_load_config_fn, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "sprints"
    args.board_id = None
    args.state = "active"
    args.refresh = False

    doer = jira_cli.Doer(args)
    doer._cache_sprints = MagicMock()
    doer._cache_sprints.obsolete.return_value = False
    doer._cache_sprints.get.return_value = MOCK_SPRINTS

    doer.do_sprints()

    output = capsys.readouterr().out
    assert "Konflux Sprint 10" in output
    assert "Sat Sprint 84" in output
    assert "Konflux Sprint 11" not in output
    assert "Sat Sprint 83" not in output


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_board_id(
    mock_create_client, mock_load_config_fn, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "sprints"
    args.board_id = 6067
    args.state = "all"
    args.refresh = False

    doer = jira_cli.Doer(args)
    doer._cache_sprints = MagicMock()
    doer._cache_sprints.obsolete.return_value = False
    doer._cache_sprints.get.return_value = MOCK_SPRINTS

    doer.do_sprints()

    output = capsys.readouterr().out
    assert "Konflux Sprint 10" in output
    assert "Konflux Sprint 11" in output
    assert "Sat Sprint 84" not in output
    assert "Sat Sprint 83" not in output


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_board_id_and_state(
    mock_create_client, mock_load_config_fn, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "sprints"
    args.board_id = 10332
    args.state = "closed"
    args.refresh = False

    doer = jira_cli.Doer(args)
    doer._cache_sprints = MagicMock()
    doer._cache_sprints.obsolete.return_value = False
    doer._cache_sprints.get.return_value = MOCK_SPRINTS

    doer.do_sprints()

    output = capsys.readouterr().out
    assert "Sat Sprint 83" in output
    assert "Sat Sprint 84" not in output
    assert "Konflux Sprint" not in output


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_refresh_deletes_cache(
    mock_create_client, mock_load_config_fn, mock_config, tmp_path
):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "sprints"
    args.board_id = None
    args.state = "all"
    args.refresh = True

    doer = jira_cli.Doer(args)

    cache_file = tmp_path / "sprints.json"
    cache_file.write_text("[]")
    doer._cache_sprints = jira_cli.Cache(str(cache_file))

    with patch.object(jira_cli.Path, "expanduser", return_value=cache_file):
        with patch.object(doer, "_list_sprints", return_value=[]):
            doer.do_sprints()

    assert not cache_file.exists()


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_execute_dispatch(
    mock_create_client, mock_load_config_fn, mock_config
):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "sprints"

    doer = jira_cli.Doer(args)

    with patch.object(doer, "do_sprints") as mock_do_sprints:
        doer.execute()

    mock_do_sprints.assert_called_once()


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
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_converts_description_to_adf(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Test description"}]}]}'

    mock_args.dry_run = False
    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    mock_translate.assert_called_once_with("to-adf", "Test description")
    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert isinstance(create_call_fields["description"], dict)
    assert create_call_fields["description"]["type"] == "doc"


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_update_converts_comment_to_adf(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "update"
    mock_args.issue = "KONFLUX-42"
    mock_args.query = None
    mock_args.comment = "my comment"
    mock_args.status = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.issue.return_value = mock_issue

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"my comment"}]}]}'

    doer = jira_cli.Doer(mock_args)
    doer.do_update()

    mock_translate.assert_called_once_with("to-adf", "my comment")
    add_comment_call = mock_jira.add_comment.call_args
    assert isinstance(add_comment_call[0][1], dict)
    assert add_comment_call[0][1]["type"] == "doc"


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_converts_adf_description_to_md(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False

    adf_desc = {"type": "doc", "content": []}
    mock_issue = MagicMock()
    mock_issue.fields.description = adf_desc
    mock_issue.fields.comment.comments = []
    mock_jira.search_issues.return_value = [mock_issue]

    mock_translate.return_value = "# Converted"

    doer = jira_cli.Doer(mock_args)
    doer.do_list()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    assert mock_issue.fields.description == "# Converted"


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_converts_adf_comment_to_md(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False

    adf_body = {"type": "doc", "content": []}
    mock_comment = MagicMock()
    mock_comment.body = adf_body

    mock_issue = MagicMock()
    mock_issue.fields.description = "plain text"
    mock_issue.fields.comment.comments = [mock_comment]
    mock_jira.search_issues.return_value = [mock_issue]

    mock_translate.return_value = "comment in markdown"

    doer = jira_cli.Doer(mock_args)
    doer.do_list()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_body))
    assert mock_comment.body == "comment in markdown"


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_prints_issue_details(
    mock_create_client, mock_load_config_fn, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-123"
    args.dump = False

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-123"
    mock_issue.fields.summary = "Investigate Pipeline performance issues"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "In Progress"
    mock_issue.fields.assignee.displayName = "John Doe"
    mock_issue.fields.assignee.emailAddress = "john.doe@redhat.com"
    mock_issue.fields.reporter.displayName = "Jane Smith"
    mock_issue.fields.priority.name = "Major"
    mock_issue.fields.description = "Plain text description"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", 5.0)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    doer = jira_cli.Doer(args)
    doer.do_view()

    output = capsys.readouterr().out
    assert "KONFLUX-123" in output
    assert "In Progress" in output
    assert "Task" in output
    assert "Points: 5.0" in output
    assert "Investigate Pipeline performance issues" in output
    assert "John Doe (john.doe@redhat.com)" in output
    assert "Jane Smith" in output
    assert "Major" in output
    assert "Plain text description" in output


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_converts_adf_description(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-456"
    args.dump = False

    adf_desc = {"type": "doc", "content": []}
    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-456"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Bug"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = adf_desc
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    mock_translate.return_value = "Converted markdown description"

    doer = jira_cli.Doer(args)
    doer.do_view()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    output = capsys.readouterr().out
    assert "Converted markdown description" in output
    assert "Unassigned" in output


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_converts_adf_comments(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, capsys
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-789"
    args.dump = False

    adf_body = {"type": "doc", "content": []}
    mock_comment = MagicMock()
    mock_comment.author.displayName = "Alice"
    mock_comment.created = "2026-06-18T14:20:00.000+0000"
    mock_comment.body = adf_body

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-789"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    mock_translate.return_value = "Comment in markdown"

    doer = jira_cli.Doer(args)
    doer.do_view()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_body))
    output = capsys.readouterr().out
    assert "Alice" in output
    assert "Comment in markdown" in output


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_execute_dispatch(mock_create_client, mock_load_config_fn, mock_config):
    mock_load_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"

    doer = jira_cli.Doer(args)

    with patch.object(doer, "do_view") as mock_do_view:
        doer.execute()

    mock_do_view.assert_called_once()


@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_dump_writes_json(
    mock_create_client, mock_load_config_fn, mock_config, tmp_path
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-100"
    args.dump = True

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-100"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_issue.raw = {"key": "KONFLUX-100", "fields": {}}
    mock_jira.issue.return_value = mock_issue

    doer = jira_cli.Doer(args)

    with patch.object(jira_cli.Path, "__new__", wraps=jira_cli.Path):
        doer.do_view()

    output_file = jira_cli.Path("jira_issue_details") / "issue-KONFLUX-100.json"
    assert output_file.exists()
    with open(output_file, "r") as f:
        data = json.load(f)
    assert data["key"] == "KONFLUX-100"
    output_file.unlink()
    try:
        jira_cli.Path("jira_issue_details").rmdir()
    except OSError:
        pass


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "_load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_skips_string_description(
    mock_create_client, mock_load_config_fn, mock_translate, mock_config, mock_args
):
    mock_load_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False

    mock_issue = MagicMock()
    mock_issue.fields.description = "already a string"
    mock_issue.fields.comment.comments = []
    mock_jira.search_issues.return_value = [mock_issue]

    doer = jira_cli.Doer(mock_args)
    doer.do_list()

    mock_translate.assert_not_called()
    assert mock_issue.fields.description == "already a string"
