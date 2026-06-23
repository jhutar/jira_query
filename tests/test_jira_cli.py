#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import subprocess

import pytest
from unittest.mock import MagicMock, patch

# Import the dash-containing module dynamically
import jira_cli.cli as jira_cli


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
    args.template = None
    return args


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_project_validation_failure(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Make project fetch raise an exception (project doesn't exist)
    mock_jira.project.side_effect = Exception("Project not found")

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Project 'KONFLUX' does not exist or is inaccessible" in str(exc_info.value)


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_issue_type_validation_failure(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_status_validation_failure(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_assignee_validation_failure(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_valid_validation_flow(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    # Setup valid project and issue types
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Setup status and security levels via REST endpoint mock side_effect
    mock_jira._options = {"server": "https://jira.example.com"}

    def get_mock_response(url, *args, **kwargs):
        resp = MagicMock()
        resp.status_code = 200
        if "statuses" in url:
            resp.json.return_value = [{"name": "Task", "statuses": [{"name": "New"}]}]
        elif "securitylevel" in url:
            resp.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
        return resp

    mock_jira._session.get.side_effect = get_mock_response

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
    assert mock_jira.search_users.called
    assert not mock_jira.create_issue.called


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_uses_parent_field_for_epic(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_validation_failure(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_uses_parent_field_v3(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When --parent is specified under v3 config, payload contains parent: {key: ...}."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_legacy_fallback_epic_link(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When config has parent_link and issue type is Task, --parent routes to Epic Link custom field."""
    mock_config["custom_fields"]["parent_link"] = "customfield_10018"
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_legacy_fallback_parent_link(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When config has parent_link and issue type is Epic, --parent routes to Parent Link custom field."""
    mock_config["custom_fields"]["parent_link"] = "customfield_10018"
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_parent_and_epic_conflict(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.parent = "PARENT-1"
    mock_args.epic = "EPIC-1"

    doer = jira_cli.Doer(mock_args)

    with pytest.raises(AssertionError) as exc_info:
        doer.do_create()

    assert "Cannot specify both --parent and --epic" in str(exc_info.value)


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_subtask_requires_parent(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Creating a Sub-task without --parent must raise AssertionError."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_subtask_with_parent_passes_validation(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Creating a Sub-task with --parent should pass the Sub-task validation."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_feature_type_accepted(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Feature issue type should pass issue type validation when project supports it."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_update_status_with_resolution(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When --resolution is passed, transition_issue receives fields with the resolution."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_update_status_without_resolution(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When --resolution is not passed, transition_issue is called without fields."""
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_state_active(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_board_id(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_filter_by_board_id_and_state(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_refresh_deletes_cache(
    mock_create_client, mockload_config_fn, mock_config, tmp_path
):
    mockload_config_fn.return_value = mock_config
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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_sprints_execute_dispatch(
    mock_create_client, mockload_config_fn, mock_config
):
    mockload_config_fn.return_value = mock_config
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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_converts_description_to_adf(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_update_converts_comment_to_adf(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_converts_adf_description_to_md(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False
    mock_args.template = "templates/default.md.j2"

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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_converts_adf_comment_to_md(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

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
    mock_jira.search_issues.return_value = [mock_issue]

    mock_translate.return_value = "comment in markdown"

    doer = jira_cli.Doer(mock_args)
    doer.do_list()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_body))
    assert mock_comment.body == "comment in markdown"


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_prints_issue_details(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-123"
    args.dump = False
    args.with_comments = False
    args.with_enrichment = False

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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_converts_adf_description(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-456"
    args.dump = False
    args.with_comments = False
    args.with_enrichment = False

    adf_desc = {"type": "doc", "content": []}
    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-456"
    mock_issue.raw = {"fields": {"description": adf_desc}}
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
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_description_not_raw_object(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, capsys
):
    """Ensure PropertyHolder description objects are converted via raw ADF, not repr()."""
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-789"
    args.dump = False
    args.with_comments = False
    args.with_enrichment = False

    adf_desc = {
        "type": "doc",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
        ],
    }
    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-789"
    mock_issue.raw = {"fields": {"description": adf_desc}}
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "New"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = MagicMock()
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    mock_translate.return_value = "Hello markdown"

    doer = jira_cli.Doer(args)
    doer.do_view()

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    output = capsys.readouterr().out
    assert "Hello markdown" in output
    assert "PropertyHolder" not in output
    assert "MagicMock" not in output


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_converts_adf_comments(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-789"
    args.dump = False
    args.with_comments = True
    args.with_enrichment = False

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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_execute_dispatch(mock_create_client, mockload_config_fn, mock_config):
    mockload_config_fn.return_value = mock_config
    mock_create_client.return_value = MagicMock()

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"

    doer = jira_cli.Doer(args)

    with patch.object(doer, "do_view") as mock_do_view:
        doer.execute()

    mock_do_view.assert_called_once()


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_dump_writes_json(
    mock_create_client, mockload_config_fn, mock_config, tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-100"
    args.dump = True
    args.with_comments = False
    args.with_enrichment = False

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


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_no_comments_by_default(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-200"
    args.dump = False
    args.with_comments = False
    args.with_enrichment = False

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Bob"
    mock_comment.created = "2026-06-18T10:00:00.000+0000"
    mock_comment.body = "This should not appear"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-200"
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

    doer = jira_cli.Doer(args)
    doer.do_view()

    output = capsys.readouterr().out
    assert "Comments:" not in output
    assert "Bob" not in output
    assert "This should not appear" not in output


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_with_comments(
    mock_create_client, mockload_config_fn, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-201"
    args.dump = False
    args.with_comments = True
    args.with_enrichment = False

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Alice"
    mock_comment.created = "2026-06-18T14:20:00.000+0000"
    mock_comment.body = "Great progress on this"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-201"
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

    doer = jira_cli.Doer(args)
    doer.do_view()

    output = capsys.readouterr().out
    assert "Comments:" in output
    assert "Alice" in output
    assert "Great progress on this" in output


@patch.object(jira_cli, "enrich_with_prs")
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_with_enrichment(
    mock_create_client, mockload_config_fn, mock_enrich, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-202"
    args.dump = False
    args.with_comments = False
    args.with_enrichment = True

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-202"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "See https://github.com/org/repo/pull/42"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    mock_enrich.return_value = [
        {
            "url": "https://github.com/org/repo/pull/42",
            "info": "Title: Fix bug\nSome body",
        },
    ]

    doer = jira_cli.Doer(args)
    doer.do_view()

    output = capsys.readouterr().out
    assert "Enrichment:" in output
    assert "https://github.com/org/repo/pull/42" in output
    assert "Title: Fix bug" in output
    mock_enrich.assert_called_once()


@patch.object(jira_cli, "enrich_with_prs")
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_view_enrichment_includes_comments(
    mock_create_client, mockload_config_fn, mock_enrich, mock_config, capsys
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    args = MagicMock()
    args.config = "~/.jira_query.yaml"
    args.subparser_name = "view"
    args.issue_key = "KONFLUX-203"
    args.dump = False
    args.with_comments = True
    args.with_enrichment = True

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Dev"
    mock_comment.created = "2026-06-18T10:00:00.000+0000"
    mock_comment.body = "Fixed in https://github.com/org/repo/pull/99"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-203"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "Some description"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_jira.issue.return_value = mock_issue

    mock_enrich.return_value = []

    doer = jira_cli.Doer(args)
    doer.do_view()

    call_text = mock_enrich.call_args[0][0]
    assert "Some description" in call_text
    assert "Fixed in https://github.com/org/repo/pull/99" in call_text


@patch.object(jira_cli, "_translate_content")
@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_list_skips_string_description(
    mock_create_client, mockload_config_fn, mock_translate, mock_config, mock_args
):
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_args.subparser_name = "list"
    mock_args.query = "project = KONFLUX"
    mock_args.dump = False
    mock_args.template = "templates/default.md.j2"

    mock_issue = MagicMock()
    mock_issue.fields.description = "already a string"
    mock_issue.fields.comment.comments = []
    mock_jira.search_issues.return_value = [mock_issue]

    doer = jira_cli.Doer(mock_args)
    doer.do_list()

    mock_translate.assert_not_called()
    assert mock_issue.fields.description == "already a string"


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_inherits_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Creating a ticket without --security or --components inherits from project_defaults."""
    mock_config["project_defaults"] = {
        "KONFLUX": {
            "security": "Red Hat Employee",
            "components": ["Performance"],
        }
    }
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_jira._session.get.return_value = mock_response

    mock_args.security = None
    mock_args.components = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}
    assert create_call_fields["components"] == [{"name": "Performance"}]


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_cli_args_override_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Explicit CLI args override project_defaults values."""
    mock_config["project_defaults"] = {
        "KONFLUX": {
            "security": "Red Hat Employee",
            "components": ["Performance"],
        }
    }
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Public", "id": "10001"}]
    mock_jira._session.get.return_value = mock_response

    mock_args.security = "Public"
    mock_args.components = ["QE"]
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-102"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10001"}
    assert create_call_fields["components"] == [{"name": "QE"}]


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_sprint_current_from_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """sprint_current: true in project_defaults triggers sprint lookup."""
    mock_config["project_defaults"] = {
        "KONFLUX": {
            "sprint_current": True,
        }
    }
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_args.sprint_current = False
    mock_args.dry_run = True

    mock_board = MagicMock()
    mock_board.id = 1
    mock_board.name = "Konflux Board"
    mock_jira.boards.return_value = [mock_board]

    mock_sprint = MagicMock()
    mock_sprint.id = 42
    mock_sprint.name = "Konflux Sprint 1"
    mock_sprint.state = "active"
    mock_jira.sprints.return_value = [mock_sprint]

    doer = jira_cli.Doer(mock_args)
    doer._cache_sprints.obsolete = MagicMock(return_value=True)
    doer._cache_sprints.set = MagicMock()
    doer.do_create()

    assert mock_jira.boards.called or mock_jira.sprints.called


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_components_empty_string_overrides_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """Passing --components '' overrides project default components with empty list."""
    mock_config["project_defaults"] = {
        "KONFLUX": {
            "components": ["Performance"],
        }
    }
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_args.components = [""]
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-103"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["components"] == []


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_global_default_security_when_no_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When no project defaults and no CLI --security, global default 'Red Hat Employee' is applied."""
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_jira._session.get.return_value = mock_response

    mock_args.security = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-104"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}


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

    # Run helper
    jira_cli.convert_issue_adf_to_md(mock_issue)

    # Assertions
    assert mock_issue.fields.description == "Translated markdown text"
    assert mock_comment.body == "Translated markdown text"
    assert mock_translate.call_count == 2


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_security_opt_out_cli_arg(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When --security is explicitly set to empty string '', security is omitted from creation payload."""
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_args.security = ""
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-105"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert "security" not in create_call_fields


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_security_opt_out_project_defaults(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When security is set to '' in project_defaults, security is omitted from creation payload."""
    mock_config["project_defaults"] = {
        "KONFLUX": {
            "security": "",
        }
    }
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    mock_args.security = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-106"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert "security" not in create_call_fields


@patch.object(jira_cli, "load_config")
@patch.object(jira_cli, "_create_jira_client")
def test_do_create_security_rest_api_validation(
    mock_create_client, mockload_config_fn, mock_config, mock_args
):
    """When setting security, we fetch valid levels directly via standard GET /securitylevel REST endpoint."""
    mockload_config_fn.return_value = mock_config
    mock_jira = MagicMock()
    mock_create_client.return_value = mock_jira

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_jira.project.return_value = mock_project

    # Mock options and session to return 200 with JSON list of levels
    mock_jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_jira._session.get.return_value = mock_response

    mock_args.security = "Red Hat Employee"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-107"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_jira.create_issue.return_value = mock_issue

    doer = jira_cli.Doer(mock_args)
    doer.do_create()

    # Verify standard user GET endpoint was called and parsed successfully
    assert mock_jira._session.get.called
    create_call_fields = mock_jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}
