#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from unittest.mock import MagicMock, patch

import pytest

from jira_cli.commands import create


def test_create_project_validation_failure(mock_ctx, mock_args):
    mock_ctx.jira.project.side_effect = Exception("Project not found")

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert "Project 'KONFLUX' does not exist or is inaccessible" in str(exc_info.value)


def test_create_issue_type_validation_failure(mock_ctx, mock_args):
    mock_project = MagicMock()
    mock_project.issueTypes = []
    mock_ctx.jira.project.return_value = mock_project

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert "Issue type 'Task' is not valid for project 'KONFLUX'" in str(exc_info.value)


def test_create_status_validation_failure(mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Task", "statuses": [{"name": "New"}]}]
    mock_ctx.jira._session.get.return_value = mock_response

    mock_args.status = "InvalidStatus"

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert (
        "Status 'InvalidStatus' is not valid for issue type 'Task' in project 'KONFLUX'"
        in str(exc_info.value)
    )


def test_create_assignee_validation_failure(mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.search_users.return_value = []
    mock_args.assignee = "nonexistent-user"

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert "Expected exactly one user for 'nonexistent-user', but found 0" in str(
        exc_info.value
    )


def test_create_valid_validation_flow(mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}

    def get_mock_response(url, *args, **kwargs):
        resp = MagicMock()
        resp.status_code = 200
        if "statuses" in url:
            resp.json.return_value = [{"name": "Task", "statuses": [{"name": "New"}]}]
        elif "securitylevel" in url:
            resp.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
        return resp

    mock_ctx.jira._session.get.side_effect = get_mock_response

    mock_user = MagicMock()
    mock_user.displayName = "Test User"
    mock_user.accountId = "user-id-123"
    mock_ctx.jira.search_users.return_value = [mock_user]

    mock_args.status = "New"
    mock_args.security = "Red Hat Employee"
    mock_args.assignee = "test-user"

    create.run(mock_ctx, mock_args)

    assert mock_ctx.jira.project.called
    assert mock_ctx.jira._session.get.called
    assert mock_ctx.jira.search_users.called
    assert not mock_ctx.jira.create_issue.called


def test_create_uses_parent_field_for_epic(mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    mock_args.epic = "KONFLUX-100"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert "parent" in create_call_fields
    assert create_call_fields["parent"] == {"key": "KONFLUX-100"}


def test_create_parent_validation_failure(mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.side_effect = Exception("Issue not found")
    mock_args.parent = "NONEXIST-999"

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert "Parent issue 'NONEXIST-999' not found or inaccessible" in str(
        exc_info.value
    )


def test_create_uses_parent_field_v3(mock_ctx, mock_args):
    """When --parent is specified under v3 config, payload contains parent: {key: ...}."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    mock_args.parent = "PARENT-123"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert "parent" in create_call_fields
    assert create_call_fields["parent"] == {"key": "PARENT-123"}


def test_create_parent_legacy_fallback_epic_link(mock_ctx, mock_args):
    """When config has parent_link and issue type is Task, --parent routes to Epic Link custom field."""
    mock_ctx.config["custom_fields"]["parent_link"] = "customfield_10018"

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    mock_args.parent = "EPIC-100"
    mock_args.type = "Task"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert "parent" not in create_call_fields
    assert create_call_fields["customfield_10001"] == "EPIC-100"


def test_create_parent_legacy_fallback_parent_link(mock_ctx, mock_args):
    """When config has parent_link and issue type is Epic, --parent routes to Parent Link custom field."""
    mock_ctx.config["custom_fields"]["parent_link"] = "customfield_10018"

    mock_itype = MagicMock()
    mock_itype.name = "Epic"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    mock_args.parent = "FEATURE-50"
    mock_args.type = "Epic"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["customfield_10018"] == "FEATURE-50"


def test_create_parent_and_epic_conflict(mock_ctx, mock_args):
    mock_args.parent = "PARENT-1"
    mock_args.epic = "EPIC-1"

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert "Cannot specify both --parent and --epic" in str(exc_info.value)


def test_create_subtask_requires_parent(mock_ctx, mock_args):
    """Creating a Sub-task without --parent must raise AssertionError."""
    mock_args.type = "Sub-task"
    mock_args.parent = None

    with pytest.raises(AssertionError) as exc_info:
        create.run(mock_ctx, mock_args)

    assert (
        "A parent issue key (via --parent) is required when creating a Sub-task."
        in str(exc_info.value)
    )


def test_create_subtask_with_parent_passes_validation(mock_ctx, mock_args):
    """Creating a Sub-task with --parent should pass the Sub-task validation."""
    mock_args.type = "Sub-task"
    mock_args.parent = "KONFLUX-200"

    mock_itype_subtask = MagicMock()
    mock_itype_subtask.name = "Sub-task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype_subtask]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    create.run(mock_ctx, mock_args)

    assert not mock_ctx.jira.create_issue.called


def test_create_feature_type_accepted(mock_ctx, mock_args):
    """Feature issue type should pass issue type validation when project supports it."""
    mock_args.type = "Feature"

    mock_itype_feature = MagicMock()
    mock_itype_feature.name = "Feature"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype_feature]
    mock_ctx.jira.project.return_value = mock_project

    create.run(mock_ctx, mock_args)

    assert not mock_ctx.jira.create_issue.called


@patch("jira_cli.commands.create._translate_content")
def test_create_converts_description_to_adf(mock_translate, mock_ctx, mock_args):
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_translate.return_value = '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Test description"}]}]}'

    mock_args.dry_run = False
    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-adf", "Test description")
    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert isinstance(create_call_fields["description"], dict)
    assert create_call_fields["description"]["type"] == "doc"


def test_create_inherits_project_defaults(mock_ctx, mock_args):
    """Creating a ticket without --security or --components inherits from project_defaults."""
    mock_ctx.config["project_defaults"] = {
        "KONFLUX": {
            "security": "Red Hat Employee",
            "components": ["Performance"],
        }
    }

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_ctx.jira._session.get.return_value = mock_response

    mock_args.security = None
    mock_args.components = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-101"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}
    assert create_call_fields["components"] == [{"name": "Performance"}]


def test_create_cli_args_override_project_defaults(mock_ctx, mock_args):
    """Explicit CLI args override project_defaults values."""
    mock_ctx.config["project_defaults"] = {
        "KONFLUX": {
            "security": "Red Hat Employee",
            "components": ["Performance"],
        }
    }

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Public", "id": "10001"}]
    mock_ctx.jira._session.get.return_value = mock_response

    mock_args.security = "Public"
    mock_args.components = ["QE"]
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-102"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10001"}
    assert create_call_fields["components"] == [{"name": "QE"}]


def test_create_sprint_current_from_project_defaults(mock_ctx, mock_args):
    """sprint_current: true in project_defaults triggers sprint lookup."""
    mock_ctx.config["project_defaults"] = {
        "KONFLUX": {
            "sprint_current": True,
        }
    }

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_args.sprint_current = False
    mock_args.dry_run = True

    mock_board = MagicMock()
    mock_board.id = 1
    mock_board.name = "Konflux Board"
    mock_ctx.jira.boards.return_value = [mock_board]

    mock_sprint = MagicMock()
    mock_sprint.id = 42
    mock_sprint.name = "Konflux Sprint 1"
    mock_sprint.state = "active"
    mock_ctx.jira.sprints.return_value = [mock_sprint]

    with patch("jira_cli.commands.create.SprintResolver") as MockResolver:
        mock_resolver = MagicMock()
        MockResolver.return_value = mock_resolver
        mock_resolver.resolve.return_value = 42

        create.run(mock_ctx, mock_args)

        assert MockResolver.called or mock_ctx.jira.boards.called


def test_create_components_empty_string_overrides_project_defaults(mock_ctx, mock_args):
    """Passing --components '' overrides project default components with empty list."""
    mock_ctx.config["project_defaults"] = {
        "KONFLUX": {
            "components": ["Performance"],
        }
    }

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_args.components = [""]
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-103"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["components"] == []


def test_create_global_default_security_when_no_project_defaults(mock_ctx, mock_args):
    """When no project defaults and no CLI --security, global default 'Red Hat Employee' is applied."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_ctx.jira._session.get.return_value = mock_response

    mock_args.security = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-104"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}


def test_create_security_opt_out_cli_arg(mock_ctx, mock_args):
    """When --security is explicitly set to empty string '', security is omitted from creation payload."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_args.security = ""
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-105"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert "security" not in create_call_fields


def test_create_security_opt_out_project_defaults(mock_ctx, mock_args):
    """When security is set to '' in project_defaults, security is omitted from creation payload."""
    mock_ctx.config["project_defaults"] = {
        "KONFLUX": {
            "security": "",
        }
    }

    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_args.security = None
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-106"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert "security" not in create_call_fields


def test_create_security_rest_api_validation(mock_ctx, mock_args):
    """When setting security, we fetch valid levels directly via standard GET /securitylevel REST endpoint."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira._options = {"server": "https://jira.example.com"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Red Hat Employee", "id": "10000"}]
    mock_ctx.jira._session.get.return_value = mock_response

    mock_args.security = "Red Hat Employee"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-107"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    assert mock_ctx.jira._session.get.called
    create_call_fields = mock_ctx.jira.create_issue.call_args[1]["fields"]
    assert create_call_fields["security"] == {"id": "10000"}


def test_create_with_link(mock_ctx, mock_args):
    """When --link-relationship and --link-target are set, create_issue_link is called."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.return_value = MagicMock()

    mock_args.link_relationship = "is blocked by"
    mock_args.link_target = "KONFLUX-999"
    mock_args.dry_run = False

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-200"
    mock_issue.permalink.return_value = "https://jira.example.com/browse/KONFLUX-200"
    mock_issue.fields = MagicMock()
    mock_issue.fields.labels = []
    mock_ctx.jira.create_issue.return_value = mock_issue

    create.run(mock_ctx, mock_args)

    mock_ctx.jira.create_issue_link.assert_called_once_with(
        "is blocked by", "KONFLUX-200", "KONFLUX-999"
    )


def test_create_link_requires_both_args(mock_ctx, mock_args):
    """Specifying only --link-relationship without --link-target raises AssertionError."""
    mock_args.link_relationship = "blocks"
    mock_args.link_target = None

    with pytest.raises(AssertionError, match="must be specified together"):
        create.run(mock_ctx, mock_args)


def test_create_link_target_validation_failure(mock_ctx, mock_args):
    """When --link-target issue doesn't exist, raise AssertionError."""
    mock_itype = MagicMock()
    mock_itype.name = "Task"
    mock_project = MagicMock()
    mock_project.issueTypes = [mock_itype]
    mock_ctx.jira.project.return_value = mock_project

    mock_ctx.jira.issue.side_effect = Exception("Issue not found")

    mock_args.link_relationship = "relates to"
    mock_args.link_target = "NONEXIST-1"

    with pytest.raises(
        AssertionError, match="Link target issue 'NONEXIST-1' not found"
    ):
        create.run(mock_ctx, mock_args)
